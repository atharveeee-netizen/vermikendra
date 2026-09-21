import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Vermikendra",
  description: "Farmer-first vermicomposting monitoring and decision support.",
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  themeColor: "#2d7a42",
};

import BottomNav from "../components/BottomNav";
import GlobalFAB from "../components/GlobalFAB";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#F9F8F4]">
        {children}
        <GlobalFAB />
        <BottomNav />
      </body>
    </html>
  );
}
