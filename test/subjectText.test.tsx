import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it, vi } from 'vitest';
import { grayTheme } from '@/moduleThemes';
import { SUBJECT_MODULE_CONTENT } from '@/subjectModuleData';
vi.mock('@/components/ModuleShared', () => ({ Highlight: ({children}: {children: React.ReactNode}) => <mark>{children}</mark> }));
vi.mock('@/components/ModuleReferences', () => ({ Cite: ({n}: {n: number}) => <sup data-cite={n} /> }));
import { renderSubjectText } from '@/components/SubjectText';
function output(text: string) {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = renderToStaticMarkup(<>{renderSubjectText(text, [{term: 'term', description: 'Meaning'}], grayTheme)}</>);
  return wrapper;
}
describe('subject lesson notation', () => {
  it('renders nested highlights and italics inside bold, with citations intact', () => {
    const result = output('Read **the [[term]] and *its meaning***. {{cite:2}}');
    expect(result.querySelector('strong mark')?.textContent).toBe('term');
    expect(result.querySelector('strong em')?.textContent).toBe('its meaning');
    expect(result.querySelector('sup')).toHaveAttribute('data-cite', '2');
    expect(result.textContent).toBe('Read the term and its meaning. ');
  });
  it('preserves malformed input once instead of duplicating or discarding curriculum wording', () => {
    for (const text of ['Before [[unfinished', 'Before **unfinished', 'Invalid {{cite:no}} stays', 'Before *unfinished']) {
      expect(output(text).textContent).toBe(text);
    }
  });
  it('preserves the wording of every subject paragraph, bullet and commitment', () => {
    for (const module of Object.values(SUBJECT_MODULE_CONTENT)) {
      for (const section of module.sections) {
        const texts = [...section.paragraphs, ...(section.bullets ?? []), ...(section.commitmentText ? [section.commitmentText] : [])];
        for (const text of texts) {
          const plain = text.replace(/\{\{cite:[1-9]\d*\}\}/g, '').replace(/\*\*|\[\[|\]\]|\*/g, '');
          expect(output(text).textContent, `${module.moduleTitle}: ${text}`).toBe(plain);
        }
      }
    }
  });
});
