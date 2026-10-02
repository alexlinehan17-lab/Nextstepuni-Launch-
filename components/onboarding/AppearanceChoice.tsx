import React, { useId } from "react";
import { ArrowUpRight, Check } from "lucide-react";
import "./appearance.css";

export interface AppearanceChoiceProps {
  darkMode: boolean;
  onChange: (darkMode: boolean) => void;
  disabled?: boolean;
}

export default function AppearanceChoice({ darkMode, onChange, disabled }: AppearanceChoiceProps) {
  const id = useId();
  return (
    <fieldset className="setup-appearance" disabled={disabled} aria-describedby={`${id}-help`}>
      <legend>Choose your view.</legend>
      <p>How would you like NextStepUni to look?</p>
      <div className="setup-appearance-options">
        {[{ dark: true, label: "Dark" }, { dark: false, label: "Light" }].map(option => (
          <label className="setup-appearance-card" key={option.label} data-selected={darkMode === option.dark}>
            <input
              type="radio"
              name={`${id}-appearance`}
              value={option.dark ? "dark" : "light"}
              checked={darkMode === option.dark}
              onChange={() => onChange(option.dark)}
            />
            <div className="setup-appearance-preview" data-mode={option.dark ? "dark" : "light"} aria-hidden="true">
              <div className="setup-appearance-mini-nav"><b>nextstepuni</b><i /></div>
              <div className="setup-appearance-mini-content">
                <small>YOUR NEXT STEP</small>
                <strong>Make a little<br />room for study.</strong>
                <div className="setup-appearance-mini-subjects"><span>Mathematics</span><i /><span>English</span><i /></div>
                <div className="setup-appearance-mini-action">Start studying <ArrowUpRight size={12} /></div>
              </div>
            </div>
            <span className="setup-appearance-name"><span>{option.label}</span><i aria-hidden="true">{darkMode === option.dark && <Check size={13} />}</i></span>
          </label>
        ))}
      </div>
      <p id={`${id}-help`} className="setup-appearance-help">You can change this anytime in Settings.</p>
    </fieldset>
  );
}
