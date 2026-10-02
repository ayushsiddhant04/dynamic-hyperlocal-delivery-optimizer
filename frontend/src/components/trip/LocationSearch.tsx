"use client";

import { useEffect, useRef } from "react";
import { MapboxGeocoder } from "@mapbox/search-js-web";

type Coordinates = [number, number];

type LocationSearchProps = {
  placeholder?: string;
  onSelect: (location: {
    address: string;
    coordinates: Coordinates;
  }) => void;
};

export default function LocationSearch({
  placeholder = "Search location",
  onSelect,
}: LocationSearchProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const geocoderRef = useRef<MapboxGeocoder | null>(null);

  useEffect(() => {
    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
    const container = containerRef.current;

    if (!token || !container) {
      return;
    }

    const geocoder = new MapboxGeocoder();

    geocoder.accessToken = token;

    geocoder.options = {
      language: "en",
      country: "IN",
      types: "address,poi",
    };

    geocoder.placeholder = placeholder;

    geocoder.addEventListener("retrieve", (event) => {
      const feature = event.detail;
      const coordinates = feature?.geometry?.coordinates;

      if (Array.isArray(coordinates) && coordinates.length >= 2) {
        onSelect({
          address:
            feature.properties?.full_address ||
            feature.properties?.name ||
            "",
          coordinates: [
            Number(coordinates[0]),
            Number(coordinates[1]),
          ],
        });
      }
    });

    container.innerHTML = "";

    container.appendChild(geocoder as unknown as Node);

    geocoderRef.current = geocoder;

    return () => {
      geocoderRef.current = null;
      container.innerHTML = "";
    };
  }, [onSelect, placeholder]);

  return (
    <div
      ref={containerRef}
      className="mapbox-search-container w-full"
    />
  );
}