import type {ComponentProps,ReactNode} from 'react';
export function InputOTP(props: Omit<ComponentProps<'input'>,'onChange'|'children'|'value'> & {maxLength:number;value?:string;onChange?:(value:string)=>void;children?:ReactNode;containerClassName?:string;success?:boolean}): ReactNode;
export function InputOTPGroup(props:ComponentProps<'div'>):ReactNode;
export function InputOTPSlot(props:ComponentProps<'div'> & {index:number}):ReactNode;
export function InputOTPSeparator(props:ComponentProps<'div'>):ReactNode;
