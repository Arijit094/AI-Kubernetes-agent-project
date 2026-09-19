"use client";

type Props = {
  onClick: () => void;
  isLoading: boolean;
};

export function InvestigateButton({ onClick, isLoading }: Props) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={isLoading}
      className="w-full rounded-xl bg-slate-900 px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:bg-slate-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
    >
      {isLoading ? (
        <>
          <span className="h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
          <span>Investigating Cluster...</span>
        </>
      ) : (
        <span>[ Investigate Cluster ]</span>
      )}
    </button>
  );
}
