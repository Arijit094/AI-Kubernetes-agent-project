export type HealthResponse = {
  status: string;
  service: string;
};

export type Diagnosis = {
  root_cause: string;
  explanation: string;
  fix: string;
  kubectl_command: string;
  confidence: number;
  prevention?: string;
};

export type InvestigationResult = {
  pods?: Record<string, any>;
  logs?: Record<string, any>;
  events?: Record<string, any>;
  deployments?: Record<string, any>;
  network?: Record<string, any>;
};

export type InvestigateResponse = {
  status: string;
  investigation: InvestigationResult;
  diagnosis: Diagnosis;
};

export type InvestigationHistoryItem = {
  id: string;
  timestamp: string;
  rootCause: string;
  status: string;
  confidence: number;
};
