import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function usePlans() {
  return useQuery({
    queryKey: ['plans'],
    queryFn: api.getPlans,
    staleTime: 60000, // 1 minute
  })
}

export function usePlanDetails(planId: string | null) {
  return useQuery({
    queryKey: ['plan', planId],
    queryFn: () => api.getPlan(planId!),
    enabled: !!planId,
    staleTime: 60000,
  })
}
