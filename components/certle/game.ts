import { markAnswer, type MarkResult } from "../landing/marking/marker";
import { dayBefore } from "../landing/fx-e/dublin";
import { MAX_ATTEMPTS, schemePoints, type CertleQuestion } from "./data";

export const GAME_KEY = "nextstepuni.certle.v2";
export const STATS_KEY = "nextstepuni.certle.stats.v1";
export interface Game {
  version: 2;
  day: string;
  id: string;
  answers: string[];
  finished: boolean;
}
export interface DayScore {
  day: string;
  id: string;
  earned: number;
  total: number;
  attempts: number;
  complete: boolean;
}
export interface Stats {
  results: DayScore[];
}
export const readStored = <T>(key: string): T | null => {
  try {
    return JSON.parse(localStorage.getItem(key) ?? "null") as T | null;
  } catch {
    return null;
  }
};
export const saveStored = (key: string, value: unknown): boolean => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
};
export const emptyGame = (day: string, id: string): Game => ({
  version: 2,
  day,
  id,
  answers: [],
  finished: false,
});
export function restoreGame(day: string, question: CertleQuestion): Game {
  const saved = readStored<Game>(GAME_KEY);
  if (
    saved?.version === 2 &&
    saved.day === day &&
    saved.id === question.id &&
    Array.isArray(saved.answers) &&
    saved.answers.every((a) => typeof a === "string" && a.length <= 3000)
  ) {
    const answers = saved.answers.slice(0, MAX_ATTEMPTS);
    return {
      ...emptyGame(day, question.id),
      answers,
      finished:
        !!saved.finished ||
        answers.length >= MAX_ATTEMPTS ||
        answers.some((a) => {
          const r = markAnswer(a, schemePoints(question));
          return r.earned === r.total;
        }),
    };
  }
  // Earlier visitors have already seen the solution: retain their answer and
  // final result, rather than offering fresh attempts at a revealed question.
  const old = readStored<{ day: string; id: string; answer: string }>(
    "landing.today.v1",
  );
  if (
    old?.day === day &&
    old.id === question.id &&
    typeof old.answer === "string" &&
    old.answer.trim()
  )
    return {
      ...emptyGame(day, question.id),
      answers: [old.answer],
      finished: true,
    };
  return emptyGame(day, question.id);
}
export function resultsFor(game: Game, question: CertleQuestion): MarkResult[] {
  return game.answers.map((answer) =>
    markAnswer(answer, schemePoints(question)),
  );
}
export function bestResult(results: MarkResult[]): MarkResult | undefined {
  return results.reduce<MarkResult | undefined>(
    (best, r) => (!best || r.earned > best.earned ? r : best),
    undefined,
  );
}
export function submitAnswer(
  game: Game,
  question: CertleQuestion,
  answer: string,
): Game {
  const clean = answer.trim().slice(0, 3000);
  if (
    game.finished ||
    !clean ||
    game.answers.length >= MAX_ATTEMPTS ||
    game.answers.some((a) => a.trim().toLowerCase() === clean.toLowerCase())
  )
    return game;
  const result = markAnswer(clean, schemePoints(question));
  return {
    ...game,
    answers: [...game.answers, clean],
    finished:
      result.earned === result.total || game.answers.length + 1 >= MAX_ATTEMPTS,
  };
}
export function recordResult(
  stats: Stats,
  game: Game,
  question: CertleQuestion,
): Stats {
  const best = bestResult(resultsFor(game, question));
  if (!best || !game.finished) return stats;
  const next: DayScore = {
    day: game.day,
    id: game.id,
    earned: best.earned,
    total: best.total,
    attempts: game.answers.length,
    complete: best.earned === best.total,
  };
  return {
    results: [...stats.results.filter((r) => r.day !== game.day), next].sort(
      (a, b) => a.day.localeCompare(b.day),
    ),
  };
}
export function loadStats(): Stats {
  const saved = readStored<Stats>(STATS_KEY);
  return {
    results: Array.isArray(saved?.results)
      ? saved.results.filter(
          (r) =>
            r &&
            /^\d{4}-\d{2}-\d{2}$/.test(r.day) &&
            Number.isFinite(r.earned) &&
            r.total > 0 &&
            r.earned >= 0 &&
            r.earned <= r.total &&
            r.attempts >= 1 &&
            r.attempts <= MAX_ATTEMPTS,
        )
      : [],
  };
}
export function statsSummary(stats: Stats, today: string) {
  const dates = new Set(stats.results.map((r) => r.day));
  let day = dates.has(today) ? today : dayBefore(today),
    streak = 0;
  while (dates.has(day)) {
    streak++;
    day = dayBefore(day);
  }
  const completed = stats.results.filter((r) => r.complete).length;
  return {
    played: stats.results.length,
    fullMarks: completed,
    streak,
    winRate: stats.results.length
      ? Math.round((completed / stats.results.length) * 100)
      : 0,
  };
}
export function shareText(
  n: number,
  game: Game,
  question: CertleQuestion,
  origin: string,
): string {
  const results = resultsFor(game, question),
    best = bestResult(results);
  return [
    `CERTLE #${n} · ${question.subject}`,
    `${best?.earned ?? 0}/${best?.total ?? 0} marks · ${game.answers.length}/${MAX_ATTEMPTS} attempts`,
    ...results.map((r) =>
      r.hits
        .flatMap((h) =>
          Array.from({ length: h.marks }, () => (h.matched ? "🟧" : "⬜")),
        )
        .join(""),
    ),
    `${origin}/certle`,
  ].join("\n");
}
