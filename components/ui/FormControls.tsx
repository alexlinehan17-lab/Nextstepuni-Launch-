import React from 'react';

import './controls.css';
export const FIELD_CLASS = 'product-field placeholder:text-[#9B9188] disabled:cursor-not-allowed disabled:opacity-50';

interface FieldShellProps {
  label: string;
  htmlFor?: string;
  hintId?: string;
  errorId?: string;
  hint?: string;
  error?: string;
  children: React.ReactElement<React.InputHTMLAttributes<HTMLInputElement>>;
  className?: string;
}

/** Wires the visible label and messages to its control before wider adoption. */
export const FieldShell: React.FC<FieldShellProps> = ({ label, htmlFor, hintId, errorId, hint, error, children, className = '' }) => {
  const generatedId = React.useId();
  const id = htmlFor ?? children.props.id ?? generatedId;
  const hintKey = hintId ?? `${id}-hint`;
  const errorKey = errorId ?? `${id}-error`;
  const describedBy = [children.props['aria-describedby'], hint && hintKey, error && errorKey].filter(Boolean).join(' ') || undefined;
  return <div className={className}>
    <label htmlFor={id} className="mb-2 block text-[10px] font-bold uppercase tracking-[0.16em] text-[#78716C] dark:text-zinc-400">{label}</label>
    {React.cloneElement(children, { id, 'aria-invalid': error ? true : children.props['aria-invalid'], 'aria-describedby': describedBy })}
    {hint && <span id={hintKey} className="product-field-message">{hint}</span>}
    {error && <span id={errorKey} className="product-field-message" role="alert">{error}</span>}
  </div>;
};

export const TextField = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(({ className = '', ...props }, ref) => (
  <input ref={ref} className={`${FIELD_CLASS} ${className}`} {...props} />
));
TextField.displayName = 'TextField';

export const TextAreaField = React.forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(({ className = '', ...props }, ref) => (
  <textarea ref={ref} className={`${FIELD_CLASS} min-h-28 resize-y ${className}`} {...props} />
));
TextAreaField.displayName = 'TextAreaField';

export const SelectField = React.forwardRef<HTMLSelectElement, React.SelectHTMLAttributes<HTMLSelectElement>>(({ className = '', ...props }, ref) => (
  <select ref={ref} className={`${FIELD_CLASS} appearance-none ${className}`} {...props} />
));
SelectField.displayName = 'SelectField';

