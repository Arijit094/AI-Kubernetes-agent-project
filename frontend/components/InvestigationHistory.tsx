"use client";

import { InvestigationHistoryItem } from "@/types/api";

type Props = {
  history: InvestigationHistoryItem[];
  onSelect?: (item: InvestigationHistoryItem) => void;
};

export function InvestigationHistory({ history }: Props) {
  if (history.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-base font-semibold text-slate-900">Recent Investigations</h2>
      <div className="mt-4 divide-y divide-slate-100">
        {history.map((item) => (
          <div key={item.id} className="py-3 flex items-center justify-between text-sm">
            <div>
              <p className="font-medium text-slate-800">{item.rootCause}</p>
              <p className="text-xs text-slate-400">{item.timestamp}</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600">
                {item.confidence}% confidence
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
