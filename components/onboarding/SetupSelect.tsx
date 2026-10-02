import React from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectSeparator,
  SelectTrigger,
  SelectValue,
} from "../approved-ui-runtime";
import "../approved-ui-runtime.css";
import "../approved-ui-theme.css";
import "./setup-select.css";

interface Props {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string }[];
  placeholder: string;
  disabled?: boolean;
}

export default function SetupSelect({ label, value, onChange, options, placeholder, disabled }: Props) {
  return (
    <div className="nsu-kobra setup-select-scope">
      <Select
        value={value || null}
        items={options}
        disabled={disabled}
        onValueChange={next => { if (next !== null) onChange(next); }}
      >
        <SelectTrigger className="setup-select-trigger" aria-label={label}>
          <SelectValue placeholder={placeholder} />
        </SelectTrigger>
        <SelectContent className="setup-select-menu" align="start" sideOffset={6} alignItemWithTrigger={false}>
          {options.map(option => (
            <React.Fragment key={option.value}>
              {option.value === "later" && <SelectSeparator />}
              <SelectItem value={option.value}>{option.label}</SelectItem>
            </React.Fragment>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
