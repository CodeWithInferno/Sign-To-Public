'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'

const navigation = {
  main: [
    { name: 'Introduction', href: '/' },
    { name: 'Getting Started', href: '/docs/getting-started' },
  ],
  models: [
    { name: 'CNN Model', href: '/docs/models/cnn' },
    { name: 'YOLO Detection', href: '/docs/models/yolo' },
    { name: 'Keypoint Detection', href: '/docs/models/keypoints' },
  ],
  api: [
    { name: 'Server API', href: '/docs/api/server' },
    { name: 'Mobile Integration', href: '/docs/api/mobile' },
  ],
  deployment: [
    { name: 'Local Setup', href: '/docs/deployment/local' },
    { name: 'Production', href: '/docs/deployment/production' },
  ],
}

export function Navigation() {
  const pathname = usePathname()

  return (
    <nav className="fixed top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="hidden font-bold sm:inline-block">
              ASL Recognition Docs
            </span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <NavigationGroup items={navigation.main} pathname={pathname} />
            <NavigationGroup items={navigation.models} pathname={pathname} />
            <NavigationGroup items={navigation.api} pathname={pathname} />
            <NavigationGroup items={navigation.deployment} pathname={pathname} />
          </nav>
        </div>
      </div>
    </nav>
  )
}

function NavigationGroup({ items, pathname }) {
  return (
    <div className="flex items-center space-x-6">
      {items.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={cn(
            'transition-colors hover:text-foreground/80',
            pathname === item.href ? 'text-foreground' : 'text-foreground/60'
          )}
        >
          {item.name}
        </Link>
      ))}
    </div>
  )
}