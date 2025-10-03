import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, Loader, Clock, XCircle } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Progress } from '@/components/ui/Progress'
import { ExecutionProgress, ExecutionStep } from '@/types/api'
import { cn } from '@/lib/utils'

interface ProgressLogProps {
  progress: ExecutionProgress
}

export function ProgressLog({ progress }: ProgressLogProps) {
  const logRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight
    }
  }, [progress.logs])

  const getStepIcon = (step: ExecutionStep) => {
    switch (step.status) {
      case 'completed':
        return <CheckCircle className="w-6 h-6 text-drive-healthy" />
      case 'active':
        return <Loader className="w-6 h-6 text-primary animate-spin" />
      case 'failed':
        return <XCircle className="w-6 h-6 text-destructive" />
      default:
        return <Clock className="w-6 h-6 text-muted-foreground opacity-50" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Overall Progress */}
      <Card className="p-6">
        <div className="flex justify-between mb-3 font-semibold">
          <span>Overall Progress</span>
          <span>
            {Math.round(progress.overall_percent)}% (Step {progress.current_step} of{' '}
            {progress.total_steps})
          </span>
        </div>
        <Progress
          value={progress.overall_percent}
          variant="default"
          showShimmer={progress.status === 'running'}
          className="h-5"
        />
      </Card>

      {/* Steps List */}
      <Card className="p-6">
        <div className="space-y-3">
          {progress.steps.map((step, index) => (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className={cn(
                'flex items-center gap-4 p-4 rounded-lg transition-colors',
                step.status === 'active' && 'glass-light border border-primary/20'
              )}
            >
              <div className="flex-shrink-0">{getStepIcon(step)}</div>
              <div className="flex-1">
                <p
                  className={cn(
                    'font-medium',
                    step.status === 'active' && 'text-primary font-semibold'
                  )}
                >
                  {step.description}
                </p>
                {step.progress_percent !== undefined && step.status === 'active' && (
                  <p className="text-sm text-muted-foreground mt-1">
                    {Math.round(step.progress_percent)}% complete
                  </p>
                )}
                {step.error_message && (
                  <p className="text-sm text-destructive mt-1">{step.error_message}</p>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </Card>

      {/* Live Log */}
      <Card className="bg-gray-900 text-green-400">
        <div className="p-4 border-b border-gray-700">
          <h3 className="font-semibold font-mono text-gray-300">LIVE LOG:</h3>
        </div>
        <div
          ref={logRef}
          className="p-4 font-mono text-sm max-h-80 overflow-y-auto bg-gray-950 rounded-b-lg"
        >
          {progress.logs.map((log, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className="mb-2"
            >
              <span className="text-gray-500">[{log.timestamp}]</span>{' '}
              <span
                className={cn({
                  'text-green-400': log.level === 'success' || log.level === 'info',
                  'text-yellow-400': log.level === 'warning',
                  'text-red-400': log.level === 'error',
                })}
              >
                {log.message}
              </span>
            </motion.div>
          ))}
        </div>
        {progress.status === 'running' && (
          <div className="p-4 border-t border-gray-700 text-gray-400 text-center font-mono text-sm">
            Processing...
          </div>
        )}
      </Card>
    </div>
  )
}
