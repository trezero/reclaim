import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { HardDrive, Settings as SettingsIcon } from 'lucide-react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Dashboard } from '@/pages/Dashboard'
import { Plans } from '@/pages/Plans'
import { PlanDetails } from '@/pages/PlanDetails'
import { Execution } from '@/pages/Execution'
import { Settings } from '@/pages/Settings'
import { Button } from '@/components/ui/Button'

function AppHeader() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <header className="bg-card border-b border-border px-6 py-4">
      <div className="flex justify-between items-center max-w-7xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-3 hover:opacity-80 transition-opacity"
        >
          <HardDrive className="w-6 h-6" />
          <h1 className="text-xl font-semibold">Storage Manager</h1>
        </button>

        <div className="flex gap-3">
          {location.pathname !== '/settings' && (
            <Button variant="ghost" onClick={() => navigate('/settings')}>
              <SettingsIcon className="w-5 h-5" />
              Settings
            </Button>
          )}
        </div>
      </div>
    </header>
  )
}

function AppContent() {
  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      <main className="p-8 max-w-7xl mx-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/plans" element={<Plans />} />
          <Route path="/plan/:planId" element={<PlanDetails />} />
          <Route path="/execution" element={<Execution />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  )
}

export default App
