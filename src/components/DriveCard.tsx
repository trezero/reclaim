import { motion } from 'framer-motion'
import { HardDrive } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Progress } from '@/components/ui/Progress'
import { Drive } from '@/types/api'
import { formatBytes, getDriveStatusBg } from '@/lib/utils'
import { cn } from '@/lib/utils'

interface DriveCardProps {
  drive: Drive
  index: number
}

export function DriveCard({ drive, index }: DriveCardProps) {
  const variant =
    drive.status === 'critical' ? 'critical' : drive.status === 'warning' ? 'warning' : 'healthy'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4, delay: index * 0.15, type: 'spring', bounce: 0.3 }}
    >
      <Card
        className={cn(
          'p-6 transition-all duration-200 hover:shadow-xl hover:-translate-y-1 hover:scale-[1.02]',
          drive.status === 'critical' &&
            'border-drive-critical bg-gradient-to-br from-card to-red-50/30'
        )}
      >
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-3">
            <HardDrive className="w-6 h-6" />
            <h3 className="text-xl font-semibold font-mono">{drive.letter}: DRIVE</h3>
          </div>
          <div
            className={cn(
              'px-3 py-1 rounded-full text-sm font-semibold text-white',
              getDriveStatusBg(drive.status),
              drive.status === 'critical' && 'animate-pulse'
            )}
          >
            {Math.round(drive.percent_used)}%
          </div>
        </div>

        <div className="space-y-3">
          <Progress value={drive.percent_used} variant={variant} showShimmer />
          <div className="flex justify-between text-sm text-muted-foreground font-mono">
            <span>{formatBytes(drive.used_bytes)} used</span>
            <span>{formatBytes(drive.total_bytes)} total</span>
          </div>
        </div>
      </Card>
    </motion.div>
  )
}
