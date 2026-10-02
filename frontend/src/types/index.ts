/**
 * RouteFlow Core TypeScript Type Definitions
 */

export interface Location {
  latitude: number;
  longitude: number;
  address?: string;
  name?: string;
}

export interface DeliveryStop {
  id: string;
  location: Location;
  package_count: number;
  priority: number;
  notes?: string;
}

export interface AlgorithmMetadata {
  id: string;
  name: string;
  description: string;
  paradigm: string;
  time_complexity: string;
  is_exact: boolean;
  status: string;
}

export interface RouteMetrics {
  total_distance_km: number;
  estimated_duration_minutes: number;
  stop_count: number;
}

export interface OptimizationRequest {
  depot: Location;
  stops: DeliveryStop[];
  algorithm: string;
  parameters?: Record<string, unknown>;
}

export interface OptimizationResult {
  algorithm_used: string;
  ordered_stop_ids: string[];
  metrics: RouteMetrics;
  computation_time_ms: number;
  status: string;
  message?: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  timestamp: string;
}

export interface SystemStatusResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  uptime_seconds: number;
  available_algorithms: AlgorithmMetadata[];
  timestamp: string;
}
