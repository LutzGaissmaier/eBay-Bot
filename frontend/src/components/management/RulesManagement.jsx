import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Textarea } from '../ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select'
import { Switch } from '../ui/switch'
import { Badge } from '../ui/badge'
import { Alert, AlertDescription } from '../ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../ui/dialog'
import { Plus, Edit, Trash2, Clock, Settings, CheckCircle, XCircle } from 'lucide-react'

export default function RulesManagement() {
  const [rules, setRules] = useState([])
  const [selectedRule, setSelectedRule] = useState(null)
  const [isEditing, setIsEditing] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [message, setMessage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')

  // Form-Daten für Regel-Editor
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    min_price_percentage: 70,
    auto_accept_percentage: 75,
    auto_decline_percentage: 60,
    max_counter_offers: 2,
    negotiation_tone: 'friendly',
    is_active: false,
    rule_type: 'general',
    time_range_start: 0,
    time_range_end: 999,
    auto_execute_enabled: false,
    auto_counter_enabled: false,
    counter_offer_percentage: 80
  })

  useEffect(() => {
    loadRules()
  }, [])

  const loadRules = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/negotiation-rules')
      const data = await response.json()
      if (data.rules) {
        setRules(data.rules)
      } else if (data.success && data.rules) {
        setRules(data.rules)
      } else {
        console.error('Unexpected API response format:', data)
        showMessage('Unerwartetes API-Format', 'error')
      }
    } catch (err) {
      console.error('Fehler beim Laden der Regeln:', err)
      showMessage('Fehler beim Laden der Regeln', 'error')
    } finally {
      setLoading(false)
    }
  }

  const showMessage = (text, type = 'success') => {
    setMessage({ text, type })
    setTimeout(() => setMessage(null), 3000)
  }

  const handleCreateRule = () => {
    setFormData({
      name: '',
      description: '',
      min_price_percentage: 70,
      auto_accept_threshold: 90,
      auto_reject_threshold: 60,
      max_counter_offers: 2,
      negotiation_tone: 'friendly',
      active: false,
      rule_type: 'general',
      time_range_start: 0,
      time_range_end: 999
    })
    setIsCreating(true)
    setIsEditing(false)
    setSelectedRule(null)
    setActiveTab('editor') // Automatisch zum Editor-Tab wechseln
  }

  const handleEditRule = (rule) => {
    setFormData({ ...rule })
    setSelectedRule(rule)
    setIsEditing(true)
    setIsCreating(false)
    setActiveTab('editor') // Automatisch zum Editor-Tab wechseln
  }

  const handleSaveRule = async () => {
    try {
      setLoading(true)
      
      const url = isCreating 
        ? '/api/negotiation-rules'
        : `/api/negotiation-rules/${selectedRule.id}`
      
      const method = isCreating ? 'POST' : 'PUT'
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      const data = await response.json()
      
      if (data.success) {
        showMessage(data.message)
        await loadRules()
        setIsEditing(false)
        setIsCreating(false)
        setSelectedRule(null)
        setActiveTab('overview') // Zurück zur Übersicht nach dem Speichern
      } else {
        showMessage(data.error || 'Fehler beim Speichern', 'error')
      }
    } catch (err) {
      console.error('Fehler beim Speichern:', err)
      showMessage('Fehler beim Speichern der Regel', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteRule = async (ruleId) => {
    if (!confirm('Sind Sie sicher, dass Sie diese Regel löschen möchten?')) return
    
    try {
      setLoading(true)
      const response = await fetch(`/api/negotiation-rules/${ruleId}`, {
        method: 'DELETE'
      })
      
      const data = await response.json()
      
      if (data.success) {
        showMessage(data.message)
        await loadRules()
      } else {
        showMessage(data.error || 'Fehler beim Löschen', 'error')
      }
    } catch (err) {
      console.error('Fehler beim Löschen:', err)
      showMessage('Fehler beim Löschen der Regel', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleToggleRule = async (ruleId, newActiveState) => {
    try {
      setLoading(true)
      const response = await fetch(`/api/negotiation-rules/${ruleId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: newActiveState })
      })
      
      const data = await response.json()
      
      if (data.success) {
        const action = newActiveState ? 'aktiviert' : 'deaktiviert'
        showMessage(data.message || `Regel erfolgreich ${action}`)
        await loadRules()
      } else {
        showMessage(data.error || 'Fehler beim Ändern der Regel', 'error')
      }
    } catch (err) {
      console.error('Fehler beim Ändern der Regel:', err)
      showMessage('Fehler beim Ändern der Regel', 'error')
    } finally {
      setLoading(false)
    }
  }

  const getRuleTypeLabel = (type) => {
    switch (type) {
      case 'general': return 'Allgemein'
      case 'time_based': return 'Zeitbasiert'
      default: return type
    }
  }

  const getRuleTypeBadgeColor = (type) => {
    switch (type) {
      case 'general': return 'bg-blue-100 text-blue-800'
      case 'time_based': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getTimeRangeText = (rule) => {
    if (rule.rule_type !== 'time_based') return ''
    if (rule.time_range_end >= 999) return `${rule.time_range_start}+ Tage`
    return `${rule.time_range_start}-${rule.time_range_end} Tage`
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

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="overview" className="flex items-center space-x-2">
            <Settings className="h-4 w-4" />
            <span>Regel-Übersicht</span>
          </TabsTrigger>
          <TabsTrigger value="editor" className="flex items-center space-x-2">
            <Edit className="h-4 w-4" />
            <span>Regel-Editor</span>
          </TabsTrigger>
        </TabsList>

        {/* Regel-Übersicht */}
        <TabsContent value="overview" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Verhandlungsregeln</h3>
            <Button onClick={handleCreateRule} className="flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Neue Regel</span>
            </Button>
          </div>

          <div className="grid gap-4">
            {rules.map((rule) => (
              <Card key={rule.id} className={`transition-all ${rule.is_active ? 'ring-2 ring-green-500' : ''}`}>
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2">
                        <CardTitle className="text-base">{rule.name}</CardTitle>
                        {rule.is_active && <CheckCircle className="h-4 w-4 text-green-500" />}
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={getRuleTypeBadgeColor(rule.rule_type)}>
                          {getRuleTypeLabel(rule.rule_type)}
                        </Badge>
                        {rule.rule_type === 'time_based' && (
                          <Badge variant="outline" className="flex items-center space-x-1">
                            <Clock className="h-3 w-3" />
                            <span>{getTimeRangeText(rule)}</span>
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button
                        size="sm"
                        variant={rule.is_active ? "default" : "outline"}
                        onClick={() => handleToggleRule(rule.id, !rule.is_active)}
                        disabled={loading}
                      >
                        {rule.is_active ? "Deaktivieren" : "Aktivieren"}
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleEditRule(rule)}
                        disabled={loading}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleDeleteRule(rule.id)}
                        disabled={loading || rule.is_active}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <CardDescription className="mb-3">{rule.description}</CardDescription>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="font-medium">Mindestpreis:</span>
                      <div>{rule.min_price_percentage}%</div>
                    </div>
                    <div>
                      <span className="font-medium">Auto-Annahme:</span>
                      <div>{rule.auto_accept_percentage}%</div>
                    </div>
                    <div>
                      <span className="font-medium">Auto-Ablehnung:</span>
                      <div>{rule.auto_decline_percentage}%</div>
                    </div>
                    <div>
                      <span className="font-medium">Max. Gegenangebote:</span>
                      <div>{rule.max_counter_offers}</div>
                    </div>
                  </div>
                  
                  {/* Automatisierung-Status */}
                  <div className="mt-4 pt-3 border-t border-gray-200">
                    <div className="flex items-center space-x-4 text-sm">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">Vollautomatik:</span>
                        <Badge variant={rule.auto_execute_enabled ? "default" : "secondary"}>
                          {rule.auto_execute_enabled ? "Aktiv" : "Inaktiv"}
                        </Badge>
                      </div>
                      {rule.auto_counter_enabled && (
                        <div className="flex items-center space-x-2">
                          <span className="font-medium">Gegenangebot:</span>
                          <Badge variant="outline">{rule.counter_offer_percentage}%</Badge>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Regel-Editor */}
        <TabsContent value="editor" className="space-y-4">
          {(isEditing || isCreating) ? (
            <Card>
              <CardHeader>
                <CardTitle>
                  {isCreating ? 'Neue Regel erstellen' : `Regel bearbeiten: ${selectedRule?.name}`}
                </CardTitle>
                <CardDescription>
                  {isCreating 
                    ? 'Erstellen Sie eine neue Verhandlungsregel für Ihre eBay-Angebote'
                    : 'Bearbeiten Sie die Einstellungen dieser Verhandlungsregel'
                  }
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Grundeinstellungen */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Regelname</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      placeholder="Name der Verhandlungsregel"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="rule_type">Regeltyp</Label>
                    <Select
                      value={formData.rule_type}
                      onValueChange={(value) => setFormData({...formData, rule_type: value})}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="general">Allgemeine Regel</SelectItem>
                        <SelectItem value="time_based">Zeitbasierte Regel</SelectItem>
                        <SelectItem value="auto">Vollautomatik-Regel</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Beschreibung</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    placeholder="Beschreibung der Regel..."
                    rows={2}
                  />
                </div>

                {/* Zeitbereich (nur für zeitbasierte Regeln) */}
                {formData.rule_type === 'time_based' && (
                  <div className="grid grid-cols-2 gap-4 p-4 bg-blue-50 rounded-lg">
                    <div className="space-y-2">
                      <Label htmlFor="time_range_start">Von (Tage)</Label>
                      <Input
                        id="time_range_start"
                        type="number"
                        value={formData.time_range_start}
                        onChange={(e) => setFormData({...formData, time_range_start: parseInt(e.target.value)})}
                        min="0"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="time_range_end">Bis (Tage)</Label>
                      <Input
                        id="time_range_end"
                        type="number"
                        value={formData.time_range_end}
                        onChange={(e) => setFormData({...formData, time_range_end: parseInt(e.target.value)})}
                        min="1"
                      />
                    </div>
                  </div>
                )}

                {/* Verhandlungsparameter */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="min_price_percentage">Mindestpreis (%)</Label>
                    <Input
                      id="min_price_percentage"
                      type="number"
                      value={formData.min_price_percentage}
                      onChange={(e) => setFormData({...formData, min_price_percentage: parseFloat(e.target.value)})}
                      min="0"
                      max="100"
                      step="0.1"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="max_counter_offers">Max. Gegenangebote</Label>
                    <Input
                      id="max_counter_offers"
                      type="number"
                      value={formData.max_counter_offers}
                      onChange={(e) => setFormData({...formData, max_counter_offers: parseInt(e.target.value)})}
                      min="1"
                      max="10"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="auto_accept_percentage">Auto-Annahme (%)</Label>
                    <Input
                      id="auto_accept_percentage"
                      type="number"
                      value={formData.auto_accept_percentage}
                      onChange={(e) => setFormData({...formData, auto_accept_percentage: parseFloat(e.target.value)})}
                      min="0"
                      max="100"
                      step="0.1"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="auto_decline_percentage">Auto-Ablehnung (%)</Label>
                    <Input
                      id="auto_decline_percentage"
                      type="number"
                      value={formData.auto_decline_percentage}
                      onChange={(e) => setFormData({...formData, auto_decline_percentage: parseFloat(e.target.value)})}
                      min="0"
                      max="100"
                      step="0.1"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="negotiation_tone">Verhandlungston</Label>
                    <Select
                      value={formData.negotiation_tone}
                      onValueChange={(value) => setFormData({...formData, negotiation_tone: value})}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="friendly">Freundlich</SelectItem>
                        <SelectItem value="professional">Professionell</SelectItem>
                        <SelectItem value="firm">Bestimmt</SelectItem>
                        <SelectItem value="efficient">Effizient</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="flex items-center space-x-2 pt-6">
                    <Switch
                      id="is_active"
                                              checked={formData.is_active}
                        onCheckedChange={(checked) => setFormData({...formData, is_active: checked})}
                    />
                    <Label htmlFor="active">Regel aktivieren</Label>
                  </div>
                </div>

                {/* Automatisierungs-Einstellungen */}
                <div className="p-4 bg-gray-50 rounded-lg space-y-4">
                  <h4 className="font-medium text-gray-900">🤖 Vollautomatik-Einstellungen</h4>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-center space-x-2">
                      <Switch
                        id="auto_execute_enabled"
                        checked={formData.auto_execute_enabled}
                        onCheckedChange={(checked) => setFormData({...formData, auto_execute_enabled: checked})}
                      />
                      <Label htmlFor="auto_execute_enabled">Automatische Ausführung aktivieren</Label>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Switch
                        id="auto_counter_enabled"
                        checked={formData.auto_counter_enabled}
                        onCheckedChange={(checked) => setFormData({...formData, auto_counter_enabled: checked})}
                      />
                      <Label htmlFor="auto_counter_enabled">Automatische Gegenangebote</Label>
                    </div>
                  </div>
                  
                  {formData.auto_counter_enabled && (
                    <div className="space-y-2">
                      <Label htmlFor="counter_offer_percentage">Gegenangebot-Prozentsatz (%)</Label>
                      <Input
                        id="counter_offer_percentage"
                        type="number"
                        value={formData.counter_offer_percentage}
                        onChange={(e) => setFormData({...formData, counter_offer_percentage: parseFloat(e.target.value)})}
                        min="0"
                        max="100"
                        step="0.1"
                        placeholder="z.B. 80 (= 80% des Listpreises)"
                      />
                      <p className="text-xs text-gray-500">
                        Bei Gegenangeboten wird automatisch {formData.counter_offer_percentage}% des Listpreises vorgeschlagen
                      </p>
                    </div>
                  )}
                  
                  {formData.auto_execute_enabled && (
                    <div className="text-xs text-gray-600 p-3 bg-blue-50 rounded border-l-4 border-blue-400">
                      <strong>Vollautomatik aktiviert:</strong> Der Bot entscheidet und handelt komplett selbstständig basierend auf den konfigurierten Schwellenwerten.
                    </div>
                  )}
                </div>

                <div className="flex justify-end space-x-2 pt-4">
                  <Button
                    variant="outline"
                    onClick={() => {
                      setIsEditing(false)
                      setIsCreating(false)
                      setSelectedRule(null)
                      setActiveTab('overview') // Zurück zur Übersicht
                    }}
                    disabled={loading}
                  >
                    Abbrechen
                  </Button>
                  <Button onClick={handleSaveRule} disabled={loading}>
                    {loading ? 'Speichern...' : (isCreating ? 'Regel erstellen' : 'Änderungen speichern')}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Edit className="h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-600 mb-2">Keine Regel ausgewählt</h3>
                <p className="text-gray-500 text-center mb-4">
                  Wählen Sie eine Regel aus der Übersicht zum Bearbeiten aus oder erstellen Sie eine neue Regel.
                </p>
                <Button onClick={handleCreateRule}>
                  <Plus className="h-4 w-4 mr-2" />
                  Neue Regel erstellen
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}

