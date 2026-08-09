import React from 'react';
import { ArrowRight, Flame } from 'lucide-react';
import { CelebrationFrame, MilestoneBadge } from './ui/Celebration';

interface StreakCelebrationProps {
  streakCount: number;
  isOpen: boolean;
  onDismiss: () => void;
  weekDays: boolean[];
}

const MILESTONE_MESSAGES: Record<number, string> = {
  3: "Three days in. You're building something.",
  7: "A full week. That's not luck — that's discipline.",
  14: 'Two weeks strong. The routine is beginning to hold.',
  21: 'Three weeks. Showing up is becoming part of how you work.',
  30: "A month. You're not the same student you were 30 days ago.",
  50: 'Fifty days. This is a serious body of work.',
  100: 'One hundred days. Extraordinary consistency.',
};

const DAY_LABELS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

const StreakCelebration: React.FC<StreakCelebrationProps> = ({ streakCount, isOpen, onDismiss, weekDays }) => (
  <CelebrationFrame isOpen={isOpen} ariaLabel={`${streakCount}-day streak`} onDismiss={onDismiss} scale="medium">
    <div className="text-center">
      <MilestoneBadge><Flame size={12} /> Streak milestone</MilestoneBadge>
      <div className="mx-auto mt-7 flex h-28 w-28 items-center justify-center rounded-full border-2 border-[#383838] bg-[#FFF0E7] shadow-[5px_5px_0_0_#383838]">
        <span className="font-serif text-6xl font-semibold tracking-[-0.05em] text-[#F26B1F]">{streakCount}</span>
      </div>
      <h1 className="mt-6 font-serif text-3xl font-semibold text-[#1A1A1A]">days, one line of effort.</h1>
      <p className="mx-auto mt-2 max-w-sm text-sm leading-6 text-[#78716C]">{MILESTONE_MESSAGES[streakCount] ?? `${streakCount} days. Keep the momentum going.`}</p>

      <div className="mt-7 grid grid-cols-7 gap-1.5 rounded-2xl border border-[#D8D3CD] bg-white p-3 sm:gap-2">
        {DAY_LABELS.map((day, index) => (
          <div key={`${day}-${index}`} className="flex min-w-0 flex-col items-center gap-1.5">
            <span className={`flex aspect-square w-full max-w-9 items-center justify-center rounded-lg border ${weekDays[index] ? 'border-[#383838] bg-[#F26B1F] text-white' : 'border-[#E4E0DA] bg-[#F4F2EE] text-[#AAA29A]'}`}>
              {weekDays[index] ? <Flame size={14} /> : null}
            </span>
            <span className={`text-[9px] font-bold ${weekDays[index] ? 'text-[#A53E0C]' : 'text-[#AAA29A]'}`}>{day}</span>
          </div>
        ))}
      </div>

      <button onClick={onDismiss} className="mt-7 inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-xl border-2 border-[#1A1A1A] bg-[#F26B1F] px-6 font-bold text-white shadow-[4px_4px_0_0_#1A1A1A] transition-transform hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-none">
        Keep going <ArrowRight size={18} />
      </button>
    </div>
  </CelebrationFrame>
);

export default StreakCelebration;
