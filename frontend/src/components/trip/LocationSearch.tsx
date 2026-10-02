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
  const onSelectRef = useRef(onSelect);

  // Always keep the latest callback without rebuilding
  // the Mapbox Search Box.
  useEffect(() => {
    onSelectRef.current = onSelect;
  }, [onSelect]);

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
          const name =
            feature.properties?.name ??
            "";

          const formatted =
            feature.properties?.place_formatted ??
            "";

          const address =
            [name, formatted]
              .filter(Boolean)
              .join(", ") ||
            "Selected location";

          // Keep the selected text visible.
          searchBox.value = address;

          onSelectRef.current({
            address,
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
  }, [placeholder]);

  return (
    <div
      ref={containerRef}
      className="mapbox-search-container w-full"
    />
  );
}