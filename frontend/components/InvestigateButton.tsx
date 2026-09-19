"use client";

export function InvestigateButton() {
  function handleClick() {
    // Investigation API will be wired in a later phase.
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className="w-full rounded-lg bg-slate-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800"
    >
      Investigate Cluster
    </button>
  );
}
