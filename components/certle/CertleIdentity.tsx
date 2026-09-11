import React from "react";
import { Check } from "lucide-react";
import { MAX_ATTEMPTS } from "./data";
import type { resultsFor } from "./game";

export function CertleLogo() {
  return (
    <span className="certle-logo" aria-hidden="true">
      {"CERTLE".split("").map((letter, i) => (
        <span className={`certle-letter certle-letter-${i}`} key={i}>
          {letter}
        </span>
      ))}
    </span>
  );
}

export function MarksBoard({
  results,
  total,
  current,
  finished = false,
}: {
  results: ReturnType<typeof resultsFor>;
  total: number;
  current: number;
  finished?: boolean;
}) {
  return (
    <div
      className="certle-attempts"
      aria-label="Your attempts"
      data-dense={total > 10}
    >
      {Array.from({ length: MAX_ATTEMPTS }, (_, i) => {
        const result = results[i];
        const cells = result
          ? result.hits.flatMap((hit) =>
              Array.from({ length: hit.marks }, () => hit.matched),
            )
          : Array.from({ length: total }, () => false);
        return (
          <div
            key={i}
            className={`certle-attempt${result ? " is-played" : ""}${!finished && i === current ? " is-current" : ""}`}
            aria-label={`Attempt ${i + 1}: ${result ? `${result.earned} of ${result.total} marks` : "not played"}`}
          >
            <span className="certle-attempt-number">0{i + 1}</span>
            <div
              className="certle-squares"
              style={{ "--marks": total } as React.CSSProperties}
            >
              {cells.map((hit, j) => (
                <span
                  key={`${!!result}-${j}`}
                  aria-hidden="true"
                  style={
                    { "--tile-delay": `${j * 35}ms` } as React.CSSProperties
                  }
                  className={hit ? "is-earned" : result ? "is-unmatched" : ""}
                >
                  {hit ? (
                    <Check size={15} strokeWidth={2.5} />
                  ) : result ? (
                    <span className="certle-miss">·</span>
                  ) : null}
                </span>
              ))}
            </div>
            <span className="certle-attempt-score">
              {result ? `${result.earned}/${result.total}` : "—"}
            </span>
          </div>
        );
      })}
    </div>
  );
}
