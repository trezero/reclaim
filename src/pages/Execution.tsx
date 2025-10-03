import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { X, CheckCircle, XCircle, AlertTriangle } from 'lucide-react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useExecutePlan } from '@/hooks/useExecutePlan'
import { useProgress } from '@/hooks/useProgress'
import { ProgressLog } from '@/components/ProgressLog'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

export function Execution() {
  const navigate = useNavigate()
  const location = useLocation()
  const planId = location.state?.planId

  const [executionId, setExecutionId] = useState<string | null>(null)
  const executeMutation = useExecutePlan()
  const { progress, isConnected } = useProgress(executionId)

  useEffect(() => {
    if (planId && !executionId) {
      executeMutation.mutate(
        { plan_id: planId },
        {
          onSuccess: (data) => {
            setExecutionId(data.execution_id)
          },
          onError: (error) => {
            console.error('Failed to start execution:', error)
          },
        }
      )
    }
  }, [planId, executionId])

  const handleCancel = () => {
    // TODO: Implement cancellation API call
    navigate('/plans')
  }

  const handleRollback = () => {
    // TODO: Implement rollback API call
    navigate('/plans')
  }

  if (executeMutation.isPending) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="p-8 text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
            className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"
          />
          <p className="text-lg">Starting execution...</p>
        </Card>
      </div>
    )
  }

  if (executeMutation.isError) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="p-8 max-w-md">
          <XCircle className="w-16 h-16 text-destructive mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-center mb-2">Execution Failed</h2>
          <p className="text-muted-foreground text-center mb-6">
            {executeMutation.error instanceof Error
              ? executeMutation.error.message
              : 'Failed to start execution'}
          </p>
          <Button onClick={() => navigate('/plans')} className="w-full">
            Back to Plans
          </Button>
        </Card>
      </div>
    )
  }

  if (!progress) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="p-8">
          <p>Connecting to execution stream...</p>
        </Card>
      </div>
    )
  }

  const isComplete = progress.status === 'completed'
  const isFailed = progress.status === 'failed'
  const isRunning = progress.status === 'running'

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">
          {isComplete ? 'Execution Complete' : isFailed ? 'Execution Failed' : 'Executing Plan...'}
        </h1>
        {isRunning && (
          <Button variant="ghost" onClick={handleCancel}>
            <X className="w-5 h-5" />
            Cancel
          </Button>
        )}
      </div>

      {/* Progress Log */}
      <ProgressLog progress={progress} />

      {/* Success State */}
      {isComplete && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', bounce: 0.4 }}
        >
          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 border-2 border-drive-healthy p-8">
            <div className="flex items-center gap-4 mb-4">
              <CheckCircle className="w-12 h-12 text-drive-healthy" />
              <div>
                <h3 className="text-2xl font-bold text-drive-healthy">Success!</h3>
                <p className="text-muted-foreground">All operations completed successfully</p>
              </div>
            </div>
            <div className="flex gap-4">
              <Button onClick={() => navigate('/')} className="flex-1">
                Back to Dashboard
              </Button>
              <Button variant="secondary" onClick={handleRollback} className="flex-1">
                Rollback Changes
              </Button>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Failure State */}
      {isFailed && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', bounce: 0.4 }}
        >
          <Card className="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-950/20 dark:to-orange-950/20 border-2 border-destructive p-8">
            <div className="flex items-center gap-4 mb-4">
              <AlertTriangle className="w-12 h-12 text-destructive" />
              <div>
                <h3 className="text-2xl font-bold text-destructive">Execution Failed</h3>
                <p className="text-muted-foreground">
                  Some operations failed. Review the logs above.
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <Button onClick={() => navigate('/')} variant="ghost" className="flex-1">
                Back to Dashboard
              </Button>
              <Button onClick={handleRollback} className="flex-1">
                Rollback Changes
              </Button>
            </div>
          </Card>
        </motion.div>
      )}
    </div>
  )
}
