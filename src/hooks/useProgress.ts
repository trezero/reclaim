import { useState, useEffect, useCallback } from 'react'
import { api } from '@/lib/api'
import type { ExecutionProgress, LogEntry } from '@/types/api'

export function useProgress(executionId: string | null) {
  const [progress, setProgress] = useState<ExecutionProgress | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    if (!executionId) {
      setProgress(null)
      setIsConnected(false)
      return
    }

    let ws: WebSocket | null = null

    try {
      ws = api.createProgressSocket(executionId)

      ws.onopen = () => {
        setIsConnected(true)
        setError(null)
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as ExecutionProgress
          setProgress(data)
        } catch (err) {
          console.error('Failed to parse progress message:', err)
        }
      }

      ws.onerror = (event) => {
        setError(new Error('WebSocket error occurred'))
        console.error('WebSocket error:', event)
      }

      ws.onclose = () => {
        setIsConnected(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to create WebSocket'))
    }

    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [executionId])

  const disconnect = useCallback(() => {
    setProgress(null)
    setIsConnected(false)
  }, [])

  return {
    progress,
    isConnected,
    error,
    disconnect,
  }
}
