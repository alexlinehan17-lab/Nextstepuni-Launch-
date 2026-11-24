# Native-feel mobile rules for a React + Capacitor app (iPhone, iPad, desktop web)

Research date: 2026-11-24. Web research only.

## How to read this file

- **[V]** = I fetched the source in this session and the rule/number is in it. Quoted text is verbatim from the source.
- **[S]** = seen only in a search-result summary or a secondary source; not confirmed against the primary page.
- **[U]** = not verified in this session (common practitioner knowledge, or my own synthesis). Treat as a design decision, not a citation.
- Apple HIG pages are JavaScript-rendered. I read them through Apple's own JSON endpoint
  (`https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`); the human-readable URL is
  `https://developer.apple.com/design/human-interface-guidelines/<slug>`. Both are given as the HIG URL below.
- The HIG now describes the Liquid Glass design language (floating tab bar, symbol-only Back/Close). The page text does not
  state an iOS version number.

---

## 1. Safe areas, notch, Dynamic Island, home indicator

### Rules

1. **Respect the safe area; it is what keeps hardware and system UI off your content.** [V] HIG Layout: "A safe area defines
   the area within a window that isn't covered on the edge by a hardware feature or another view within the window, like a
   toolbar, tab bar, or status bar. Respecting the safe area is essential to make sure system UI and hardware features like
   the Dynamic Island don't obstruct content and controls."
   https://developer.apple.com/design/human-interface-guidelines/layout
2. **Never hardcode inset values; read them.** Current values (points), from Use Your Loaf's device tables [V]:

   | Model | Screen (pt) | Status bar | Portrait top / bottom | Landscape left / right / top / bottom |
   |---|---|---|---|---|
   | iPhone 17 | 402 x 874 | 54 | 62 / 34 | 62 / 62 / 20 / 20 |
   | iPhone 17 Pro | 402 x 874 | 54 | 62 / 34 | 62 / 62 / 20 / 20 |
   | iPhone 17 Pro Max | 440 x 956 | 54 | 62 / 34 | 62 / 62 / 20 / 20 |
   | iPhone Air | 420 x 912 | 54 | 68 / 34 | 68 / 68 / 20 / 29 |
   | iPhone 16e | 390 x 844 | not stated | not stated | not stated |

   https://useyourloaf.com/blog/iphone-17-screen-sizes/
   - iPhone 16 (standard): top 59, bottom 34; iPhone 16 Pro: top 62, bottom 34, landscape left/right 62, bottom 21, top 0
     on the iOS version of that article. [S] https://useyourloaf.com/blog/iphone-16-screen-sizes/
   - The landscape **top** inset is now 20pt where earlier iOS returned 0. [V in the iPhone 17 table; S for the Apple
     forum thread https://developer.apple.com/forums/thread/801829]
   - Takeaway: top inset varies 59-68pt across current Dynamic Island phones; bottom (home indicator) is 34pt portrait
     and about 20-29pt landscape. The numbers are a third-party measurement, not an Apple-published table.
3. **Opt in to edge-to-edge with `viewport-fit=cover`, then pad with `env()`.** [V] WebKit: "The default value of
   `viewport-fit` is `auto`, which results in the automatic insetting behavior"; to fill the screen "you can set
   `viewport-fit` to `cover`." The four variables are `safe-area-inset-left`, `-right`, `-top`, `-bottom`.
   https://webkit.org/blog/7929/designing-websites-for-iphone-x/
4. **Combine insets with your normal gutter using `max()`, never add them blindly.** [V] WebKit: "Use max() to combine safe
   area insets with traditional margins" so padding is "the default padding or the safe area inset, whichever is greater."
   In portrait "the left safe area inset becomes 0px", so a bare `env()` leaves text touching the screen edge.
   Pattern: `padding-left: max(16px, env(safe-area-inset-left))`.
5. **Landscape: side insets appear (about 62-68pt on the sensor side and mirrored).** [V] WebKit: insets grow in landscape
   "when `env(safe-area-inset-left)` is larger due to the sensor housing." Backgrounds should bleed to the edge; content
   and controls should not.
6. **Home indicator: keep tappable controls above `env(safe-area-inset-bottom)`.** [V] WebKit: safe areas avoid "the
   corners, sensor housing, and indicator for accessing the Home screen." Bottom bars extend their background into the
   inset and pad their content by the inset.
7. **What must never sit in the top inset:** any interactive control or text. Only a background colour/material may extend
   under the status bar and Dynamic Island. This follows directly from the HIG safe-area sentence in rule 1 [V]; the
   "background only" phrasing is my summary [U].
8. **Do not use `100vh` for full-height screens.** [V] web.dev: "Although the viewport size can change, the `vw` and `vh`
   sizes do not. As a result, elements sized to be `100vh` tall will bleed out of the viewport." Use `100dvh` (tracks the
   UI), `100svh` (smallest) or `100lvh` (largest). Caveats: "The on-screen keyboard ... is not considered part of the UA
   UI" so it does not change these units, and "The values for the dynamic viewport do not update at 60fps."
   Support: Chrome 108, Edge 108, Firefox 101, Safari 15.4. https://web.dev/blog/viewport-units

### Capacitor-specific

9. **`ios.contentInset` defaults to `never`.** [V] Capacitor config: sets the WKWebView scroll view's content inset
   adjustment behaviour; values `automatic | scrollableAxes | never | always`; default `never`. So the web layer owns the
   insets via CSS. https://capacitorjs.com/docs/config
   - Do not combine `contentInset: 'always'` with CSS `env()` padding: the inset is applied twice. [S, community guide]
   - Missing `viewport-fit=cover` is the usual cause of `env()` returning 0. [S, community guide]
     https://capgo.app/blog/capacitor-iphone-duo-safe-area-guide/
10. **Status bar plugin.** [V] https://capacitorjs.com/docs/apis/status-bar
    - `overlaysWebView` default `true`: "Whether the statusbar is overlaid or not. Not available on Android 15+."
    - `backgroundColor`: "Doesn't work if `overlaysWebView` is true."
    - Style naming is inverted from what people expect: `Style.Dark` = "Light text for dark backgrounds"; `Style.Light` =
      "Dark text for light backgrounds"; `Default` = "based on the device appearance." Switch it with your theme.
    - Requires `UIViewControllerBasedStatusBarAppearance` = `YES` in Info.plist.
    - There is an iOS-only `statusTap` window event. The docs show the listener but do not say what to do with it; wiring
      it to scroll-to-top (the native convention) is my recommendation [U].
    - Android 16: the edge-to-edge opt-out is gone, so `overlaysWebView` and `backgroundColor` "no longer have any effect."
