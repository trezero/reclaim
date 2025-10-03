import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowLeft, Play } from 'lucide-react'
import { useNavigate, useParams } from 'react-router-dom'
import { usePlanDetails } from '@/hooks/usePlans'
import { ActionCard } from '@/components/ActionCard'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { formatBytes, formatDuration } from '@/lib/utils'

export function PlanDetails() {
  const navigate = useNavigate()
  const { planId } = useParams<{ planId: string }>()
  const { data: plan, isLoading } = usePlanDetails(planId || null)
  const [showConfirm, setShowConfirm] = useState(false)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading plan details...</p>
      </div>
    )
  }

  if (!plan) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="p-8">
          <p>Plan not found</p>
          <Button onClick={() => navigate('/plans')} className="mt-4">
            Back to Plans
          </Button>
        </Card>
      </div>
    )
  }

  // Group actions by type
  const groupedActions = plan.actions.reduce(
    (acc, action) => {
      const key = action.type
      if (!acc[key]) acc[key] = []
      acc[key].push(action)
      return acc
    },
    {} as Record<string, typeof plan.actions>
  )

  const actionGroups = Object.entries(groupedActions).map(([type, actions]) => ({
    type,
    title: type.replace(/_/g, ' '),
    totalSize: actions.reduce((sum, a) => sum + a.size_bytes, 0),
    actions,
  }))

  const handleExecute = () => {
    navigate('/execution', { state: { planId: plan.id } })
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={() => navigate('/plans')} className="p-2">
            <ArrowLeft className="w-6 h-6" />
          </Button>
          <h1 className="text-3xl font-bold">{plan.name} Plan Details</h1>
        </div>
        <Button onClick={() => setShowConfirm(true)} size="lg">
          <Play className="w-5 h-5" />
          Execute Plan
        </Button>
      </div>

      {/* Summary */}
      <Card className="bg-gradient-to-br from-primary/5 to-accent/5 border-2 border-primary p-6">
        <div className="flex flex-wrap gap-8 items-center font-mono font-semibold">
          <span>💾 {formatBytes(plan.space_saved_bytes)} freed</span>
          <span>🛡️ {plan.risk_level} Risk</span>
          <span>⏱️ ~{formatDuration(plan.estimated_minutes)}</span>
        </div>
      </Card>

      {/* Action Groups */}
      {actionGroups.map((group) => (
        <div key={group.type} className="space-y-4">
          <h2 className="text-xl font-semibold uppercase tracking-wide">
            {group.title} ({formatBytes(group.totalSize)})
          </h2>
          <div className="space-y-3">
            {group.actions.map((action, index) => (
              <ActionCard key={action.id} action={action} index={index} />
            ))}
          </div>
        </div>
      ))}

      {/* Actions Footer */}
      <div className="flex justify-end gap-4 pt-4">
        <Button variant="ghost" onClick={() => navigate('/plans')}>
          Cancel
        </Button>
        <Button onClick={() => setShowConfirm(true)}>
          <Play className="w-5 h-5" />
          Execute Plan
        </Button>
      </div>

      {/* Confirmation Modal */}
      {showConfirm && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
          onClick={() => setShowConfirm(false)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
          >
            <Card className="p-8 max-w-md">
              <h3 className="text-2xl font-bold mb-4">Confirm Execution</h3>
              <p className="text-muted-foreground mb-6">
                You are about to apply the <strong>{plan.name}</strong> plan. This will:
              </p>
              <ul className="list-disc list-inside mb-6 space-y-2 text-muted-foreground">
                <li>Free up {formatBytes(plan.space_saved_bytes)} of space</li>
                <li>Execute {plan.actions.length} actions</li>
                <li>Take approximately {formatDuration(plan.estimated_minutes)}</li>
              </ul>
              <div className="flex gap-4">
                <Button variant="ghost" onClick={() => setShowConfirm(false)} className="flex-1">
                  Cancel
                </Button>
                <Button onClick={handleExecute} className="flex-1">
                  Confirm & Execute
                </Button>
              </div>
            </Card>
          </motion.div>
        </motion.div>
      )}
    </div>
  )
}
