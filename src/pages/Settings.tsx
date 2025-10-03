import { useState, useEffect } from 'react'
import { ArrowLeft, Save } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useSettings } from '@/hooks/useSettings'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { Toggle } from '@/components/ui/Toggle'
import { Settings as SettingsType } from '@/types/api'

export function Settings() {
  const navigate = useNavigate()
  const { settings, isLoading, updateSettings, isUpdating } = useSettings()
  const [formData, setFormData] = useState<Partial<SettingsType>>({})

  useEffect(() => {
    if (settings) {
      setFormData(settings)
    }
  }, [settings])

  const handleSave = async () => {
    try {
      await updateSettings(formData)
      navigate('/')
    } catch (error) {
      console.error('Failed to save settings:', error)
    }
  }

  const handleReset = () => {
    if (settings) {
      setFormData(settings)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading settings...</p>
      </div>
    )
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/')} className="p-2">
          <ArrowLeft className="w-6 h-6" />
        </Button>
        <h1 className="text-3xl font-bold">Settings</h1>
      </div>

      {/* AI Configuration */}
      <Card className="p-6">
        <h3 className="text-xl font-semibold uppercase tracking-wide mb-6 text-primary">
          AI Configuration
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 rounded-lg hover:bg-muted/50 transition-colors">
            <span className="font-medium">Enable AI Recommendations</span>
            <Toggle
              checked={formData.use_ai || false}
              onCheckedChange={(checked) => setFormData({ ...formData, use_ai: checked })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Provider</label>
            <select
              value={formData.ai_provider || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  ai_provider: e.target.value as 'openai' | 'anthropic',
                })
              }
              className="w-full p-3 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Select provider</option>
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">API Key</label>
            <div className="flex gap-3">
              <input
                type="password"
                value={formData.api_key || ''}
                onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                placeholder="sk-..."
                className="flex-1 p-3 border border-border rounded-lg bg-background font-mono focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <Button variant="secondary">Test</Button>
            </div>
          </div>
        </div>
      </Card>

      {/* Safety Settings */}
      <Card className="p-6">
        <h3 className="text-xl font-semibold uppercase tracking-wide mb-6 text-primary">
          Safety Settings
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 rounded-lg hover:bg-muted/50 transition-colors">
            <div>
              <p className="font-medium">Dry Run Mode</p>
              <p className="text-sm text-muted-foreground">Preview only, no changes</p>
            </div>
            <Toggle
              checked={formData.dry_run || false}
              onCheckedChange={(checked) => setFormData({ ...formData, dry_run: checked })}
            />
          </div>

          <div className="flex items-center justify-between p-4 rounded-lg hover:bg-muted/50 transition-colors">
            <div>
              <p className="font-medium">Use Recycle Bin</p>
              <p className="text-sm text-muted-foreground">Move to recycle bin vs permanent delete</p>
            </div>
            <Toggle
              checked={formData.use_recycle_bin || false}
              onCheckedChange={(checked) => setFormData({ ...formData, use_recycle_bin: checked })}
            />
          </div>

          <div className="flex items-center justify-between p-4 rounded-lg hover:bg-muted/50 transition-colors">
            <div>
              <p className="font-medium">Create Backups</p>
              <p className="text-sm text-muted-foreground">
                Backup before major operations
              </p>
            </div>
            <Toggle
              checked={formData.create_backups || false}
              onCheckedChange={(checked) => setFormData({ ...formData, create_backups: checked })}
            />
          </div>
        </div>
      </Card>

      {/* Default Targets */}
      <Card className="p-6">
        <h3 className="text-xl font-semibold uppercase tracking-wide mb-6 text-primary">
          Default Targets
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Primary Target Drive</label>
            <select
              value={formData.primary_target_drive || ''}
              onChange={(e) =>
                setFormData({ ...formData, primary_target_drive: e.target.value })
              }
              className="w-full p-3 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Select drive</option>
              <option value="D:">D:</option>
              <option value="E:">E:</option>
              <option value="F:">F:</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Secondary Target Drive</label>
            <select
              value={formData.secondary_target_drive || ''}
              onChange={(e) =>
                setFormData({ ...formData, secondary_target_drive: e.target.value })
              }
              className="w-full p-3 border border-border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Select drive</option>
              <option value="D:">D:</option>
              <option value="E:">E:</option>
              <option value="F:">F:</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Backup Location</label>
            <div className="flex gap-3">
              <input
                type="text"
                value={formData.backup_location || ''}
                onChange={(e) => setFormData({ ...formData, backup_location: e.target.value })}
                placeholder="D:\Backups\"
                className="flex-1 p-3 border border-border rounded-lg bg-background font-mono focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <Button variant="secondary">Browse</Button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Backend URL</label>
            <input
              type="text"
              value={formData.backend_url || ''}
              onChange={(e) => setFormData({ ...formData, backend_url: e.target.value })}
              placeholder="http://127.0.0.1:8000"
              className="w-full p-3 border border-border rounded-lg bg-background font-mono focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
      </Card>

      {/* Actions */}
      <div className="flex justify-end gap-4">
        <Button variant="ghost" onClick={handleReset}>
          Reset
        </Button>
        <Button onClick={handleSave} disabled={isUpdating}>
          <Save className="w-5 h-5" />
          {isUpdating ? 'Saving...' : 'Save Settings'}
        </Button>
      </div>
    </div>
  )
}
