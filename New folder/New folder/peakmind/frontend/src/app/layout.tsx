import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ClerkProvider } from '@clerk/nextjs'
import { AuthHeader } from '@/components/AuthHeader'
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PeakMind AI - Your Personal Performance Coach",
  description: "An intelligent productivity ecosystem that combines AI Task Management, Energy Tracking, Study Planner, Fitness Coach, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider afterSignOutUrl="/">
      <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}>
        <body className="min-h-full flex flex-col bg-slate-950 text-slate-50">
          {/* Global Header / Nav */}
          <header className="flex justify-between items-center p-4 lg:px-8 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
            <a href="/" className="text-xl font-bold text-brand-400 hover:text-brand-300 transition-colors">PeakMind AI</a>
            <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
              <a href="/" className="hover:text-white transition-colors">Dashboard</a>
              <a href="/study" className="hover:text-white transition-colors">Study Planner</a>
              <a href="/fitness" className="hover:text-white transition-colors">Fitness Coach</a>
            </nav>
            <AuthHeader />
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
