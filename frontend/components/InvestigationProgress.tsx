"use client";

import { useEffect, useState } from "react";

type Props = {
  isLoading: boolean;
  onComplete?: () => void;
};

const STEPS = [
  "Checking Pods",
  "Reading Logs",
  "Analyzing Events",
  "Inspecting Deployments",
  "Checking Networking",
  "AI Reasoning",
  "Root Cause Found",
];

export function InvestigationProgress({ isLoading }: Props) {
  const [currentStepIndex, setCurrentStepIndex] = useState(-1);

  useEffect(() => {
    if (!isLoading) {
      setCurrentStepIndex(STEPS.length - 1);
      return;
    }

    setCurrentStepIndex(0);
    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev < STEPS.length - 2) {
          return prev + 1;
        }
        return prev;
      });
    }, 400);

    return () => clearInterval(interval);
  }, [isLoading]);

  if (!isLoading && currentStepIndex === -1) {
    return null;
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">
      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-500">
        Investigation Progress
      </h3>
      <ul className="mt-3 space-y-2">
        {STEPS.map((step, idx) => {
          const isDone = !isLoading || idx <= currentStepIndex;
          const isCurrent = isLoading && idx === currentStepIndex;

          return (
            <li key={step} className="flex items-center gap-3 text-sm">
              <span
                className={`flex h-5 w-5 items-center justify-center rounded-full text-xs font-medium ${
                  isDone
                    ? "bg-emerald-100 text-emerald-700"
                    : isCurrent
                    ? "bg-amber-100 text-amber-700 animate-pulse"
                    : "bg-slate-200 text-slate-400"
                }`}
              >
                {isDone ? "✓" : idx + 1}
              </span>
              <span
                className={
                  isDone
                    ? "font-medium text-slate-900"
                    : isCurrent
                    ? "font-medium text-amber-800"
                    : "text-slate-400"
                }
              >
                {step}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
