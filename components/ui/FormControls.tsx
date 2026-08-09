import React from 'react';

export const FIELD_CLASS = 'product-field min-h-12 w-full rounded-xl border-[1.5px] border-[#383838] bg-white px-4 py-3 text-sm text-[#1A1A1A] placeholder:text-[#9B9188] shadow-[2px_2px_0_0_#383838] outline-none transition-[border-color,box-shadow,transform] focus:border-[#F26B1F] focus:shadow-[3px_3px_0_0_#383838] disabled:cursor-not-allowed disabled:opacity-50 dark:border-zinc-600 dark:bg-zinc-900 dark:text-zinc-100';

interface FieldShellProps {
  label: string;
  hint?: string;
  error?: string;
  children: React.ReactNode;
  className?: string;
}

export const FieldShell: React.FC<FieldShellProps> = ({ label, hint, error, children, className = '' }) => (
  <label className={`block ${className}`}>
    <span className="mb-2 block text-[10px] font-bold uppercase tracking-[0.16em] text-[#78716C] dark:text-zinc-400">{label}</span>
    {children}
    {(error || hint) && <span className={`mt-2 block text-xs leading-5 ${error ? 'font-semibold text-red-700 dark:text-red-300' : 'text-[#78716C] dark:text-zinc-400'}`}>{error ?? hint}</span>}
  </label>
);

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

