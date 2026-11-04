import { useId, useState } from 'react';
import './french-rubric.css';

/** A paper-side selection only. Scoring remains behind the scheme reveal. */
export default function FrenchQuestionChoices({ options }: { options: string[] }) {
  const group = useId();
  const [selected, setSelected] = useState<number | null>(null);
  return <fieldset className="mb-french-choices">
    <legend>Select one answer</legend>
    {options.map((option, index) => <label key={option} className="mb-french-choice" data-selected={selected === index}>
      <input type="radio" name={group} value={index} checked={selected === index} onChange={() => setSelected(index)} />
      <span>{option}</span>
    </label>)}
  </fieldset>;
}