11. **Keyboard plugin.** [V] https://capacitorjs.com/docs/apis/keyboard
    - `resize` modes (iOS only), default `native`: "The whole native Web View will be resized when the keyboard shows/hides.
      This affects the `vh` relative unit." `body`: "Only the `body` HTML element will be resized. Relative units are not
      affected, because the viewport does not change." `ionic`: only `ion-app`. `none`: "Neither the app nor the Web View
      are resized."
    - `keyboardWillShow` delivers `keyboardHeight`; use it to lift a fixed composer/CTA above the keyboard.
    - `setAccessoryBarVisible` (iPhone only) hides the bar above the keyboard; docs recommend disabling it for short forms.
    - `setScroll({ isDisabled })` and `style` (Dark/Light/Default follows device appearance) are iOS only.
    - Do not rely on `env(keyboard-inset-height)` on iOS; it is a Chromium feature. [S]
12. **Other Capacitor config worth setting.** [V] `ios.backgroundColor` / `backgroundColor` (set to your page colour so
    overscroll and launch do not flash white), `zoomEnabled` default `false`, `ios.allowsLinkPreview`,
    `ios.scrollEnabled`, `plugins.SystemBars` (Capacitor 8: `insetsHandling` default `"css"`, Android only).
    https://capacitorjs.com/docs/config

---

## 2. Touch targets, spacing, thumb reach

1. **44 x 44 pt is the iOS target; 28 x 28 pt is Apple's stated floor.** [V] HIG Accessibility table: iOS/iPadOS default
   control size 44x44 pt, minimum 28x28 pt (macOS 28/20; visionOS 60/28).
   https://developer.apple.com/design/human-interface-guidelines/accessibility
   HIG Buttons: "a button needs a hit region of at least 44x44 pt ... to ensure that people can select it easily."
   https://developer.apple.com/design/human-interface-guidelines/buttons
2. **Spacing between targets.** [V] HIG Accessibility: "it works well to add about 12 points of padding around elements
   that include a bezel. For elements without a bezel, about 24 points of padding works well around the element's visible
   edges." (Same numbers in HIG Pointing devices.)
3. **WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA: 24 x 24 CSS px.** [V] "The size of the target for pointer inputs is
   at least 24 by 24 CSS pixels, except when" spacing ("a 24 CSS pixel diameter circle is centered on the bounding box of
   each, the circles do not intersect another target"), equivalent control, inline text, user-agent control, essential.
   https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
4. **WCAG 2.2 SC 2.5.5 Target Size (Enhanced), Level AAA: 44 x 44 CSS px.** [V]
   https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
5. **Android/Material: 48 x 48 dp, 8 dp apart.** [V] Google Android Accessibility Help: "Consider making touch targets at
   least 48x48dp, separated by 8dp of space or more." https://support.google.com/accessibility/android/answer/7101858
   (The m3.material.io page is JS-rendered and I could not read it directly. [U for the M3 page itself])
6. **NN/g physical size: 1 cm x 1 cm.** [V] "minimum size should be 1cm x 1cm (0.4in x 0.4in)"; average fingertip
   "1.6-2cm (0.6-0.8 in) wide", thumb impact area "an average of 2.5cm (1 inch) wide"; about 2 mm is "the
   often-recommended minimum" spacing. Primary CTAs, children and in-motion contexts need larger.
   https://www.nngroup.com/articles/touch-target-size/
