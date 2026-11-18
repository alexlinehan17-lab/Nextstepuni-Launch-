/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The printed options under a listening question (Irish Foundation: "Cá háit a bhfuil Breandán ina chónaí faoi
 * láthair?" then "Droichead Átha", "Dún Dealgan", "Faoin tuath"), one to a line as the paper sets them. The card's
 * question text keeps them after a blank line; run into the prompt they read as one sentence.
 */
import React from 'react';

/** A prompt's question and the options printed under it (none where the paper prints none). */
export const listeningPromptParts = (text: string): { question: string; options: string[] } => {
  const [question, ...rest] = text.split(/\n{2,}/);
  return { question: question.trim(), options: rest.join('\n').split('\n').map(line => line.trim()).filter(Boolean) };
};

const ListeningPromptOptions: React.FC<{ text: string }> = ({ text }) => {
  const { options } = listeningPromptParts(text);
  if (!options.length) return null;
  return (
    <span data-listening-options="" style={{ display: 'block', marginTop: 6 }}>
      {options.map((option, index) => <span key={`${option}-${index}`} style={{ display: 'block' }}>{option}</span>)}
    </span>
  );
};

export default ListeningPromptOptions;
