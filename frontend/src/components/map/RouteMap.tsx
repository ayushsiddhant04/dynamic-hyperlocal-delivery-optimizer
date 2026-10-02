"use client";

import { useEffect, useRef } from "react";
import * as mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

type RouteMapProps = {
  startCoordinates?: [number, number] | null;
};

export default function RouteMap({
  startCoordinates = null,
}: RouteMapProps) {
  const mapContainer = useRef<HTMLDivElement | null>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const startMarker = useRef<mapboxgl.Marker | null>(null);

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
      startMarker.current = null;

      map.current?.remove();
      map.current = null;
    };
  }, []);

  useEffect(() => {
    if (!map.current || !startCoordinates) {
      return;
    }

    const [longitude, latitude] = startCoordinates;

    map.current.flyTo({
      center: [longitude, latitude],
      zoom: 14,
      duration: 1200,
    });

    startMarker.current?.remove();

    startMarker.current = new mapboxgl.Marker({
      color: "#111827",
    })
      .setLngLat([longitude, latitude])
      .addTo(map.current);
  }, [startCoordinates]);

  return (
    <div
      ref={mapContainer}
      className="h-full w-full"
    />
  );
}