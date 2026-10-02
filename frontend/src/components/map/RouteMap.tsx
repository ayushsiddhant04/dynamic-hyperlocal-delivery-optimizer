"use client";

import { useEffect, useRef } from "react";
import * as mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

type StopLocation = {
  id: number;
  coordinates: [number, number];
};

type RouteMapProps = {
  startCoordinates?: [number, number] | null;
  stopLocations?: StopLocation[];
};

export default function RouteMap({
  startCoordinates = null,
  stopLocations = [],
}: RouteMapProps) {
  const mapContainer = useRef<HTMLDivElement | null>(null);
  const map = useRef<mapboxgl.Map | null>(null);

  const startMarker = useRef<mapboxgl.Marker | null>(null);
  const stopMarkers = useRef<mapboxgl.Marker[]>([]);

  useEffect(() => {
    if (!mapContainer.current || map.current) {
      return;
    }

    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;

    if (!token) {
      console.error("NEXT_PUBLIC_MAPBOX_TOKEN is missing.");
      return;
    }

    map.current = new mapboxgl.Map({
      accessToken: token,
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/streets-v12",
      center: [77.5946, 12.9716],
      zoom: 11,
    });

    map.current.addControl(
      new mapboxgl.NavigationControl(),
      "top-right"
    );

    return () => {
      startMarker.current?.remove();

      stopMarkers.current.forEach((marker) => {
        marker.remove();
      });

      startMarker.current = null;
      stopMarkers.current = [];

      map.current?.remove();
      map.current = null;
    };
  }, []);

  useEffect(() => {
    if (!map.current || !startCoordinates) {
      return;
    }

    const [longitude, latitude] = startCoordinates;

    startMarker.current?.remove();

    startMarker.current = new mapboxgl.Marker({
      color: "#111827",
    })
      .setLngLat([longitude, latitude])
      .addTo(map.current);
  }, [startCoordinates]);

  useEffect(() => {
    if (!map.current) {
      return;
    }

    stopMarkers.current.forEach((marker) => {
      marker.remove();
    });

    stopMarkers.current = [];

    stopLocations.forEach((stop, index) => {
      const markerElement = document.createElement("div");

      markerElement.className =
        "flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-indigo-600 text-[10px] font-semibold text-white shadow-md";

      markerElement.textContent = String(index + 1);

      const marker = new mapboxgl.Marker({
        element: markerElement,
      })
        .setLngLat(stop.coordinates)
        .addTo(map.current!);

      stopMarkers.current.push(marker);
    });

    const allCoordinates: [number, number][] = [];

    if (startCoordinates) {
      allCoordinates.push(startCoordinates);
    }

    stopLocations.forEach((stop) => {
      allCoordinates.push(stop.coordinates);
    });

    if (allCoordinates.length === 0) {
      return;
    }

    const bounds = new mapboxgl.LngLatBounds();

    allCoordinates.forEach(([longitude, latitude]) => {
      bounds.extend([longitude, latitude]);
    });

    map.current.fitBounds(bounds, {
      padding: 100,
      maxZoom: 14,
      duration: 1000,
    });
  }, [startCoordinates, stopLocations]);

  return (
    <div
      ref={mapContainer}
      className="h-full w-full"
    />
  );
}