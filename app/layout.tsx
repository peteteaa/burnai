import type React from "react"
import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "BurnAI - Controlled Burn Analysis",
  description: "Intelligent mapping system for controlled burn analysis and planning",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="relative">
        <div className="relative min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}

