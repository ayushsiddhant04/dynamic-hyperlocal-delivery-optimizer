import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RouteFlow — Dynamic Hyperlocal Delivery Optimizer",
  description:
    "Intelligent delivery route optimization platform with real-time dynamic re-routing and multi-algorithm benchmarking.",
  keywords: [
    "route optimization",
    "hyperlocal delivery",
    "tsp",
    "vrp",
    "dispatch",
    "fastapi",
    "nextjs",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
