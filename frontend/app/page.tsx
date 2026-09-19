import { InvestigateButton } from "@/components/InvestigateButton";
import { SystemStatus } from "@/components/SystemStatus";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <section className="w-full max-w-xl rounded-2xl border border-slate-200 bg-white p-10 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-wide text-slate-500">
          On-demand troubleshooting
        </p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">
          AI Kubernetes Agent
        </h1>
        <p className="mt-3 text-lg text-slate-600">
          Troubleshoot Kubernetes with AI
        </p>
        <div className="mt-8 flex flex-col gap-6">
          <InvestigateButton />
          <SystemStatus />
        </div>
      </section>
    </main>
  );
}
