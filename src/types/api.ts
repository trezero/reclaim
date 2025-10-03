export interface Drive {
  letter: string
  total_bytes: number
  used_bytes: number
  free_bytes: number
  percent_used: number
  status: 'critical' | 'warning' | 'healthy'
}

export interface SpaceConsumer {
  name: string
  path: string
  size_bytes: number
  type: 'docker' | 'wsl' | 'downloads' | 'temp' | 'cache' | 'other'
}

export interface AnalysisReport {
  drives: Drive[]
  top_consumers: SpaceConsumer[]
  total_recoverable_bytes: number
  has_imbalance: boolean
  imbalance_message?: string
}

export interface PlanAction {
  id: string
  type: 'MOVE' | 'PRUNE' | 'DELETE_TO_RECYCLE' | 'EXPORT_IMPORT_WSL' | 'CLEANUP'
  description: string
  source_path?: string
  target_path?: string
  size_bytes: number
  safety_explanation: string
  rollback_option: string
  command?: string
}

export interface Plan {
  id: string
  name: 'Conservative' | 'Balanced' | 'Aggressive'
  space_saved_bytes: number
  risk_level: 'low' | 'medium' | 'high'
  estimated_minutes: number
  rationale: string
  actions: PlanAction[]
  recommended: boolean
}

export interface ExecutionStep {
  id: string
  action_id: string
  status: 'pending' | 'active' | 'completed' | 'failed'
  description: string
  progress_percent?: number
  error_message?: string
}

export interface ExecutionProgress {
  plan_id: string
  overall_percent: number
  current_step: number
  total_steps: number
  steps: ExecutionStep[]
  logs: LogEntry[]
  status: 'running' | 'completed' | 'failed' | 'cancelled'
}

export interface LogEntry {
  timestamp: string
  level: 'info' | 'success' | 'warning' | 'error'
  message: string
}

export interface Settings {
  use_ai: boolean
  ai_provider: 'openai' | 'anthropic' | null
  api_key: string
  dry_run: boolean
  use_recycle_bin: boolean
  create_backups: boolean
  primary_target_drive: string
  secondary_target_drive: string
  backup_location: string
  backend_url: string
}

export interface ExecuteRequest {
  plan_id: string
  dry_run?: boolean
}

export interface ExecuteResponse {
  execution_id: string
  status: string
}