7. **Visual size may be smaller than the hit area**, but the hit area must meet the target (e.g. a 24px icon inside a 44px
   button). [S for Material's wording; standard practice]
8. **Thumb reach.** [V] HIG Designing for iOS: "it tends to be easier and more comfortable for people to reach a control
   when it's located in the middle or bottom area of the display, so it's especially important to let people swipe to
   navigate back or initiate actions in a list row."
   https://developer.apple.com/design/human-interface-guidelines/designing-for-ios
9. **How people hold phones (Hoober, 1,333 observations, 780 touching).** [V] one-handed 49%, cradled 36%, two-handed 15%;
   one-handed is right thumb 67% / left thumb 33%. "Don't place low-priority or dangerous functions in hard-to-reach
   areas" is not the takeaway; the author's point is do not assume one grip. Important caveat: a 2017 editor's note says
   later research contradicts the reach drawings and that users favour the centre of the screen.
   https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php
   Smashing's thumb-zone article repeats 49% one-handed and "75% of interactions are thumb-driven" (Clark), and says to
   "keep frequently used links in the easy-to-reach zone." [V]
   https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/
10. **NN/g counterpoint:** do not justify a bottom sheet by reachability alone; the middle of the screen is usually
    easier to tap than the bottom. [V] https://www.nngroup.com/articles/bottom-sheet/
11. **Where the primary action goes on a phone.** Two native conventions, both sourced:
    - In a nav bar/sheet toolbar: the single primary action (Done, Submit) on the **trailing** side. [V] HIG Toolbars:
      "Only specify one primary action, and put it on the trailing side of the toolbar."
    - For a high-commitment CTA on a content screen: a full-width button pinned at the bottom above the home indicator
      is the widespread pattern; this specific placement is not stated in the HIG pages I read. [U]

---

## 3. Navigation model

### Tab bar vs sidebar (iPhone / iPad / desktop)

1. **iPhone: bottom tab bar for top-level sections.** [V] HIG Tab bars, iOS: "A tab bar floats above content at the bottom
   of the screen." https://developer.apple.com/design/human-interface-guidelines/tab-bars
2. **Tab bar is navigation only.** [V] "Use a tab bar to support navigation, not to provide actions."
3. **Keep it visible on pushed screens; hide only under modals.** [V] "Make sure the tab bar is visible when people navigate
   to different sections of your app. ... The exception is when a modal view covers the tab bar."
4. **How many tabs.** [V] HIG gives no hard number for iPhone; it says fewer is easier, "Avoid overflow tabs" (the More
   tab), and on iPad "aim for a default list of five or fewer to preserve continuity between compact and regular view
   sizes." NN/g: "If your site has more than 5 options, it's hard to fit them in a tab or navigation bar."
   https://www.nngroup.com/articles/mobile-navigation-patterns/
5. **Never disable or hide a tab.** [V] "Don't disable or hide tab bar buttons, even when their content is unavailable. ...
   If a section is empty, explain why its content is unavailable."
6. **Label every tab, single words, filled icons.** [V] "Include tab labels ... Use single words whenever possible";
   "Prefer filled symbols or icons." Badges: "Reserve badges for critical information."
7. **iPad: tab bar at the top, optionally convertible to a sidebar.** [V] "The system displays a tab bar near the top of the
   screen. You can choose to have the tab bar appear as a fixed element, or with a button that converts it to a sidebar."
   HIG Sidebars: "Consider using a tab bar first." "In general, show no more than two levels of hierarchy in a sidebar."
   "Avoid hiding the sidebar by default." https://developer.apple.com/design/human-interface-guidelines/sidebars
8. **Decide by size class, not device.** [V] HIG Layout: "Determine layout based on size classes, not device type or
   orientation." and "Consider taking advantage of larger spaces to switch from a tab bar to a sidebar or expose
   functionality that might otherwise be grouped into an overflow menu."
9. **Desktop: visible navigation, not a hamburger.** [V] NN/g: "Do not use hidden navigation (such as hamburger icons) in
   desktop user interfaces." Hidden nav was used in 27% of desktop tasks vs 48% visible; on mobile hidden 57% vs combo
   86%; discoverability dropped "more than 20%"; desktop tasks "at least 39% slower", mobile 15% slower. Mobile: "If your
   site has 4 or fewer top-level navigation links, display them as visible links."
   https://www.nngroup.com/articles/hamburger-menus/
10. **Segmented control is for sibling sub-views, not app sections.** [V] HIG: "Consider a segmented control to switch
    between closely related subviews. ... For switching between completely separate sections of an app, use a tab bar
    instead." https://developer.apple.com/design/human-interface-guidelines/segmented-controls

### Nav bar anatomy

11. **Leading = back; centre/leading = title; trailing = the one primary action and More.** [V] HIG Toolbars: "Elements that
    let people return to the previous document and show or hide a sidebar appear at the far leading edge, followed by the
    view title." "The trailing edge contains important items ... It also includes a primary action like Done when one
    exists." https://developer.apple.com/design/human-interface-guidelines/toolbars
12. **Titles: under 15 characters, never the app name.** [V] "keep the title under 15 characters long"; "Don't title
    windows with your app name."
13. **Large titles.** [V] "Use a large title to help people stay oriented as they navigate and scroll. By default, a large
    title transitions to a standard title as people begin scrolling the content, and transitions back to large when
    people scroll to the top." Type: Large Title is 34pt/41pt leading (see section 5).
14. **Few items.** [V] "Prioritize only the most important items for inclusion in the main toolbar area. ... Create a More
    menu to include additional items." Maximum of about three groups.
15. **One Back, standard symbol, no text label.** [V] "Use the standard Back and Close buttons. People know that the
    standard Back button lets them retrace their steps through a hierarchy of information, and the standard Close button
    closes a modal view. Prefer the standard symbols for each, and don't use a text label that says *Back* or *Close*."
16. **Edge-swipe back is an accelerator, the button stays.** [V] HIG Gestures: "people expect to find a Back button in a top
    toolbar that lets them return to the previous view with a single tap. To help accelerate this action, many apps also
    offer a shortcut gesture - such as swiping from the side of a window or touchscreen - while continuing to provide the
    Back button." Also: "Avoid conflicting with gestures that access system UI."
    https://developer.apple.com/design/human-interface-guidelines/gestures
    Note for Capacitor: WKWebView's own back-forward swipe is history-based, not stack-based; an app-level interactive
    swipe-back has to be built or supplied by a framework (Ionic does this). [U]

### Back vs Close vs Cancel vs Done vs Exit

Sourced definitions [V], HIG Sheets (https://developer.apple.com/design/human-interface-guidelines/sheets):

- **Back**: "lets people navigate to a previous step in a multi-step flow or to a parent view in a hierarchy. It isn't
  intended to dismiss a sheet." Chevron, leading edge. Pairs with push/pop.
- **Cancel (or Close)**: "dismisses a sheet without saving any changes." Leading edge of the sheet's top toolbar.
- **Done**: "dismisses a sheet after completing a task or explicitly saving changes." Trailing edge. "If you provide a
  Done button, always pair it with a Cancel button ... or a Back button." "Avoid showing all three buttons - Cancel,
  Done, and Back - together."
- Multi-step sheets: step 1 Cancel (leading) + inactive Done (trailing); later steps Back replaces Cancel; final step
  Done becomes active.
- **Unsaved input on dismiss**: [V] HIG Modality: "When necessary, help people avoid data loss by getting confirmation
  before closing a modal view. ... For example, in iOS, you might present an action sheet that includes a save option."
  HIG Sheets: "If people have unsaved changes in the sheet when they begin swiping to dismiss it, use an action sheet to
  let them confirm their action." https://developer.apple.com/design/human-interface-guidelines/modality
- **Alerts**: [V] "Always use "Cancel" to title a button that cancels the alert's action." Cancel is never the default
  button. https://developer.apple.com/design/human-interface-guidelines/alerts

Working distinction for the design system (the HIG treats "Cancel (or Close)" as one role; the finer split below is my
synthesis and should be labelled as house convention) [U]:

| Label | Glyph | Used when | Dismiss behaviour |
|---|---|---|---|
| Back | chevron, leading | pushed screen in a hierarchy | pop, no confirmation, edge-swipe works |
| Close | X | modal with nothing to lose (viewer, info sheet) | dismiss immediately, swipe-down works |
| Cancel | text | modal with editable input | dismiss; confirm via action sheet only if input is dirty |
| Done | text, trailing, prominent | commits/saves and dismisses | always paired with Cancel or Back |
| Exit | text or X plus confirmation | leaving an immersive session (timed test, focus mode) | confirm if progress would be lost |

**Exit** has no dedicated HIG definition that I found. Nearest sources [V]: HIG Going full screen, "Let people choose when
to exit full-screen mode"; and the Modality rule above about confirming when closing would lose user content.
https://developer.apple.com/design/human-interface-guidelines/going-full-screen

Breadcrumbs: [V] NN/g: breadcrumbs "augment but do not replace" main navigation, show hierarchy not history, must not
wrap on mobile, and on mobile "consider shortening the breadcrumb trail" to a single parent link. On a native-feeling
phone screen that single parent link *is* the Back button, so a breadcrumb plus a Back button is duplication.
https://www.nngroup.com/articles/breadcrumbs/

---

## 4. Sheets, modals, alerts, popovers, pickers

1. **Modality needs a reason.** [V] "Present content modally only when there's a clear benefit." "Always give people an
   obvious way to dismiss a modal view." "Let people dismiss a modal view before presenting another one." Avoid "a modal
   experience that feels like an app within your app."
   https://developer.apple.com/design/human-interface-guidelines/modality
2. **Sheet = brief, scoped task.** [V] "A sheet is useful for requesting specific information from people or presenting a
   simple task that they can complete before returning to the parent view." "Keep sheet interactions brief and
   occasional. ... Avoid using a sheet to help people navigate your app's content."
3. **Detents.** [V] "The system defines two detents: *large* is the height of a fully expanded sheet and *medium* is about
   half of the fully expanded height." Custom detents are allowed. "In an iPhone app, consider supporting the medium
   detent to allow progressive disclosure of the sheet's content."
4. **Grabber.** [V] "Include a grabber in a resizable sheet." It can be tapped to cycle detents and works with VoiceOver.
5. **Swipe to dismiss.** [V] "Support swiping to dismiss a sheet. People expect to swipe vertically to dismiss a sheet
   instead of tapping a dismiss button."
6. **Full-screen cover** for immersive or long multistep work. [V] "For complex or prolonged user flows, consider
   alternatives to sheets ... a full-screen style of modal view ... to help people perform multistep tasks." HIG
   Modality: "Consider using a full-screen modal style for in-depth content or a complex task."
7. **iPad sheets are centred cards.** [V] "Prefer using the page or form sheet presentation styles in an iPadOS app."
8. **Alerts: sparingly, max three buttons.** [V] "Use alerts sparingly." "Avoid using an alert merely to provide
   information." "Avoid displaying alerts for common, undoable actions, even when they're destructive." "alerts display a
   title, optional informative text, and up to three buttons." Default button trailing/top, Cancel leading/bottom. Button
   titles are verbs; avoid "OK" unless purely informational; avoid "Yes"/"No". Titles must not be "Error".
   https://developer.apple.com/design/human-interface-guidelines/alerts
9. **Action sheet** for choices following an intentional action. [V] "Use an action sheet - not an alert - to offer choices
   related to an intentional action." Cancel at the bottom; destructive at the top in the destructive style; "Avoid
   letting an action sheet scroll." https://developer.apple.com/design/human-interface-guidelines/action-sheets
10. **Popover**: regular width only. [V] "Avoid displaying popovers in compact views. ... Reserve popovers for wide views;
    for compact views, use all available screen space by presenting information in a full-screen modal view like a sheet
    instead." "Show one popover at a time." "Always save work when automatically closing a nonmodal popover."
    https://developer.apple.com/design/human-interface-guidelines/popovers
11. **NN/g on bottom sheets.** [V] Do not stack sheets; do not use them for page-to-page navigation (they are for
    "interruptions or a fork in the road"); not for long/complex content; support Back to dismiss; include a visible
    Close (X) "Rather than relying exclusively on the grab handle."
    https://www.nngroup.com/articles/bottom-sheet/

### Pickers and dropdowns on mobile

12. **Choose the control by list length.** [V] HIG Pickers: "Consider using a picker to offer medium-to-long lists of
    items. If you need to display a fairly short list of choices, consider using a pull-down button instead ... if you
    need to present a very large set of items, consider using a list or table."
    https://developer.apple.com/design/human-interface-guidelines/pickers
13. **Pop-up button (menu) for a flat, mutually exclusive choice.** [V] "Use a pop-up button to present a flat list of
    mutually exclusive options or states." Use a pull-down button for actions, multi-select or submenus. "Provide a useful
    default selection." https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons
14. **Segmented control for about 2-5 visible options.** [V] "no more than about five to seven segments in a wide interface
    and no more than about five segments on iPhone."
15. **Menus.** [V] "Prefer listing important or frequently used menu items first." "Use submenus sparingly", one level, and
    "if a submenu contains more than about five items, consider creating a new menu."
    https://developer.apple.com/design/human-interface-guidelines/menus
16. **Keep the picker in context.** [V] "Avoid switching views to show a picker. ... A picker typically appears at the
    bottom of a window or in a popover."
17. **Prefer choosing over typing.** [V] HIG Entering data: "When possible, offer choices instead of requiring text entry."
    https://developer.apple.com/design/human-interface-guidelines/entering-data
18. **HTML `<select>` vs custom.** In WKWebView a native `<select>` renders the iOS system picker/menu, which is
    accessible and native-looking; a desktop-style custom dropdown list is the "web tell". For long or searchable lists
    use a bottom-sheet selector or a pushed list with search. This mapping (short = segmented/menu, medium = menu or
    sheet, long = searchable list) follows rules 12-14 but the WKWebView rendering statement is not from a fetched
    source. [U]

---

## 5. Typography on iOS

1. **17pt default body, 11pt absolute floor.** [V] HIG Typography / Accessibility: iOS and iPadOS default size 17 pt,
   minimum 11 pt. https://developer.apple.com/design/human-interface-guidelines/typography
2. **iOS text styles at the default (Large) Dynamic Type size** [V]:

   | Style | Size / leading (pt) | Weight |
   |---|---|---|
   | Large Title | 34 / 41 | Regular (emphasised Bold) |
   | Title 1 | 28 / 34 | Regular |
   | Title 2 | 22 / 28 | Regular |
   | Title 3 | 20 / 25 | Regular |
   | Headline | 17 / 22 | Semibold |
   | Body | 17 / 22 | Regular |
   | Callout | 16 / 21 | Regular |
   | Subhead | 15 / 20 | Regular |
   | Footnote | 13 / 18 | Regular |
   | Caption 1 | 12 / 16 | Regular |
   | Caption 2 | 11 / 13 | Regular |

3. **No light weights.** [V] "In general, avoid light font weights ... prefer Regular, Medium, Semibold, or Bold font
   weights, and avoid Ultralight, Thin, and Light."
4. **Hierarchy through weight, size, colour.** [V] "Adjust font weight, size, and color as needed to emphasize important
   information and help people visualize hierarchy." "Minimize the number of typefaces you use."
5. **Dynamic Type / text scaling.** [V] HIG Accessibility: "give people the option to enlarge text by at least 200
   percent." WCAG 1.4.4 Resize Text (AA): "text can be resized without assistive technology up to 200 percent without loss
   of content or functionality." Keep hierarchy at large sizes: "keep primary elements toward the top of a view even when
   the font size is very large."
   In a Capacitor app the web layer does not automatically follow the iOS text-size setting; using `rem` units and the
   `-apple-system-body` font keyword (`font: -apple-system-body`) is the known technique, but I did not fetch a source
   for it this session. [U]
6. **Form inputs must be at least 16px or iOS zooms the page on focus.** [V] CSS-Tricks: Safari on iOS zooms when an
   input's font-size is 15px or less; 16px or larger does not zoom.
   https://css-tricks.com/16px-or-larger-text-prevents-ios-form-zoom/
7. **Line length.** [V] Baymard: "The optimal line length for body text is 50-75 characters"; suggests `max-width` about
   70ch / 34em; portrait phones rarely exceed it, landscape and iPad do. WCAG 1.4.8 (AAA): "Width is no more than 80
   characters or glyphs." https://baymard.com/blog/line-length-readability
   The HIG also mentions system layout guides that "restrict the width of text for optimal readability" [V] (no number
   given).
8. **Contrast thresholds for text**: see section 7.

---

## 6. Spacing systems

1. **8pt grid with 4pt half-steps.** [V] spec.fm: "Use multiples of 8 to define dimensions, padding, and margin"; a 4pt
   baseline grid is used for text. Rationale: consistency, fewer decisions, clean division on common screens. This is
   practitioner convention, not an Apple rule. https://spec.fm/specifics/8-pt-grid
2. **Standard iOS side margins 16pt (compact) / 20pt (larger widths).** [U] These are the widely quoted UIKit
   `systemMinimumLayoutMargins` values. Apple's doc confirms that "UIKit enforces a set of minimum layout margins" for a
   view controller's root view and that the values come from `systemMinimumLayoutMargins`, but the page I fetched gives no
   numbers. https://developer.apple.com/documentation/uikit/positioning-content-within-layout-margins
3. **Use system margins and guides rather than inventing gutters.** [V] HIG Layout: respect "system-defined safe areas,
   margins, and guides."
4. **Minimum gap between tappable things: 12pt (bezelled) / 24pt (unbezelled).** [V] HIG Accessibility (see section 2).
5. **Group by proximity; grouped lists use headers, footers and extra space.** [V] HIG Lists and tables: "the grouped style
   uses headers, footers, and additional space to separate groups of data."
   https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
   Concrete section-spacing numbers (for example 32-35pt between grouped sections, 44pt minimum row height) are common
   practitioner values that I did not verify against a source. [U]
6. **Concentric corner radii.** [V] HIG Toolbars: standard components "have corner radii that are concentric with bar
   corners. If you need to create a custom component, ensure that its corner radius is also concentric."

---

## 7. Dark mode

1. **Two background sets: base and elevated.** [V] HIG Dark Mode: "In Dark Mode, the system uses two sets of background
   colors - called *base* and *elevated* - to enhance the perception of depth when one dark interface is layered above
   another. The base colors are dimmer, making background interfaces appear to recede, and the elevated colors are
   brighter, making foreground interfaces appear to advance." Sheets and popovers move to elevated automatically.
   https://developer.apple.com/design/human-interface-guidelines/dark-mode
2. **Three hierarchy levels per set, two sets (system and grouped).** [V] HIG Color: "Primary for the overall view",
   "Secondary for grouping content or elements within the overall view", "Tertiary for grouping content or elements
   within secondary elements." So a token model of 3 surface levels x base/elevated is the Apple structure; more than
   that produces near-duplicate greys. https://developer.apple.com/design/human-interface-guidelines/color
   The actual hex values (commonly quoted as #000000 base / #1C1C1E elevated or secondary, #2C2C2E tertiary) are not on
   the HIG page I read. [U] Note that Apple's own base background in dark mode is true black on OLED iPhones; "never
   pure black" is a Material rule, not an Apple one.
3. **Four label levels.** [V] label, secondaryLabel, tertiaryLabel, quaternaryLabel. Text hierarchy comes from these
   semantic levels, not ad-hoc greys.
4. **Dark is not an inversion.** [V] "these colors aren't necessarily inversions of their light counterparts."
5. **Tokens, never hard-coded values.** [V] "Avoid using hard-coded color values or colors that don't adapt." Every custom
   colour needs a light and dark variant.
6. **Contrast.** [V] HIG Dark Mode: "At a minimum, make sure the contrast ratio between colors is no lower than 4.5:1. For
   custom foreground and background colors, strive for a contrast ratio of 7:1, especially in small text."
   WCAG 1.4.3 (AA): 4.5:1 normal text, 3:1 large text (18pt, or 14pt bold).
   https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
   WCAG 1.4.11 (AA): 3:1 for UI component boundaries/states and meaningful graphics.
   https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
   HIG Accessibility table: up to 17pt 4.5:1; 18pt 3:1; bold 3:1.
7. **Follow the system setting; no in-app-only switch.** [V] "Avoid offering an app-specific appearance setting." (NN/g
   agrees on using OS dark-mode APIs, but also recommends letting users switch.)
8. **Soften white content.** [V] "Soften the color of white backgrounds" for images in dark mode.
9. **Test with Increase Contrast and Reduce Transparency.** [V]
10. **Why not pure black, how many levels, desaturating accents (Material).** Material's dark theme guidance is the usual
    citation: dark grey #121212 surface rather than black, lighter overlays at higher elevation (commonly quoted 5% at
    1dp up to 16% at 24dp), desaturated accent tones (the 200 tone), text at 87% / 60% / 38% opacity. I could not load
    material.io (JS-rendered), so **all of those numbers are unverified this session**. [U] What I could verify:
    Material's Android docs say dark surfaces are "dark grey instead of black" and that "surfaces become lighter" at
    higher elevation because shadows are less visible on dark backgrounds [V]
    https://github.com/material-components/material-components-android/blob/master/docs/theming/Dark.md
    and Google's theming codelab: "Dark themes use a dark surface color, with limited color accents" [V]
    https://developer.android.com/codelabs/basic-android-kotlin-compose-material-theming
    The HIG dark-mode page contains no guidance on desaturation. [V, absence confirmed]
11. **Light as default for reading-heavy products.** [V] NN/g: "in users with normal vision, light mode leads to better
    performance most of the time", stronger at small font sizes; "we strongly recommend that designers allow users to
    switch to dark mode if they want to." https://www.nngroup.com/articles/dark-mode/
12. **Colour meaning.** [V] HIG Color: "Avoid using the same color to mean different things." "Avoid relying solely on
    color to differentiate between objects, indicate interactivity, or communicate essential information."

---

## 8. Buttons, hierarchy, disabled states, validation

1. **One, at most two, prominent buttons per view.** [V] HIG Buttons: "Keep the number of prominent buttons to one or two
   per view." https://developer.apple.com/design/human-interface-guidelines/buttons
2. **Distinguish by style, not size.** [V] "Use style - not size - to visually distinguish the preferred choice among
   multiple options." The current HIG page does not name filled/tinted/gray/plain; those are the UIKit
   `UIButton.Configuration` names (filled > tinted > gray > plain as descending emphasis). [U for the four-name ladder]
3. **Roles.** [V] Primary ("the button people are most likely to choose", accent colour), Cancel, Destructive (system red).
   "Don't assign the primary role to a button that performs a destructive action, even if that action is the most likely
   choice."
4. **Toolbar primary action: one, trailing, prominent.** [V] HIG Toolbars.
5. **Labels start with a verb.** [V] "consider starting the label with a verb", e.g. "Add to Cart".
6. **In-button progress.** [V] "Configure a button to display an activity indicator when you need to provide feedback about
   an action that doesn't instantly complete" and change the label ("Checkout" to "Checking out...").
7. **Disabled CTAs: two sources disagree; pick one deliberately.**
   - Apple [V], HIG Entering data: "if you include a Next or Continue button after a set of text fields, make the button
     available only after people enter the data you require." Apple also expects "Done ... in an inactive state" on the
     first step of a multi-step sheet.
   - Smashing (Vitaly Friedman) [V]: "Disabled buttons don't explain what's wrong." Keep the button enabled, validate on
     submit, show which fields are wrong, link to the first error. Disabled is acceptable while a process is running,
     to prevent double submission, or for a genuinely unavailable item. If you must disable, use `aria-disabled` rather
     than `disabled` so it stays focusable and can explain itself, and do not use `pointer-events: none`.
     https://www.smashingmagazine.com/2021/08/frustrating-design-patterns-disabled-buttons/
   - NN/g [V, video summary only; transcript not readable]: "Disabled buttons often confuse users by appearing clickable
     but providing no response or feedback." "Designers should use them sparingly, ensure they're accessible, and clearly
     explain why the button is disabled."
     https://www.nngroup.com/videos/why-disabled-buttons-hurt-ux-and-how-to-fix-them/
   - Reconciliation that satisfies both: if a CTA looks unavailable, tapping it must still respond by saying what is
     missing and moving focus there; or always state the requirement next to the button. HIG Feedback supports this [V]:
     "Show people when a command can't be carried out and help them understand why."
     https://developer.apple.com/design/human-interface-guidelines/feedback
   - Contrast: WCAG 1.4.3 and 1.4.11 exempt inactive components [V], so a faint disabled button passes WCAG while still
     being unreadable; that is a usability argument, not a conformance one.
8. **Inline validation timing.** [V] HIG Text fields: "when entering an email address, it's best to validate when people
   switch to another field; when creating a user name or password, validation needs to happen before people switch to
   another field." HIG Entering data: "Dynamically validate field values." NN/g: do not show errors too soon; put the
   message next to the field, never colour alone, say how to fix it, preserve the input.
   https://www.nngroup.com/articles/error-message-guidelines/
9. **Labels, not just placeholders.** [V] HIG Text fields: "Because placeholder text disappears when people start typing,
   it can also be useful to include a separate label." Match the keyboard type to the input.
   https://developer.apple.com/design/human-interface-guidelines/text-fields

---

## 9. Long pages and content density

1. **Progressive disclosure, max two levels.** [V] NN/g: "Initially, show users only a few of the most important options."
   "Designs that go beyond 2 disclosure levels typically have low usability." Staged disclosure (wizard) suits tasks with
   "distinct steps that have little interaction." https://www.nngroup.com/articles/progressive-disclosure/
   HIG [V]: "Use a disclosure control to hide details until they're relevant." "Use no more than one disclosure button in
   a single view." https://developer.apple.com/design/human-interface-guidelines/disclosure-controls
2. **Drill-down list beats a long row.** [V] HIG Lists: "Keep item text succinct ... you could list item titles only,
   letting people choose an item to reveal its content in a detail view." Use a disclosure indicator (chevron) for
   drill-in, an info button only for extra details. Persistently highlight the selected row in hierarchical navigation.
3. **Lists beat cards for homogeneous, scannable, comparable items.** [V] NN/g: "Cards work best for collections of
   heterogeneous items"; card layouts "deemphasize the ranking of content"; "Cards take more space"; for similar items use
   a vertical list or grid; lists are better for searching, scanning and comparison.
   https://www.nngroup.com/articles/cards-component/
   HIG [V]: "Prefer displaying text in a list or table."
4. **Accordions vs separate views.** [V] NN/g: accordions suit pages where people need "only a few key pieces of content";
   "Accordions should be avoided" when people need most of the page; "Accordions increase interaction cost." On mobile
   "people often stop scrolling before reaching the end of an extremely long page" so collapsing helps. Let multiple
   sections stay open. https://www.nngroup.com/articles/accordions-complex-content/
5. **Search has one prominent home.** [V] HIG Searching: "If search is important, give it a primary position"; in tab-bar
   apps "search is a dedicated tab"; "Aim to make your app's content searchable through a single location"; "Clearly
   display the current scope of a search"; show recents and suggestions.
   https://developer.apple.com/design/human-interface-guidelines/searching
6. **Segmented controls** for 2 to about 5 sibling views (see section 4).
7. **Filters/chips, sticky headers.** No authoritative numeric rule found this session. iOS grouped-list section headers
   stick natively and large titles collapse on scroll [V for large titles]; chip-row guidance is practitioner
   convention. [U]
8. **Limit on-screen controls.** [V] HIG Designing for iOS: "Help people concentrate on primary tasks and content by
   limiting the number of onscreen controls while making secondary details and actions discoverable with minimal
   interaction."

---

## 10. Motion and haptics

1. **Purposeful, brief, optional, cancellable.** [V] HIG Motion: "Don't add motion for the sake of adding motion." "Aim for
   brevity and precision in feedback animations." "In apps, generally avoid adding motion to UI interactions that occur
   frequently." "Make motion optional." "don't make people wait for an animation to complete before they can do
   anything." The HIG gives **no durations**. https://developer.apple.com/design/human-interface-guidelines/motion
2. **System default is a critically damped spring.** [V] Apple docs: SwiftUI `Animation.default` is a spring with
   `response` 0.55, `dampingFraction` 1.0 (no bounce); before iOS 17 it was `easeInOut`.
   https://developer.apple.com/documentation/swiftui/animation/default
3. **A web approximation of the iOS push.** [V] Ionic's iOS page transition uses 540ms with
   `cubic-bezier(0.32, 0.72, 0, 1)`, leaving page dims to 0.8 opacity.
   https://github.com/ionic-team/ionic-framework/blob/main/core/src/utils/transition/ios.transition.ts
   The often-quoted UIKit figures (push about 0.35s, sheet about 0.5s) were **not** confirmed. [U]
4. **What animates:** spatial transitions that explain hierarchy (push from trailing edge, sheet from bottom), state
   changes that follow a gesture. **What does not:** frequent taps, list scrolling content, decoration. [V for the HIG
   principles above; the specific list is my summary]
5. **Reduce Motion.** [V] HIG Accessibility: reduce "automatic and repetitive animations, including zooming, scaling, and
   peripheral motion"; "Tightening animation springs to reduce bounce effects"; "Replacing transitions in x-, y-, and
   z-axes with fades"; "Avoiding animating into and out of blurs." Web: `@media (prefers-reduced-motion: reduce)`, remove
   non-essential movement, parallax, zoom, autoplay. JS animations need a `matchMedia` listener.
   https://web.dev/articles/prefers-reduced-motion
   WCAG 2.3.3 (AAA): "Motion animation triggered by interaction can be disabled, unless the animation is essential."
   WCAG 2.2.2 (A) covers auto-starting motion lasting more than five seconds.
6. **Haptics.** [V] HIG Playing haptics: "Use system-provided haptic patterns according to their documented meanings."
   "Avoid overusing haptics." "Make haptics optional." Types: Notification (success, warning, error); Impact (light,
   medium, heavy, rigid, soft) for collisions/snaps; Selection for a changing value.
   https://developer.apple.com/design/human-interface-guidelines/playing-haptics
   In Capacitor these map to the `@capacitor/haptics` plugin; I did not fetch that doc. [U]
7. **Multi-channel feedback.** [V] HIG Feedback: "when you provide feedback using color, text, sound, and haptics, people can
   receive it whether they silence their device, look away from the screen, or use VoiceOver."

---

## 11. Empty, error, loading states

1. **Loading: show something at once.** [V] HIG Loading: "Show something as soon as possible. ... consider showing
   placeholder text, graphics, or animations as content loads." Determinate indicator when duration is known,
   indeterminate when not. https://developer.apple.com/design/human-interface-guidelines/loading
2. **Thresholds.** [V] NN/g: under 1 second, no skeleton or spinner; 2-10 seconds, spinner (single module) or skeleton
   (full page); over 10 seconds, progress bar with estimate. Static skeletons preferred; shimmer can distract;
   frame-only skeletons not recommended. https://www.nngroup.com/articles/skeleton-screens/
3. **Empty states do three jobs.** [V] NN/g: communicate system status ("Totally empty states cause confusion about how and
   whether the system is working"), teach ("contextual help relevant to the user's task"), and "Provide direct pathways
   ... to getting started with key tasks." Do not show "No records" while still loading.
   https://www.nngroup.com/articles/empty-state-interface-design/
   HIG Tab bars [V]: "If a section is empty, explain why its content is unavailable."
4. **Errors.** [V] NN/g: "Display the error message close to the error's source"; "never use exclusively color or animation
   to indicate errors"; "Use human-readable language"; "offer some potential remedies"; preserve input; match severity to
   presentation (modal only for severe). HIG Alerts: never title an alert "Error". HIG Feedback: "Use alerts to deliver
   critical - and ideally actionable - information."
5. **Confirm only what matters.** [V] HIG Feedback: "people typically expect their action or task to succeed, they only need
   to know when it doesn't." Warn only for data loss "that's unexpected and irreversible."

---

## 12. iPad

1. **Layout by size class.** [V] HIG Layout: each dimension is compact or regular; "Consider all possible combinations of
   size classes"; iPad windows resize, so a regular-width design can become compact.
2. **Do not stretch the phone layout.** [V] HIG Designing for iPadOS: "Take advantage of the large display to elevate the
   content people care about, minimizing modal interfaces and full-screen transitions." "Use viewing distance and input
   mode to help you determine the size and density of the onscreen content."
   https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados
3. **Split view in regular width.** [V] "Prefer using a split view in a regular - not a compact - environment." Two or three
   panes; "persistently highlight the current selection in each pane"; "Account for narrow, compact, and intermediate
   window widths." https://developer.apple.com/design/human-interface-guidelines/split-views
4. **Navigation: top tab bar and/or sidebar** (section 3).
5. **Sheets become form/page sheets; popovers are allowed** (section 4).
6. **Keep functionality the same across sizes.** [V] "Keep functionality the same as size classes change, and keep layout
   changes recognizable and familiar."
7. **Pointer and keyboard.** [V] HIG Pointing devices: the pointer "doesn't replace touch"; three effects (highlight, lift,
   hover); "Add padding around interactive elements to create comfortable hit regions" (12pt bezelled / 24pt
   unbezelled); "Create contiguous hit regions for custom bar buttons"; "Distinguish between pointer and finger input
   only if it provides value." https://developer.apple.com/design/human-interface-guidelines/pointing-devices
   Web mapping: gate hover styles with `@media (hover: hover) and (pointer: fine)`. [U, standard CSS; not fetched]
8. **Orientation.** [V] WCAG 1.3.4 (AA): "Content does not restrict its view and operation to a single display
   orientation." iPad should support both.
9. **Line length on iPad**: cap reading columns at about 70ch (section 5).

---

## 13. Accessibility essentials beyond the above

All WCAG text below [V] from https://www.w3.org/TR/WCAG22/ unless marked.

- **Focus Visible 2.4.7 (AA):** "Any keyboard operable user interface has a mode of operation where the keyboard focus
  indicator is visible." Matters for iPad keyboards and desktop.
- **Focus Not Obscured 2.4.11 (AA):** focused component "is not entirely hidden due to author-created content" (sticky
  headers, bottom CTAs, the keyboard).
- **Focus Appearance 2.4.13 (AAA).**
- **Use of Color 1.4.1 (A):** colour is never the only signal.
- **Non-text contrast 1.4.11 (AA):** 3:1 for control boundaries, states, icons.
- **Reflow 1.4.10 (AA)**, **Text Spacing 1.4.12 (AA)**, **Resize Text 1.4.4 (AA, 200%)**.
- **Pointer Gestures 2.5.1 (A):** every swipe/drag/pinch has a single-tap alternative. HIG agrees: gestures "supplement
  standard gestures, not replace them."
- **Pointer Cancellation 2.5.2 (A):** act on pointer-up, allow abort.
- **Content on Hover or Focus 1.4.13 (AA):** no hover-only content.
- **Dragging Movements 2.5.7, Name/Role/Value 4.1.2, Error Identification 3.3.1, Error Suggestion 3.3.3:** exist in
  WCAG 2.2, but the page was truncated before I could quote them. [U for verbatim text]
- **Labels for VoiceOver / Voice Control.** [V] HIG Accessibility: "Describe your app's interface and content for
  VoiceOver"; "label interface elements appropriately." Icon-only buttons need an accessible name.
- **Reduce Motion, Increase Contrast, Reduce Transparency** honoured (sections 7, 10).

---

## 14. "Website in a phone shell" tells, and the fix

| # | Tell | Fix | Source |
|---|---|---|---|
| 1 | Header or fixed element sits under the status bar / Dynamic Island | `viewport-fit=cover` + `padding-top: env(safe-area-inset-top)`; background may bleed, content may not | WebKit, HIG Layout [V] |
| 2 | Bottom bar/CTA collides with the home indicator | pad by `env(safe-area-inset-bottom)` (34pt portrait) | WebKit, Use Your Loaf [V] |
| 3 | `100vh` layouts clipped or jumpy | `100dvh`/`svh`; in Capacitor decide `Keyboard.resize` mode deliberately | web.dev, Capacitor [V] |
| 4 | Keyboard covers the focused field or the CTA | use `keyboardWillShow.keyboardHeight`; choose resize `native` vs `body`; WCAG 2.4.11 | Capacitor, WCAG [V] |
| 5 | Page zooms when an input is focused | input font-size at least 16px | CSS-Tricks [V] |
| 6 | Tiny tap targets, tightly packed links | 44x44pt hit area, 12/24pt padding; never below 24px (WCAG AA) | HIG, WCAG 2.5.8 [V] |
| 7 | Hover-dependent UI (tooltips, hover menus, hover-reveal actions) | everything reachable by tap; hover is an enhancement on pointer devices only | WCAG 1.4.13, HIG Pointing devices [V] |
| 8 | Hamburger menu for 3-5 top-level sections | bottom tab bar on iPhone, top tab bar/sidebar on iPad, visible nav on desktop | HIG Tab bars, NN/g [V] |
| 9 | Tab bar disappears on detail screens, or tabs trigger actions | keep it on all pushed screens; hide only under modals; tabs navigate only | HIG Tab bars [V] |
| 10 | Breadcrumbs plus a Back link plus a logo-home link | one Back chevron, leading edge, plus edge-swipe | HIG Toolbars/Gestures, NN/g breadcrumbs [V] |
| 11 | Back that says "Back to X" as a text link in the content | standard chevron in the nav bar, no "Back"/"Close" text label | HIG Toolbars [V] |
| 12 | Centred desktop modal dialog with an X in the corner on a phone | sheet with detents and grabber, swipe to dismiss; full-screen cover for long tasks | HIG Sheets, Popovers [V] |
| 13 | Modal on top of modal | dismiss one before presenting another; no stacked sheets | HIG Modality, NN/g [V] |
| 14 | `window.alert`-style or toast-only confirmations for everything | alerts sparingly with verb buttons; action sheet for choices; inline status otherwise | HIG Alerts, Feedback [V] |
| 15 | Web-style custom dropdown lists | segmented (up to about 5), menu/pop-up button, picker or searchable list for long sets, shown in context | HIG Pickers, Pop-up buttons [V] |
| 16 | Several equally loud buttons; primary action top-right in the content area | one prominent action per view; in a nav bar it is trailing; otherwise in the lower, reachable area | HIG Buttons, Toolbars, Designing for iOS [V]; bottom-pinned CTA placement [U] |
| 17 | Whole page rubber-bands, including fixed header and tab bar | fixed shell; only the content region scrolls; `overscroll-behavior: none/contain` on the root and on sheets | MDN [V] https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior ; shell architecture [U] |
| 18 | Scroll chaining: sheet scroll continues into the page behind | `overscroll-behavior: contain` on the sheet's scroller | MDN [V] |
| 19 | Grey tap flash on every tap | `-webkit-tap-highlight-color: transparent` and supply your own pressed state | MDN [V] https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-tap-highlight-color |
| 20 | UI chrome text is selectable; long-press shows the callout/link preview | `user-select: none` and `-webkit-touch-callout: none` on chrome (keep content selectable); `ios.allowsLinkPreview: false` | Capacitor config [V]; CSS properties [U] |
| 21 | Pinch-zoom of the app UI | Capacitor `zoomEnabled` defaults to false; do not block text scaling as a side effect | Capacitor config [V] |
| 22 | No pressed state / delayed response to touch | immediate visual press feedback; optional light haptic on significant actions | HIG Motion, Haptics [V] |
| 23 | Page navigations cross-fade or hard-cut like web routes | push slides in from trailing edge, modal rises from bottom; about 540ms `cubic-bezier(0.32,0.72,0,1)` or a no-bounce spring; fade under reduced motion | Ionic source, Apple docs, HIG Accessibility [V] |
| 24 | Scroll position lost on Back; tab re-tap does nothing | preserve per-screen scroll; status-bar tap and tab re-tap scroll to top | Capacitor `statusTap` exists [V]; behaviour [U] |
| 25 | White flash on launch or overscroll in dark mode | set `backgroundColor` in Capacitor config to the theme surface | Capacitor config [V]; flash claim [U] |
| 26 | Status bar text unreadable against the header | set `StatusBar` style per theme (Dark = light text) | Capacitor [V] |
| 27 | Full-screen spinner on every navigation | nothing under 1s; skeleton for full-page 2-10s; keep previous content visible | NN/g, HIG Loading [V] |
| 28 | Card grids for uniform items; long accordions of everything | lists with drill-down; accordions only when few sections are needed | NN/g, HIG Lists [V] |
| 29 | iPad shows the phone column stretched or letterboxed | size-class layout: sidebar/split view, form sheets, popovers, 70ch reading width | HIG [V] |
| 30 | Ignores system text size, dark mode, reduce motion | respond to all three | HIG Designing for iOS [V] |
| 31 | Long text labels and titles in the nav bar; app name as title | title under 15 characters; never the app name | HIG Toolbars [V] |
| 32 | Footer links, cookie-style banners, web page footers in app screens | remove; app screens end with content | [U] |

---

## 15. Could not verify (summary)

1. Material dark-theme numbers (#121212, overlay percentages 5-16%, 87/60/38% text opacity, desaturated 200 tones):
   material.io would not render. Only the qualitative statements are verified.
2. iOS standard margins of 16pt/20pt and any section-spacing/row-height numbers: Apple's doc confirms system minimum
   margins exist but gives no values on the page fetched.
3. UIKit animation durations (0.35s push, 0.5s sheet): not found. Verified substitutes are SwiftUI's default spring and
   Ionic's 540ms curve.
4. The four-way Close / Cancel / Done / Exit distinction: the HIG defines Back, "Cancel (or Close)" and Done; it has no
   definition of "Exit". The table in section 3 is a house convention built on those plus the unsaved-changes rule.
5. Filled/tinted/gray/plain as a named hierarchy: not on the current HIG Buttons page.
6. Bottom-pinned full-width CTA as "the" primary-action position: not stated in the HIG pages read.
7. Per-device safe-area numbers are third-party (Use Your Loaf), and iPhone 16-series values came from a search summary.
8. NN/g disabled-button guidance: only the video summary was readable. The detailed "keep it enabled" guidance is from
   Smashing Magazine. Apple's own guidance points the other way.
9. Hoober's thumb-zone maps carry the author's own 2017 note that later research contradicts them.
10. Dynamic Type inside WKWebView (`-apple-system-body`), `@capacitor/haptics`, `user-select` / `-webkit-touch-callout`,
    `@media (hover: hover)`: standard techniques, not fetched this session.
11. WCAG 2.5.7, 3.3.1, 3.3.3, 4.1.2 verbatim text: page truncated.
12. m3.material.io touch-target page: not readable; the 48dp / 8dp figure is verified from Google's Android
    Accessibility Help instead.
