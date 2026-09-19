"use client";

import { Diagnosis } from "@/types/api";
import { useState } from "react";

type Props = {
  diagnosis: Diagnosis;
};

export function DiagnosisCard({ diagnosis }: Props) {
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(diagnosis.kubectl_command);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 pb-4">
        <h2 className="text-lg font-semibold text-slate-900">Diagnosis & Fix</h2>
        <div className="flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
          <span>Confidence: {diagnosis.confidence}%</span>
        </div>
      </div>

      <div className="mt-5 space-y-4 text-sm">
        <div>
          <span className="font-semibold text-slate-700">Root Cause:</span>
          <p className="mt-1 font-medium text-rose-700 bg-rose-50 rounded-lg p-3 border border-rose-100">
            {diagnosis.root_cause}
          </p>
        </div>

        <div>
          <span className="font-semibold text-slate-700">Explanation:</span>
          <p className="mt-1 text-slate-600 leading-relaxed">
            {diagnosis.explanation}
          </p>
        </div>

        <div>
          <span className="font-semibold text-slate-700">Suggested Fix:</span>
          <p className="mt-1 text-slate-700 bg-slate-50 rounded-lg p-3 border border-slate-200">
            {diagnosis.fix}
          </p>
        </div>

        <div>
          <div className="flex items-center justify-between">
            <span className="font-semibold text-slate-700">kubectl Command:</span>
            <button
              type="button"
              onClick={handleCopy}
              className="text-xs font-medium text-indigo-600 hover:text-indigo-800"
            >
              {copied ? "Copied!" : "Copy command"}
            </button>
          </div>
          <pre className="mt-1 overflow-x-auto rounded-lg bg-slate-900 p-3 text-xs font-mono text-emerald-400">
            <code>{diagnosis.kubectl_command}</code>
          </pre>
        </div>

        {diagnosis.prevention && (
          <div>
            <span className="font-semibold text-slate-700">Prevention:</span>
            <p className="mt-1 text-slate-600 text-xs bg-slate-50 rounded-lg p-3">
              {diagnosis.prevention}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
