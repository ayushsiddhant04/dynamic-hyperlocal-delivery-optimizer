import {
  HealthResponse,
  OptimizationRequest,
  OptimizationResult,
  SystemStatusResponse,
} from "@/types";

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
    throw new Error(
      `Health probe failed with status ${response.status}: ${response.statusText}`
    );
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
    throw new Error(
      `Status probe failed with status ${response.status}: ${response.statusText}`
    );
  }

  return response.json();
}

/**
 * Send a dynamically generated delivery trip to the backend
 * for route optimization.
 */
export async function optimizeRoute(
  request: OptimizationRequest
): Promise<OptimizationResult> {
  const response = await fetch(`${API_BASE_URL}/api/optimize`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
    cache: "no-store",
  });

  if (!response.ok) {
    let errorMessage = `Route optimization failed with status ${response.status}: ${response.statusText}`;

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      } else if (
        errorData.detail &&
        typeof errorData.detail.message === "string"
      ) {
        errorMessage = errorData.detail.message;
      }
    } catch {
      // Keep the default error message if the response is not JSON.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}

export { API_BASE_URL };