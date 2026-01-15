import React from "react";
import type { Metadata } from "next";
import { SidebarProvider } from "@/components/ui/sidebar";

export const metadata: Metadata = {
  title: "PRPay Dashboard",
  description: "Dashboard page for PRPay application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="w-full">
      <SidebarProvider>{children}</SidebarProvider>
    </div>
  );
}