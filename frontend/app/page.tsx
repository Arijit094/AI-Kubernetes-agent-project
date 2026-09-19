"use client";

import { useState } from "react";
import { InvestigateButton } from "@/components/InvestigateButton";
import { SystemStatus } from "@/components/SystemStatus";
import { InvestigationProgress } from "@/components/InvestigationProgress";
import { DiagnosisCard } from "@/components/DiagnosisCard";
import { InvestigationHistory } from "@/components/InvestigationHistory";
import { investigateCluster } from "@/services/investigation";
import { Diagnosis, InvestigationHistoryItem } from "@/types/api";

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [history, setHistory] = useState<InvestigationHistoryItem[]>([]);

  async function handleInvestigate() {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const response = await investigateCluster();
      const diag = response.diagnosis;
      setDiagnosis(diag);

      // Add to history
      const newItem: InvestigationHistoryItem = {
        id: Date.now().toString(),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        rootCause: diag.root_cause || "Investigation complete",
        status: "Completed",
        confidence: diag.confidence || 90,
      };
      setHistory((prev) => [newItem, ...prev.slice(0, 4)]);
    } catch (err: any) {
      console.error("Investigation failed:", err);
      setErrorMessage(
        err.response?.data?.detail ||
          err.message ||
          "Failed to connect to backend cluster investigation service."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 py-12 px-6">
      <div className="mx-auto max-w-2xl space-y-8">
        {/* Header & Main Card */}
        <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              On-demand troubleshooting
            </p>
            <SystemStatus />
          </div>

          <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">
            AI Kubernetes Agent
          </h1>
          <p className="mt-2 text-base text-slate-600">
            Troubleshoot Kubernetes with AI
          </p>

          <div className="mt-8 space-y-6">
            <InvestigateButton onClick={handleInvestigate} isLoading={isLoading} />
            <InvestigationProgress isLoading={isLoading} />
          </div>

          {errorMessage && (
            <div className="mt-6 rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">
              <span className="font-semibold">Investigation Error:</span> {errorMessage}
            </div>
          )}
        </section>

        {/* Diagnosis Result */}
        {diagnosis && <DiagnosisCard diagnosis={diagnosis} />}

        {/* Investigation History */}
        <InvestigationHistory history={history} />
      </div>
    </main>
  );
}
