import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

// The browser is installed separately by CI; it is not an app dependency.
const { chromium } = await import(pathToFileURL(process.env.PLAYWRIGHT_MODULE_PATH).href);
const destination = resolve(process.env.WAR_ROOM_SCREENSHOTS ?? 'output/war-room-layout-review');
await mkdir(destination, { recursive: true });
const browser = await chromium.launch({ headless: true });
const cases = [];
const errors = [];
const failures = [];
let failure;
let screenshotCount = 0;
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.on('pageerror', error => errors.push(error.message));
  for (const scenario of ['demo', 'reset']) {
    const url = pathToFileURL(resolve('dist/war-room-review/index.html'));
    if (scenario === 'reset') url.searchParams.set('scenario', 'reset');
    await page.goto(url.href);
    await page.getByRole('tab', { name: 'Today', exact: true }).waitFor();
    await page.evaluate(() => document.fonts.ready);
    for (const theme of ['dark', 'light']) {
      if (theme === 'light') await page.getByRole('button', { name: 'Light view', exact: true }).click();
      for (const width of [1920, 1440, 1024, 768, 390, 320]) {
        await page.setViewportSize({ width, height: 1000 });
        for (const tab of scenario === 'reset' ? ['Today', 'Time plan'] : ['Today', 'Subjects', 'Learning record', 'Time plan']) {
          await page.getByRole('tab', { name: tab, exact: true }).click();
          // Kobra retains the outgoing panel briefly for its exit animation.
          // Only the non-inert panel is the active, accessible tab content.
          const panel = page.locator('[data-slot=tabs-content]:not([inert])');
          await panel.waitFor();
          await page.waitForFunction(label => {
            const selected = [...document.querySelectorAll('[role=tab]')].find(element => element.textContent === label);
            return selected && getComputedStyle(selected, '::after').opacity === '1';
          }, tab);
          const geometry = await page.locator('.wr-tabs').evaluate(root => {
            const bounds = element => {
              const rect = element.getBoundingClientRect();
              return { left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom, width: rect.width };
            };
            const workspace = root.closest('.war-room-workspace');
            const current = root.querySelector('[data-slot=tabs-content]:not([inert])');
            const meta = current.querySelector('.wr-session-meta');
            const action = current.querySelector('.wr-session-actions [data-slot=button]');
            return {
              root: bounds(root),
              navigation: bounds(root.querySelector('[role=tablist]')),
              panel: bounds(current),
              workspaceWidth: workspace.clientWidth,
              workspaceScrollWidth: workspace.scrollWidth,
              viewportWidth: window.innerWidth,
              workspaceBackground: getComputedStyle(workspace).backgroundColor,
              actionGap: meta && action ? bounds(action).top - bounds(meta).bottom : null,
            };
          });
          const label = `${scenario} / ${theme} / ${width}px / ${tab}`;
          let passed = true;
          try {
            // These assertions check actual rendered geometry, not CSS declarations.
            assert.ok(geometry.panel.top >= geometry.navigation.bottom - 1, `${label}: panel must sit below the tabs`);
            assert.ok(Math.abs(geometry.panel.left - geometry.root.left) < 2, `${label}: content must align with the tabs`);
            assert.ok(Math.abs(geometry.panel.width - geometry.root.width) < 2, `${label}: content must use the available width`);
            assert.ok(geometry.panel.right <= geometry.viewportWidth + 1, `${label}: content must stay inside the viewport`);
            assert.equal(geometry.workspaceBackground, 'rgba(0, 0, 0, 0)', `${label}: the component scope must leave the page canvas visible`);
            if (geometry.actionGap !== null) assert.ok(geometry.actionGap >= 23.5, `${label}: session text needs at least 24px above its action (${geometry.actionGap}px)`);
            if (geometry.workspaceScrollWidth > geometry.workspaceWidth + 1) {
              const overflow = await page.locator('.war-room-workspace').evaluate(workspace => {
                const right = workspace.getBoundingClientRect().right;
                return [...workspace.querySelectorAll('*')]
                  .filter(element => element.getBoundingClientRect().right > right + 1)
                  .map(element => ({
                    tag: element.tagName,
                    className: String(element.className).slice(0, 160),
                    width: element.getBoundingClientRect().width,
                    text: element.textContent.slice(0, 80),
                  })).slice(0, 20);
              });
              console.log(JSON.stringify({ label, geometry, overflow }));
            }
            assert.ok(geometry.workspaceScrollWidth <= geometry.workspaceWidth + 1, `${label}: workspace must not overflow horizontally (${geometry.workspaceScrollWidth}/${geometry.workspaceWidth}px)`);
            const underline = await page.getByRole('tab', { name: tab, exact: true }).evaluate(element => {
              const style = getComputedStyle(element, '::after');
              return { opacity: style.opacity, height: style.height };
            });
            assert.equal(underline.opacity, '1', `${label}: selected tab must have an underline`);
            assert.equal(underline.height, '2px', `${label}: selected tab underline must be visible`);
          } catch (error) {
            passed = false;
            failures.push({ label, error: error.message });
            console.error(`${label}: ${error.message}`);
          }
          cases.push({ scenario, theme, width, tab, geometry, passed });
          if (width === 1440 || width === 390) {
            const filename = `${scenario === 'reset' ? 'reset-' : ''}${theme}-${width}-${tab.toLowerCase().replaceAll(' ', '-')}.png`;
            await page.locator('.review-product img').evaluateAll(async images => {
              await Promise.all(images.map(async image => {
                image.loading = 'eager';
                try { await image.decode(); } catch { /* Existing missing artwork uses its product fallback. */ }
              }));
            });
            await page.locator('.review-product').screenshot({ path: resolve(destination, filename), animations: 'disabled' });
            screenshotCount += 1;
            if (process.env.WAR_ROOM_LOG_SCREENSHOTS === '1') {
              // Review transport through the read-only logs connector when local
              // browser capture or artifact downloads are unavailable.
              console.log(`NSU_WAR_ROOM_SCREENSHOT ${JSON.stringify({ filename, data: (await readFile(resolve(destination, filename))).toString('base64') })}`);
            }
          }
        }
      }
    }
  }
  assert.deepEqual(errors, [], 'The implemented review must not throw browser errors');
  assert.deepEqual(failures, [], 'All rendered War Room layouts must fit');
  console.log(`Passed ${cases.length} browser layout checks; captured ${screenshotCount} screenshots.`);
} catch (error) {
  failure = String(error);
  const page = browser.contexts()[0]?.pages()[0];
  if (page) await page.screenshot({ path: resolve(destination, 'failure.png'), fullPage: true });
  throw error;
} finally {
  await writeFile(resolve(destination, 'results.json'), JSON.stringify({ cases, errors, failures, failure }, null, 2));
  await browser.close();
}
