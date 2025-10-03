import { useMutation } from '@tanstack/react-query'
import { api } from '@/lib/api'
import type { ExecuteRequest } from '@/types/api'

export function useExecutePlan() {
  return useMutation({
    mutationFn: (request: ExecuteRequest) => api.executePlan(request),
  })
}
