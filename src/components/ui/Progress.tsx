import { HTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ProgressProps extends HTMLAttributes<HTMLDivElement> {
  value: number
  variant?: 'default' | 'critical' | 'warning' | 'healthy'
  showShimmer?: boolean
}

export const Progress = forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value, variant = 'default', showShimmer = false, ...props }, ref) => {
    const percentage = Math.min(Math.max(value, 0), 100)

    return (
      <div
        ref={ref}
        className={cn('relative h-3 w-full overflow-hidden rounded-full bg-muted', className)}
        {...props}
      >
        <div
          className={cn('h-full rounded-full transition-all duration-500 relative overflow-hidden', {
            'gradient-primary': variant === 'default',
            'gradient-danger': variant === 'critical',
            'gradient-warning': variant === 'warning',
            'gradient-success': variant === 'healthy',
          })}
          style={{ width: `${percentage}%` }}
        >
          {showShimmer && (
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
          )}
        </div>
      </div>
    )
  }
)

Progress.displayName = 'Progress'
