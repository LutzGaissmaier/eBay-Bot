import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Switch } from '@/components/ui/switch.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import RulesManagement from '../management/RulesManagement.jsx'
import { 
  Save, 
  TestTube, 
  CheckCircle, 
  XCircle, 
  Key, 
  Settings, 
  Bot,
  AlertTriangle,
  Info
} from 'lucide-react'

function SettingsPanel() {
  const [settings, setSettings] = useState({
    ebay_app_id: '',
    ebay_dev_id: '',
    ebay_cert_id: '',
    ebay_auth_token: '',
    openai_api_key: '',
    use_sandbox: 'true',
    auto_mode: 'false'
  })

  const [testResults, setTestResults] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      const response = await fetch('/api/settings')
      const data = await response.json()
      if (data.success) {
        setSettings(data.settings)
      }
    } catch (err) {
      console.error('Fehler beim Laden der Einstellungen:', err)
    }
  }

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  const saveSettings = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      })
      
      const data = await response.json()
      
      if (data.success) {
        setMessage({ text: 'Einstellungen erfolgreich gespeichert', type: 'success' })
      } else {
        setMessage({ text: 'Fehler beim Speichern der Einstellungen', type: 'error' })
      }
    } catch (err) {
      console.error('Fehler beim Speichern:', err)
      setMessage({ text: 'Fehler beim Speichern der Einstellungen', type: 'error' })
    } finally {
      setIsLoading(false)
      setTimeout(() => setMessage(null), 3000)
    }
  }

  const testConnection = async (service) => {
    try {
      setIsLoading(true)
      const response = await fetch(`/api/test-${service}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      })
      
      const data = await response.json()
      setTestResults(prev => ({ ...prev, [service]: data }))
    } catch (err) {
      console.error(`Fehler beim Testen von ${service}:`, err)
      setTestResults(prev => ({ 
        ...prev, 
        [service]: { success: false, message: 'Verbindungstest fehlgeschlagen' }
      }))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {message && (
        <Alert className={message.type === 'error' ? 'border-red-500 bg-red-50' : 'border-green-500 bg-green-50'}>
          <AlertDescription className={message.type === 'error' ? 'text-red-700' : 'text-green-700'}>
            {message.text}
          </AlertDescription>
        </Alert>
      )}

      <Tabs defaultValue="api" className="space-y-6">
        <TabsList className="grid w-full grid-cols-1 md:grid-cols-3 gap-1">
          <TabsTrigger value="api" className="flex items-center justify-center space-x-1 md:space-x-2 text-xs md:text-sm px-2 py-2">
            <Key className="h-3 w-3 md:h-4 md:w-4" />
            <span className="hidden sm:inline">API-Konfiguration</span>
            <span className="sm:hidden">API</span>
          </TabsTrigger>
          <TabsTrigger value="rules" className="flex items-center justify-center space-x-1 md:space-x-2 text-xs md:text-sm px-2 py-2">
            <Bot className="h-3 w-3 md:h-4 md:w-4" />
            <span className="hidden sm:inline">Verhandlungsregeln</span>
            <span className="sm:hidden">Regeln</span>
          </TabsTrigger>
          <TabsTrigger value="behavior" className="flex items-center justify-center space-x-1 md:space-x-2 text-xs md:text-sm px-2 py-2">
            <Settings className="h-3 w-3 md:h-4 md:w-4" />
            <span>Verhalten</span>
          </TabsTrigger>
        </TabsList>

        {/* API-Konfiguration */}
        <TabsContent value="api" className="space-y-6">
          {/* eBay API Einstellungen */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <span>eBay API Konfiguration</span>
                {testResults.ebay && (
                  <Badge variant={testResults.ebay.success ? 'default' : 'destructive'}>
                    {testResults.ebay.success ? 'Verbunden' : 'Fehler'}
                  </Badge>
                )}
              </CardTitle>
              <CardDescription>
                Konfigurieren Sie Ihre eBay Trading API Zugangsdaten
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="ebay_app_id">Application ID</Label>
                  <Input
                    id="ebay_app_id"
                    value={settings.ebay_app_id || ''}
                    onChange={(e) => updateSetting('ebay_app_id', e.target.value)}
                    placeholder="Ihre eBay App ID"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="ebay_dev_id">Developer ID</Label>
                  <Input
                    id="ebay_dev_id"
                    value={settings.ebay_dev_id || ''}
                    onChange={(e) => updateSetting('ebay_dev_id', e.target.value)}
                    placeholder="Ihre eBay Dev ID"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="ebay_cert_id">Certificate ID</Label>
                <Input
                  id="ebay_cert_id"
                  value={settings.ebay_cert_id || ''}
                  onChange={(e) => updateSetting('ebay_cert_id', e.target.value)}
                  placeholder="Ihr eBay Certificate"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="ebay_auth_token">Auth Token</Label>
                <Textarea
                  id="ebay_auth_token"
                  value={settings.ebay_auth_token || ''}
                  onChange={(e) => updateSetting('ebay_auth_token', e.target.value)}
                  placeholder="Ihr eBay Auth Token"
                  rows={3}
                />
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="use_sandbox"
                  checked={settings.use_sandbox === 'true'}
                  onCheckedChange={(checked) => updateSetting('use_sandbox', checked.toString())}
                />
                <Label htmlFor="use_sandbox">Sandbox-Modus verwenden</Label>
              </div>

              <div className="flex space-x-2">
                <Button onClick={() => testConnection('ebay')} disabled={isLoading}>
                  <TestTube className="h-4 w-4 mr-2" />
                  Verbindung testen
                </Button>
              </div>

              {testResults.ebay && (
                <Alert variant={testResults.ebay.success ? 'default' : 'destructive'}>
                  {testResults.ebay.success ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
                  <AlertDescription>{testResults.ebay.message}</AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* OpenAI API Einstellungen */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <span>OpenAI API Konfiguration</span>
                {testResults.openai && (
                  <Badge variant={testResults.openai.success ? 'default' : 'destructive'}>
                    {testResults.openai.success ? 'Verbunden' : 'Fehler'}
                  </Badge>
                )}
              </CardTitle>
              <CardDescription>
                Konfigurieren Sie Ihren OpenAI API Key für KI-Entscheidungen
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="openai_api_key">OpenAI API Key</Label>
                <Input
                  id="openai_api_key"
                  type="password"
                  value={settings.openai_api_key || ''}
                  onChange={(e) => updateSetting('openai_api_key', e.target.value)}
                  placeholder="sk-..."
                />
              </div>

              <div className="flex space-x-2">
                <Button onClick={() => testConnection('openai')} disabled={isLoading}>
                  <TestTube className="h-4 w-4 mr-2" />
                  Verbindung testen
                </Button>
              </div>

              {testResults.openai && (
                <Alert variant={testResults.openai.success ? 'default' : 'destructive'}>
                  {testResults.openai.success ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
                  <AlertDescription>{testResults.openai.message}</AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          <div className="flex justify-end">
            <Button onClick={saveSettings} disabled={isLoading}>
              <Save className="h-4 w-4 mr-2" />
              Einstellungen speichern
            </Button>
          </div>
        </TabsContent>

        {/* Verhandlungsregeln */}
        <TabsContent value="rules" className="space-y-6">
          <RulesManagement />
        </TabsContent>

        {/* Verhalten */}
        <TabsContent value="behavior" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Menschliches Verhalten</CardTitle>
              <CardDescription>
                Einstellungen für natürliches, menschliches Verhalten des Bots
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Alert>
                <Info className="h-4 w-4" />
                <AlertDescription>
                  Der Bot simuliert automatisch menschliches Verhalten durch:
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>Zufällige Antwortzeiten (2-30 Minuten je nach Tageszeit)</li>
                    <li>Natürliche Sprachvariationen in Nachrichten</li>
                    <li>Gelegentliche "menschliche" Unperfektion</li>
                    <li>Rate-Limiting und Pausen zwischen Aktionen</li>
                  </ul>
                </AlertDescription>
              </Alert>

              <div className="flex items-center space-x-2">
                <Switch
                  id="auto_mode"
                  checked={settings.auto_mode === 'true'}
                  onCheckedChange={(checked) => updateSetting('auto_mode', checked.toString())}
                />
                <Label htmlFor="auto_mode">Automatischer Modus</Label>
              </div>
              <p className="text-sm text-gray-500">
                Wenn aktiviert, antwortet der Bot automatisch auf neue Angebote basierend auf den Verhandlungsregeln.
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default SettingsPanel

