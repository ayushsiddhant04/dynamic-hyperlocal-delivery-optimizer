import { HealthResponse, SystemStatusResponse } from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Fetch health liveness probe from FastAPI backend.
 */
export async function getBackendHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/health`, {
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Health probe failed with status ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch detailed system diagnostics from FastAPI backend.
 */
export async function getBackendStatus(): Promise<SystemStatusResponse> {
  const response = await fetch(`${API_BASE_URL}/api/status`, {
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Status probe failed with status ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

export { API_BASE_URL };
