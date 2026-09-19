"use client";

import { useHealth } from "@/hooks/useHealth";

export function SystemStatus() {
  const { data, isLoading, isError } = useHealth();

  let label = "Checking...";
  let color = "bg-slate-400";

  if (isLoading) {
    label = "Checking...";
  } else if (data?.status === "healthy") {
    label = "Ready";
    color = "bg-emerald-500";
  } else if (isError) {
    label = "Backend unavailable";
    color = "bg-amber-500";
  } else {
    label = "Unknown";
  }

  return (
    <div className="flex items-center gap-2 text-sm text-slate-600">
      <span className={`h-2.5 w-2.5 rounded-full ${color}`} aria-hidden="true" />
      <span>System Status: {label}</span>
    </div>
  );
}
