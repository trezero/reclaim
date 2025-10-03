import { motion } from 'framer-motion'
import { Save, Shield, Clock, Sparkles, ShieldAlert, AlertTriangle } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Plan } from '@/types/api'
import { formatBytes, formatDuration, getRiskBadgeColor } from '@/lib/utils'

interface PlanCardProps {
  plan: Plan
  index: number
  onViewDetails: () => void
}

export function PlanCard({ plan, index, onViewDetails }: PlanCardProps) {
  const riskIcons = {
    low: Shield,
    medium: ShieldAlert,
    high: AlertTriangle,
  }

  const RiskIcon = riskIcons[plan.risk_level]

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.2, type: 'spring', bounce: 0.3 }}
    >
      <Card
        className={`p-6 transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 hover:scale-[1.02] ${
          plan.recommended
            ? 'border-primary border-2 bg-gradient-to-br from-primary/5 to-accent/5'
            : ''
        }`}
      >
        <h3 className="text-2xl font-bold tracking-wide uppercase mb-6">{plan.name}</h3>

        <div className="space-y-4 mb-6">
          <div className="flex items-center gap-3 text-lg">
            <Save className="w-5 h-5" />
            <span className="font-semibold font-mono">{formatBytes(plan.space_saved_bytes)}</span>
          </div>

          <div className="flex items-center gap-3 text-lg">
            <RiskIcon className="w-5 h-5" />
            <span className={`font-semibold capitalize ${getRiskBadgeColor(plan.risk_level)}`}>
              {plan.risk_level} Risk
            </span>
          </div>

          <div className="flex items-center gap-3 text-lg">
            <Clock className="w-5 h-5" />
            <span className="font-semibold font-mono">{formatDuration(plan.estimated_minutes)}</span>
          </div>
        </div>

        <p className="text-muted-foreground mb-6 leading-relaxed">{plan.rationale}</p>

        <Button
          onClick={onViewDetails}
          variant={plan.recommended ? 'primary' : 'secondary'}
          className="w-full"
        >
          View Plan
        </Button>

        {plan.recommended && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 + index * 0.2, duration: 0.8, type: 'spring', bounce: 0.4 }}
            className="mt-4 gradient-success text-white px-4 py-2 rounded-lg text-center font-semibold flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            RECOMMENDED
          </motion.div>
        )}
      </Card>
    </motion.div>
  )
}
