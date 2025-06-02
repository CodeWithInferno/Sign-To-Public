import { Inter } from 'next/font/google'
import { ThemeProvider } from '@/components/theme-provider'
import { Navigation } from '@/components/navigation'
import { cn } from '@/lib/utils'

import '@/styles/globals.css'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn(
          'min-h-screen bg-background font-sans antialiased',
          inter.className
        )}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="relative flex min-h-screen flex-col">
            <Navigation />
            <div className="flex-1">{children}</div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}

export const metadata = {
  title: 'ASL Recognition Documentation',
  description: 'Documentation for the ASL Recognition project',
}
