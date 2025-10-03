import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, CheckCircle, Lightbulb, RotateCcw } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { PlanAction } from '@/types/api'
import { formatBytes } from '@/lib/utils'

interface ActionCardProps {
  action: PlanAction
  index: number
}

export function ActionCard({ action, index }: ActionCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.2, delay: index * 0.1 }}
    >
      <Card className="overflow-hidden">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full p-4 flex items-center justify-between hover:bg-muted/50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <motion.div
              animate={{ rotate: isExpanded ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChevronDown className="w-5 h-5" />
            </motion.div>
            <CheckCircle className="w-5 h-5 text-drive-healthy" />
            <div className="text-left">
              <h4 className="font-semibold">{action.description}</h4>
              <p className="text-sm text-muted-foreground font-mono">
                {formatBytes(action.size_bytes)}
              </p>
            </div>
          </div>
        </button>

        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="p-4 pt-0 space-y-4">
                {action.source_path && (
                  <div className="bg-muted p-3 rounded-lg">
                    <p className="text-sm mb-1">
                      <strong>From:</strong>
                    </p>
                    <p className="text-sm font-mono text-muted-foreground">{action.source_path}</p>
                  </div>
                )}

                {action.target_path && (
                  <div className="bg-muted p-3 rounded-lg">
                    <p className="text-sm mb-1">
                      <strong>To:</strong>
                    </p>
                    <p className="text-sm font-mono text-muted-foreground">{action.target_path}</p>
                  </div>
                )}

                {action.command && (
                  <div className="bg-muted p-3 rounded-lg">
                    <p className="text-sm mb-1">
                      <strong>Command:</strong>
                    </p>
                    <p className="text-sm font-mono text-muted-foreground">{action.command}</p>
                  </div>
                )}

                <div className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-950/20 rounded-lg border border-green-200 dark:border-green-800">
                  <Lightbulb className="w-5 h-5 text-drive-healthy flex-shrink-0 mt-0.5" />
                  <div className="text-sm">
                    <strong className="text-drive-healthy">💡 Safe:</strong>{' '}
                    {action.safety_explanation}
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 glass-light rounded-lg border border-border">
                  <RotateCcw className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                  <div className="text-sm">
                    <strong className="text-primary">🔄 Rollback:</strong> {action.rollback_option}
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </Card>
    </motion.div>
  )
}
