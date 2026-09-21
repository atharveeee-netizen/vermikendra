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

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        {children}
      </body>
    </html>
  );
}
