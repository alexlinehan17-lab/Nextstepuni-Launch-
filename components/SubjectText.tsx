import React from 'react';
import { Highlight } from './ModuleShared';
import { Cite } from './ModuleReferences';
import type { ModuleTheme } from '../types';
import type { SubjectHighlight } from '../subjectModuleData';

/** The curriculum's inline notation, with nested bold/italic/highlight support.
 * Malformed notation stays visible once; source wording is never interpreted as HTML. */
export function renderSubjectText(text: string, highlights: SubjectHighlight[], theme: ModuleTheme): React.ReactNode {
  function read(start: number, closing?: string): { nodes: React.ReactNode[]; end: number; closed: boolean } {
    const nodes: React.ReactNode[] = [];
    let position = start;
    let plainStart = start;
    const flush = () => { if (position > plainStart) nodes.push(text.slice(plainStart, position)); };
    while (position < text.length) {
      const rest = text.slice(position);
      // In *** the innermost italic closes first, leaving ** for its parent.
      if (closing && rest.startsWith(closing) && (closing !== '*' || !rest.startsWith('**') || rest.startsWith('***'))) {
        flush();
        return { nodes, end: position + closing.length, closed: true };
      }
      const citation = rest.match(/^\{\{cite:([1-9]\d*)\}\}/);
      if (citation) {
        flush();
        nodes.push(<Cite key={position} n={Number(citation[1])} />);
        position += citation[0].length;
        plainStart = position;
        continue;
      }
      const opener = rest.startsWith('[[') ? '[[' : rest.startsWith('**') ? '**' : rest.startsWith('*') ? '*' : null;
      if (opener) {
        const child = read(position + opener.length, opener === '[[' ? ']]' : opener);
        if (child.closed) {
          flush();
          if (opener === '**') nodes.push(<strong key={position}>{child.nodes}</strong>);
          else if (opener === '*') nodes.push(<em key={position}>{child.nodes}</em>);
          else {
            const term = text.slice(position + 2, child.end - 2);
            const highlight = highlights.find(item => item.term === term);
            nodes.push(highlight?.description
              ? <Highlight key={position} description={highlight.description} theme={theme}>{child.nodes}</Highlight>
              : <strong key={position}>{child.nodes}</strong>);
          }
          position = child.end;
          plainStart = position;
          continue;
        }
        // Consume the whole unmatched opener so ** cannot become an empty italic.
        position += opener.length;
      } else position++;
    }
    flush();
    return { nodes, end: position, closed: false };
  }
  return <>{read(0).nodes}</>;
}
