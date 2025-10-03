import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useAnalysis() {
  return useQuery({
    queryKey: ['analysis'],
    queryFn: api.analyze,
    staleTime: 30000, // 30 seconds
  })
}
