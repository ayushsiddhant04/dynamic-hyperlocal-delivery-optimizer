"use client";

import { useEffect, useRef } from "react";

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

  useEffect(() => {
    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
    const container = containerRef.current;

    if (!token || !container) {
      return;
    }

    let cancelled = false;

    const initializeSearchBox = async () => {
      const { MapboxSearchBox } = await import(
        "@mapbox/search-js-web"
      );

      if (cancelled) {
        return;
      }

      const searchBox = new MapboxSearchBox();

      searchBox.accessToken = token;

      searchBox.options = {
        language: "en",
        country: "IN",
        types: "address,poi",
      };

      searchBox.placeholder = placeholder;

      searchBox.addEventListener("retrieve", (event) => {
        const response = event.detail;
        const feature = response.features?.[0];

        const coordinates = feature?.geometry?.coordinates;

        if (
          Array.isArray(coordinates) &&
          coordinates.length >= 2
        ) {
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

      container.appendChild(
        searchBox as unknown as Node
      );
    };

    initializeSearchBox();

    return () => {
      cancelled = true;
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