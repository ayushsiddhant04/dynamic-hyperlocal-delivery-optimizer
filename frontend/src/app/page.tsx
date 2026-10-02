"use client";

import { useEffect, useState, useCallback } from "react";
import { getBackendHealth, getBackendStatus, API_BASE_URL } from "@/lib/api";
import { HealthResponse, SystemStatusResponse } from "@/types";

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [status, setStatus] = useState<SystemStatusResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastChecked, setLastChecked] = useState<string>("");

  const fetchStatusData = useCallback(async () => {
    try {
      const [healthData, statusData] = await Promise.all([
        getBackendHealth(),
        getBackendStatus(),
      ]);
      setHealth(healthData);
      setStatus(statusData);
      setError(null);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Failed to connect to backend server";
      setError(message);
      setHealth(null);
      setStatus(null);
      setLastChecked(new Date().toLocaleTimeString());
    } finally {
      setLoading(false);
    }
  }, []);

  const handleManualRefresh = async () => {
    setLoading(true);
    await fetchStatusData();
  };

  useEffect(() => {
    let ignore = false;
    async function init() {
      try {
        const [healthData, statusData] = await Promise.all([
          getBackendHealth(),
          getBackendStatus(),
        ]);
        if (!ignore) {
          setHealth(healthData);
          setStatus(statusData);
          setError(null);
          setLastChecked(new Date().toLocaleTimeString());
        }
      } catch (err: unknown) {
        if (!ignore) {
          const message =
            err instanceof Error ? err.message : "Failed to connect to backend server";
          setError(message);
          setHealth(null);
          setStatus(null);
          setLastChecked(new Date().toLocaleTimeString());
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }
    init();
    return () => {
      ignore = true;
    };
  }, []);

  return (
    <main className="page-container">
      {/* Header */}
      <section className="hero-section">
        <div className="brand-badge">
          <span className="brand-badge-pulse" />
          Foundation Architecture &bull; Step 1
        </div>
        <h1 className="hero-title">
          Route<span className="hero-gradient-text">Flow</span>
        </h1>
        <p className="hero-description">
          Dynamic Hyperlocal Delivery Optimizer &bull; Foundation Layer
        </p>
      </section>

      {/* Backend Status & Health Diagnostic */}
      <section>
        <div className="section-title-wrap">
          <h2 className="section-title">
            <span>⚡</span> Backend Connectivity Status
          </h2>
          <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
            {lastChecked && (
              <span className="section-subtitle">
                Last checked: {lastChecked}
              </span>
            )}
            <button
              onClick={handleManualRefresh}
              disabled={loading}
              className="btn-secondary"
              style={{ padding: "0.4rem 0.85rem", fontSize: "0.82rem" }}
            >
              {loading ? "Checking..." : "↻ Test Connection"}
            </button>
          </div>
        </div>

        <div className="status-banner">
          {/* Health Endpoint Card */}
          <div
            className="status-card"
            style={{ "--card-accent": health ? "#10b981" : "#f43f5e" } as React.CSSProperties}
          >
            <div className="card-header">
              <span className="card-label">Health Check (/api/health)</span>
              <span
                className={`status-pill ${
                  loading ? "checking" : health ? "operational" : "offline"
                }`}
              >
                {loading ? "Checking" : health ? "Healthy" : "Offline"}
              </span>
            </div>
            <div className="card-value">
              {loading ? "Probing..." : health ? health.status.toUpperCase() : "Unreachable"}
            </div>
            <div className="card-subtext">
              Service: <span className="code-pill">{health?.service || "routeflow-backend"}</span>
              {health?.timestamp && (
                <div style={{ fontSize: "0.75rem", marginTop: "0.3rem" }}>
                  Server time: {health.timestamp}
                </div>
              )}
            </div>
          </div>

          {/* System Status Endpoint Card */}
          <div
            className="status-card"
            style={{ "--card-accent": status ? "#6366f1" : "#f43f5e" } as React.CSSProperties}
          >
            <div className="card-header">
              <span className="card-label">System Status (/api/status)</span>
              <span
                className={`status-pill ${
                  loading ? "checking" : status ? "operational" : "offline"
                }`}
              >
                {loading ? "Checking" : status ? "Operational" : "Offline"}
              </span>
            </div>
            <div className="card-value">
              {status ? `v${status.version}` : loading ? "..." : "Offline"}
            </div>
            <div className="card-subtext">
              Target URL: <span className="code-pill">{API_BASE_URL}</span>
              {status && (
                <div style={{ fontSize: "0.75rem", marginTop: "0.3rem" }}>
                  Uptime: {status.uptime_seconds}s | Env: {status.environment}
                </div>
              )}
            </div>
          </div>

          {/* Algorithm Modules Card */}
          <div
            className="status-card"
            style={{ "--card-accent": "#a855f7" } as React.CSSProperties}
          >
            <div className="card-header">
              <span className="card-label">Algorithm Registry</span>
              <span className="status-pill operational">
                {status?.available_algorithms.length ?? 0} Registered
              </span>
            </div>
            <div className="card-value">
              {status?.available_algorithms.length ?? 0} Solvers Ready
            </div>
            <div className="card-subtext">
              Extensible BaseRouteOptimizer interface
            </div>
          </div>
        </div>

        {error && (
          <div
            style={{
              marginTop: "1.25rem",
              padding: "1rem 1.25rem",
              background: "rgba(244, 63, 94, 0.1)",
              border: "1px solid rgba(244, 63, 94, 0.3)",
              borderRadius: "var(--radius-sm)",
              color: "#fca5a5",
              fontSize: "0.9rem",
            }}
          >
            <strong>Backend Connection Notice:</strong> {error}. Ensure FastAPI is running on{" "}
            <code>{API_BASE_URL}</code>.
          </div>
        )}
      </section>

      {/* Registered Algorithm Interfaces */}
      {status && status.available_algorithms.length > 0 && (
        <section>
          <div className="section-title-wrap">
            <div>
              <h2 className="section-title">
                <span>📐</span> Registered Optimization Algorithms
              </h2>
              <p className="section-subtitle">
                Algorithm modules registered in the backend engine via BaseRouteOptimizer.
              </p>
            </div>
          </div>

          <div className="grid-4">
            {status.available_algorithms.map((algo) => (
              <div key={algo.id} className="module-card">
                <div className="module-header">
                  <span className="module-name">{algo.name}</span>
                  <span className="module-badge">{algo.paradigm}</span>
                </div>
                <p className="module-desc">{algo.description}</p>
                <div className="module-meta">
                  <span>Complexity:</span>
                  <span className="module-complexity">{algo.time_complexity}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Foundation Verification Summary */}
      <section className="checklist-card">
        <h2 className="section-title" style={{ fontSize: "1.2rem" }}>
          <span>🏛️</span> Foundation Verification
        </h2>
        <ul className="checklist-items">
          <li className="checklist-item">
            <span className="checklist-icon done">✓</span>
            <div>
              <strong>Frontend Setup</strong>
              <p style={{ fontSize: "0.85rem", color: "var(--text-dim)", marginTop: "2px" }}>
                Next.js App Router, TypeScript, Vanilla CSS design tokens, typed API client.
              </p>
            </div>
          </li>
          <li className="checklist-item">
            <span className="checklist-icon done">✓</span>
            <div>
              <strong>Backend FastAPI Application</strong>
              <p style={{ fontSize: "0.85rem", color: "var(--text-dim)", marginTop: "2px" }}>
                Configured with CORS, Pydantic schemas, <code>/api/health</code>, and <code>/api/status</code>.
              </p>
            </div>
          </li>
          <li className="checklist-item">
            <span className="checklist-icon done">✓</span>
            <div>
              <strong>Algorithm Engine Foundation</strong>
              <p style={{ fontSize: "0.85rem", color: "var(--text-dim)", marginTop: "2px" }}>
                <code>BaseRouteOptimizer</code> abstract base class and <code>AlgorithmRegistry</code> with 4 modular solvers.
              </p>
            </div>
          </li>
          <li className="checklist-item">
            <span className="checklist-icon done">✓</span>
            <div>
              <strong>Distance Service Utilities</strong>
              <p style={{ fontSize: "0.85rem", color: "var(--text-dim)", marginTop: "2px" }}>
                Mathematical Haversine distance, travel time estimation, and distance matrix generation.
              </p>
            </div>
          </li>
        </ul>
      </section>

      {/* Footer */}
      <footer className="page-footer">
        <div>RouteFlow &bull; Hyperlocal Route Optimizer</div>
        <div>
          Frontend: <span className="code-pill">localhost:3000</span> &bull; Backend:{" "}
          <span className="code-pill">localhost:8000</span>
        </div>
      </footer>
    </main>
  );
}
