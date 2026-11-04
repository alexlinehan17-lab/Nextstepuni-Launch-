// Generated declarations for the compiled control runtime.
import { type ReactNode } from 'react';
export type PlanStep = {
    label: string;
    done?: boolean;
};
export declare function PlanCard({ icon, title, description, steps, visibleSteps, autoApproveIn, onApprove, onAutoApprove, onCancelAutoApprove, onView, onDownload, onExpand, approveDisabled, approveLabel, viewLabel, className, }: {
    icon?: ReactNode;
    title: string;
    description?: ReactNode;
    steps: Array<PlanStep>;
    visibleSteps?: number;
    autoApproveIn?: number;
    onApprove?: () => void;
    onAutoApprove?: () => void;
    onCancelAutoApprove?: () => void;
    onView?: () => void;
    onDownload?: () => void;
    onExpand?: () => void;
    approveDisabled?: boolean;
    approveLabel?: string;
    viewLabel?: string;
    className?: string;
}): import("react").JSX.Element;
