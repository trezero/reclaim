import { motion } from 'framer-motion'
import { ArrowLeft, Brain, RefreshCw } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { usePlans } from '@/hooks/usePlans'
import { PlanCard } from '@/components/PlanCard'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

export function Plans() {
  const navigate = useNavigate()
  const { data: plans, isLoading, error } = usePlans()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-lg text-muted-foreground">Generating AI recommendations...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="p-8 max-w-md">
          <h2 className="text-xl font-semibold text-center mb-2">Failed to Load Plans</h2>
          <p className="text-muted-foreground text-center mb-4">
            {error instanceof Error ? error.message : 'An error occurred'}
          </p>
          <Button onClick={() => navigate('/')} className="w-full">
            Back to Dashboard
          </Button>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/')} className="p-2">
          <ArrowLeft className="w-6 h-6" />
        </Button>
        <h1 className="text-3xl font-bold">AI Cleanup Recommendations</h1>
      </div>

      {/* Plans Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {plans?.map((plan, index) => (
          <PlanCard
            key={plan.id}
            plan={plan}
            index={index}
            onViewDetails={() => navigate(`/plan/${plan.id}`)}
          />
        ))}
      </div>

      {/* AI Reasoning */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <Card className="glass-light glass-blur border p-6">
          <div className="flex items-center gap-3 mb-4">
            <Brain className="w-6 h-6 text-primary" />
            <h3 className="font-semibold text-lg text-primary">AI Reasoning</h3>
          </div>
          <p className="text-foreground leading-relaxed">
            {plans?.find((p) => p.recommended)?.rationale ||
              'The AI has analyzed your storage patterns and generated optimized cleanup strategies based on safety, effectiveness, and minimal disruption to your workflow.'}
          </p>
        </Card>
      </motion.div>
    </div>
  )
}
