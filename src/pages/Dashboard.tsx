import { motion } from 'framer-motion'
import { AlertTriangle, Sparkles, RefreshCw } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAnalysis } from '@/hooks/useAnalysis'
import { DriveCard } from '@/components/DriveCard'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { formatBytes } from '@/lib/utils'

export function Dashboard() {
  const navigate = useNavigate()
  const { data: analysis, isLoading, error, refetch } = useAnalysis()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-lg text-muted-foreground">Analyzing your drives...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="p-8 max-w-md">
          <AlertTriangle className="w-12 h-12 text-destructive mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-center mb-2">Connection Error</h2>
          <p className="text-muted-foreground text-center mb-4">
            Failed to connect to the backend. Make sure the Python server is running on
            http://127.0.0.1:8000
          </p>
          <Button onClick={() => refetch()} className="w-full">
            Retry
          </Button>
        </Card>
      </div>
    )
  }

  if (!analysis) return null

  return (
    <div className="space-y-8">
      {/* Drive Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {analysis.drives.map((drive, index) => (
          <DriveCard key={drive.letter} drive={drive} index={index} />
        ))}
      </div>

      {/* Imbalance Alert */}
      {analysis.has_imbalance && analysis.imbalance_message && (
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, type: 'spring', bounce: 0.3 }}
        >
          <Card className="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-950/20 dark:to-orange-950/20 border-2 border-drive-critical p-6">
            <div className="flex items-center gap-4">
              <AlertTriangle className="w-8 h-8 text-drive-critical flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-lg mb-1">⚠️ IMBALANCE DETECTED</h3>
                <p className="text-muted-foreground">{analysis.imbalance_message}</p>
              </div>
            </div>
          </Card>
        </motion.div>
      )}

      {/* Top Space Consumers */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Card className="p-6">
          <h2 className="text-2xl font-semibold mb-6">TOP SPACE CONSUMERS</h2>
          <div className="space-y-3">
            {analysis.top_consumers.map((consumer, index) => (
              <motion.div
                key={consumer.path}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div className="flex-1 font-medium">{consumer.name}</div>
                <div className="flex-[2] h-2 bg-muted rounded-full overflow-hidden">
                  <motion.div
                    className="h-full gradient-accent rounded-full"
                    initial={{ width: 0 }}
                    animate={{
                      width: `${(consumer.size_bytes / analysis.top_consumers[0].size_bytes) * 100}%`,
                    }}
                    transition={{ duration: 0.8, delay: index * 0.1 }}
                  />
                </div>
                <div className="min-w-[80px] text-right font-semibold font-mono">
                  {formatBytes(consumer.size_bytes)}
                </div>
              </motion.div>
            ))}
          </div>

          <div className="mt-8 flex justify-center">
            <Button
              onClick={() => navigate('/plans')}
              size="lg"
              className="gradient-primary text-white shadow-lg hover:shadow-2xl"
            >
              <Sparkles className="w-6 h-6" />
              GET AI RECOMMENDATIONS
            </Button>
          </div>
        </Card>
      </motion.div>
    </div>
  )
}
