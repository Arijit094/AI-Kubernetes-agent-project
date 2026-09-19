import { api } from "./api";
import { InvestigateResponse } from "@/types/api";

export async function investigateCluster(): Promise<InvestigateResponse> {
  const response = await api.post<InvestigateResponse>("/investigate");
  return response.data;
}
