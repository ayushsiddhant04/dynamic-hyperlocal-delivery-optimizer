"use client";

import RouteMap from "@/components/map/RouteMap";
import LocationSearch from "@/components/trip/LocationSearch";
import { useCallback, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import {
  Activity,
  ChevronDown,
  Clock3,
  Navigation,
  Package,
  Plus,
  RefreshCw,
  Route,
  Settings2,
  Truck,
  X,
  Zap,
} from "lucide-react";

type Stop = {
  id: number;
  name: string;
  address: string;
  coordinates: [number, number] | null;
};

const createStop = (id: number): Stop => ({
  id,
  name: `Customer ${String.fromCharCode(64 + id)}`,
  address: "",
  coordinates: null,
});

export default function Home() {
  const [startPoint, setStartPoint] = useState("");
  const [startCoordinates, setStartCoordinates] = useState<
    [number, number] | null
  >(null);

  const [stops, setStops] = useState<Stop[]>([
    createStop(1),
    createStop(2),
    createStop(3),
  ]);

  const [method, setMethod] = useState("Recommended");
  const [priority, setPriority] = useState("Shortest time");



  const handleStartLocationSelect = useCallback(
    (location: {
      address: string;
      coordinates: [number, number];
    }) => {
      setStartPoint(location.address);
      setStartCoordinates(location.coordinates);
    },
    []
  );

  const addStop = () => {
    const nextId =
      stops.length > 0
        ? Math.max(...stops.map((stop) => stop.id)) + 1
        : 1;

    setStops((current) => [...current, createStop(nextId)]);
  };

  const removeStop = (id: number) => {
    setStops((current) => current.filter((stop) => stop.id !== id));
  };


  const handleStopLocationSelect = useCallback(
    (
      id: number,
      location: {
        address: string;
        coordinates: [number, number];
      }
    ) => {
      setStops((current) =>
        current.map((stop) =>
          stop.id === id
            ? {
                ...stop,
                address: location.address,
                coordinates: location.coordinates,
              }
            : stop
        )
      );
    },
    []
  );

  const resetPlanner = () => {
    setStartPoint("");
    setStartCoordinates(null);
    setStops([createStop(1), createStop(2), createStop(3)]);
    setMethod("Recommended");
    setPriority("Shortest time");
  };

  return (
    <main className="min-h-screen bg-[#f5f7fb] text-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-[1800px] items-center justify-between px-5 lg:px-7">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 text-white shadow-sm">
              <Truck size={20} strokeWidth={2.2} />
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-[17px] font-semibold tracking-tight">
                  RouteFlow
                </h1>

                <span className="hidden text-xs text-slate-400 sm:inline">
                  Delivery Optimizer
                </span>
              </div>

              <p className="text-[11px] text-slate-500">
                Smarter Routes. Faster Deliveries.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs sm:flex">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              <span className="text-slate-600">System Online</span>
            </div>

            <button
              type="button"
              aria-label="Settings"
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 transition hover:border-slate-300 hover:bg-slate-50"
            >
              <Settings2 size={17} />
            </button>

            <div className="hidden h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white sm:flex">
              A
            </div>
          </div>
        </div>
      </header>

      {/* Main */}
      <section className="mx-auto max-w-[1800px] p-4 lg:p-6">
        <div className="grid min-h-[calc(100vh-104px)] gap-4 xl:grid-cols-[300px_minmax(0,1fr)_320px]">
          {/* Planner */}
          <aside className="flex flex-col rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-100 p-5">
              <div className="flex items-center gap-2">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100">
                  <Route size={17} className="text-slate-700" />
                </div>

                <div>
                  <h2 className="text-sm font-semibold">Plan Delivery</h2>
                  <p className="text-xs text-slate-500">
                    Build your delivery trip
                  </p>
                </div>
              </div>
            </div>

            <div className="flex-1 space-y-6 p-5">
              {/* Starting point */}
              <div>
                <label className="mb-2 block text-xs font-medium text-slate-600">
                  Starting point
                </label>

                <LocationSearch
                  placeholder="Search shop or starting point"
                  onSelect={handleStartLocationSelect}
                />

                {startCoordinates && (
                  <p className="mt-2 truncate text-[10px] text-emerald-600">
                    Selected: {startPoint}
                  </p>
                )}
              </div>

              {/* Delivery stops */}
              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label className="text-xs font-medium text-slate-600">
                    Delivery stops
                  </label>

                  <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] font-medium text-slate-500">
                    {stops.length} stops
                  </span>
                </div>

                <div className="space-y-2.5">
                  <AnimatePresence initial={false}>
                    {stops.map((stop, index) => (
                      <motion.div
                        key={stop.id}
                        layout
                        initial={{ opacity: 0, y: -8 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{
                          opacity: 0,
                          height: 0,
                          marginBottom: 0,
                        }}
                        className="group rounded-xl border border-slate-200 bg-white p-2"
                      >
                        <div className="flex items-center gap-2">
                          <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-slate-900 text-[10px] font-semibold text-white">
                            {index + 1}
                          </div>

                          <div className="min-w-0 flex-1">
                            <p className="mb-1 text-[10px] font-medium text-slate-500">
                              {stop.name}
                            </p>

                            <LocationSearch
                              placeholder="Delivery location"
                              onSelect={(location) =>
                                handleStopLocationSelect(
                                  stop.id,
                                  location
                                )
                              }
                            />

                            {stop.coordinates && (
                              <p className="mt-1 text-[9px] text-emerald-600">
                                Location selected
                              </p>
                            )}
                          </div>

                          <button
                            type="button"
                            onClick={() => removeStop(stop.id)}
                            aria-label={`Remove ${stop.name}`}
                            className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg text-slate-400 opacity-0 transition hover:bg-slate-100 hover:text-slate-700 group-hover:opacity-100"
                          >
                            <X size={14} />
                          </button>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>

                <button
                  type="button"
                  onClick={addStop}
                  className="mt-3 flex h-10 w-full items-center justify-center gap-2 rounded-xl border border-dashed border-slate-300 text-xs font-medium text-slate-600 transition hover:border-slate-400 hover:bg-slate-50"
                >
                  <Plus size={15} />
                  Add delivery stop
                </button>
              </div>

              {/* Optimization settings */}
              <div className="space-y-3 border-t border-slate-100 pt-5">
                <div className="flex items-center gap-2">
                  <Zap size={15} className="text-slate-500" />

                  <p className="text-xs font-medium text-slate-600">
                    Optimization settings
                  </p>
                </div>

                <div>
                  <label
                    htmlFor="method"
                    className="mb-1.5 block text-[11px] text-slate-500"
                  >
                    Method
                  </label>

                  <div className="relative">
                    <select
                      id="method"
                      value={method}
                      onChange={(event) => setMethod(event.target.value)}
                      className="h-10 w-full appearance-none rounded-xl border border-slate-200 bg-slate-50 px-3 text-xs outline-none focus:border-slate-400 focus:bg-white"
                    >
                      <option>Recommended</option>
                      <option>Nearest Neighbor</option>
                      <option>2-opt</option>
                    </select>

                    <ChevronDown
                      size={14}
                      className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="priority"
                    className="mb-1.5 block text-[11px] text-slate-500"
                  >
                    Priority
                  </label>

                  <div className="relative">
                    <select
                      id="priority"
                      value={priority}
                      onChange={(event) => setPriority(event.target.value)}
                      className="h-10 w-full appearance-none rounded-xl border border-slate-200 bg-slate-50 px-3 text-xs outline-none focus:border-slate-400 focus:bg-white"
                    >
                      <option>Shortest time</option>
                      <option>Minimum distance</option>
                      <option>Time-critical windows</option>
                    </select>

                    <ChevronDown
                      size={14}
                      className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Planner actions */}
            <div className="space-y-2 border-t border-slate-100 p-5">
              <button
                type="button"
                disabled={
                  !startCoordinates ||
                  stops.filter((stop) => stop.coordinates).length < 2
                }
                className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-slate-900 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400"
              >
                <Route size={16} />
                Optimize Route
              </button>

              <button
                type="button"
                onClick={resetPlanner}
                className="flex h-10 w-full items-center justify-center gap-2 rounded-xl text-xs font-medium text-slate-500 transition hover:bg-slate-50 hover:text-slate-700"
              >
                <RefreshCw size={14} />
                Reset
              </button>
            </div>
          </aside>

          {/* Real Mapbox map */}
          <section className="relative min-h-[620px] overflow-hidden rounded-2xl border border-slate-200 bg-[#edf2f7] shadow-sm">
            <div className="absolute inset-0">
              <RouteMap
  startCoordinates={startCoordinates}
  stopLocations={stops
    .filter((stop) => stop.coordinates !== null)
    .map((stop) => ({
      id: stop.id,
      coordinates: stop.coordinates as [number, number],
    }))}
/>
            </div>

            <div className="pointer-events-none absolute left-5 top-5 z-10 rounded-xl border border-white/80 bg-white/90 px-3 py-2 shadow-sm backdrop-blur">
              <p className="text-xs font-semibold text-slate-700">
                Interactive Map
              </p>

              <p className="mt-0.5 text-[10px] text-slate-400">
                RouteFlow workspace
              </p>
            </div>
          </section>

          {/* Route summary */}
          <aside className="flex flex-col gap-4">
            <section className="rounded-2xl border border-slate-200 bg-white shadow-sm">
              <div className="border-b border-slate-100 p-5">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-xs font-medium text-slate-400">
                      Route planning
                    </p>

                    <h2 className="mt-1 text-base font-semibold">
                      Optimized Route
                    </h2>
                  </div>

                  <span className="rounded-full bg-amber-50 px-2.5 py-1 text-[10px] font-semibold text-amber-700">
                    Ready
                  </span>
                </div>
              </div>

              <div className="p-5">
                <p className="mb-3 text-xs font-medium text-slate-500">
                  Delivery order
                </p>

                <div className="space-y-2">
                  {stops.map((stop, index) => (
                    <div
                      key={stop.id}
                      className="flex items-center gap-3 rounded-xl border border-slate-100 px-3 py-2.5"
                    >
                      <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-slate-100 text-[10px] font-semibold text-slate-600">
                        {index + 1}
                      </div>

                      <span className="truncate text-xs font-medium text-slate-700">
                        {stop.name}
                      </span>

                      <ChevronDown
                        size={13}
                        className="ml-auto rotate-[-90deg] text-slate-300"
                      />
                    </div>
                  ))}
                </div>

                <div className="mt-5 grid grid-cols-2 gap-2">
                  <div className="rounded-xl bg-slate-50 p-3">
                    <div className="flex items-center gap-1.5 text-slate-400">
                      <Navigation size={13} />
                      <span className="text-[10px]">Distance</span>
                    </div>

                    <p className="mt-1 text-sm font-semibold">-- km</p>
                  </div>

                  <div className="rounded-xl bg-slate-50 p-3">
                    <div className="flex items-center gap-1.5 text-slate-400">
                      <Clock3 size={13} />
                      <span className="text-[10px]">ETA</span>
                    </div>

                    <p className="mt-1 text-sm font-semibold">-- min</p>
                  </div>
                </div>

                <div className="mt-2 rounded-xl bg-slate-50 p-3">
                  <div className="flex items-center gap-1.5 text-slate-400">
                    <Package size={13} />
                    <span className="text-[10px]">Stops</span>
                  </div>

                  <p className="mt-1 text-sm font-semibold">
                    {stops.length}
                  </p>
                </div>
              </div>

              <div className="border-t border-slate-100 p-5">
                <button
                  type="button"
                  disabled
                  className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-slate-100 text-sm font-semibold text-slate-400"
                >
                  <Navigation size={16} />
                  Start Delivery
                </button>
              </div>
            </section>

            {/* Analysis preview */}
            <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-2">
                <Activity size={16} className="text-slate-500" />

                <h3 className="text-sm font-semibold">
                  Algorithm Analysis
                </h3>
              </div>

              <p className="mt-1 text-[11px] text-slate-400">
                Available after optimization
              </p>

              <div className="mt-4 space-y-2">
                {[
                  ["Nearest Neighbor", "--"],
                  ["2-opt", "--"],
                  ["Brute Force", "--"],
                ].map(([name, value]) => (
                  <div
                    key={name}
                    className="flex items-center justify-between rounded-xl border border-slate-100 px-3 py-2.5"
                  >
                    <span className="text-xs text-slate-600">
                      {name}
                    </span>

                    <span className="text-xs font-semibold text-slate-400">
                      {value}
                    </span>
                  </div>
                ))}
              </div>

              <div className="mt-4 flex items-center gap-2 rounded-xl bg-slate-50 p-3">
                <Clock3 size={14} className="text-slate-400" />

                <div>
                  <p className="text-[10px] font-medium text-slate-500">
                    Trip status
                  </p>

                  <p className="text-xs font-semibold text-slate-700">
                    No active delivery
                  </p>
                </div>
              </div>
            </section>
          </aside>
        </div>
      </section>
    </main>
  );
}