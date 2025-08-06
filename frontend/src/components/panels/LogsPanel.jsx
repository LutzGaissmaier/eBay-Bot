import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table.jsx'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog.jsx'
import { 
  Clock, 
  Eye, 
  Bot,
  User,
  MessageSquare,
  CheckCircle,
  XCircle,
  RefreshCw,
  Search,
  Filter,
  Download,
  AlertTriangle,
  Info,
  Activity
} from 'lucide-react'

function LogsPanel() {
  const [logs, setLogs] = useState([])
  const [filteredLogs, setFilteredLogs] = useState([])
  const [selectedLog, setSelectedLog] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [actionFilter, setActionFilter] = useState('all')
  const [dateFilter, setDateFilter] = useState('all')

  useEffect(() => {
    loadLogs()
  }, [])

  useEffect(() => {
    filterLogs()
  }, [logs, searchTerm, actionFilter, dateFilter])

  const loadLogs = async () => {
    try {
      setIsLoading(true)
      
      // Lade Logs direkt von der Backend-API
      const logsResponse = await fetch('/api/logs')
      const logsData = await logsResponse.json()
      
      if (logsData.logs) {
        // Sortiere nach Datum (neueste zuerst)
        const sortedLogs = logsData.logs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        setLogs(sortedLogs)
      } else {
        setMessage({ type: 'error', text: 'Keine Logs gefunden' })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler beim Laden der Protokolle' })
    } finally {
      setIsLoading(false)
    }
  }

  const filterLogs = () => {
    let filtered = [...logs]

    // Textsuche
    if (searchTerm) {
      filtered = filtered.filter(log => 
        log.message?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.action?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.level?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Aktionsfilter
    if (actionFilter !== 'all') {
      filtered = filtered.filter(log => log.action === actionFilter)
    }

    // Datumsfilter
    if (dateFilter !== 'all') {
      const now = new Date()
      const filterDate = new Date()
      
      switch (dateFilter) {
        case 'today':
          filterDate.setHours(0, 0, 0, 0)
          break
        case 'week':
          filterDate.setDate(now.getDate() - 7)
          break
        case 'month':
          filterDate.setMonth(now.getMonth() - 1)
          break
      }
      
      if (dateFilter !== 'all') {
        filtered = filtered.filter(log => new Date(log.timestamp) >= filterDate)
      }
    }

    setFilteredLogs(filtered)
  }

  const getActionBadge = (action) => {
    const actionConfig = {
      received: { variant: 'secondary', text: 'Empfangen', icon: MessageSquare, color: 'blue' },
      ai_analyzed: { variant: 'outline', text: 'KI-Analyse', icon: Bot, color: 'purple' },
      response_sent: { variant: 'default', text: 'Antwort gesendet', icon: CheckCircle, color: 'green' },
      manual_override: { variant: 'destructive', text: 'Manuell übersteuert', icon: User, color: 'red' },
      error: { variant: 'destructive', text: 'Fehler', icon: AlertTriangle, color: 'red' },
      system_started: { variant: 'outline', text: 'System gestartet', icon: Activity, color: 'green' },
      auto_accept: { variant: 'default', text: 'Auto-Akzeptiert', icon: CheckCircle, color: 'green' },
      auto_decline: { variant: 'destructive', text: 'Auto-Abgelehnt', icon: XCircle, color: 'red' },
      auto_counter: { variant: 'secondary', text: 'Auto-Gegenangebot', icon: MessageSquare, color: 'blue' }
    }
    
    const config = actionConfig[action] || { variant: 'secondary', text: action, icon: Activity, color: 'gray' }
    const Icon = config.icon
    
    return (
      <Badge variant={config.variant} className="flex items-center space-x-1">
        <Icon className="h-3 w-3" />
        <span>{config.text}</span>
      </Badge>
    )
  }

  const getLevelBadge = (level) => {
    const levelConfig = {
      info: { variant: 'outline', text: 'Info', icon: Info, color: 'blue' },
      error: { variant: 'destructive', text: 'Fehler', icon: AlertTriangle, color: 'red' },
      warning: { variant: 'secondary', text: 'Warnung', icon: AlertTriangle, color: 'yellow' },
      success: { variant: 'default', text: 'Erfolg', icon: CheckCircle, color: 'green' }
    }
    
    const config = levelConfig[level] || { variant: 'secondary', text: level, icon: Info, color: 'gray' }
    const Icon = config.icon
    
    return (
      <Badge variant={config.variant} className="flex items-center space-x-1">
        <Icon className="h-3 w-3" />
        <span>{config.text}</span>
      </Badge>
    )
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('de-DE', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR'
    }).format(price)
  }

  const exportLogs = () => {
    const csvContent = [
      ['Zeitstempel', 'Aktion', 'Artikel', 'Käufer', 'Angebotspreis', 'Käufer-Angebot', 'Details'].join(';'),
      ...filteredLogs.map(log => [
        formatDate(log.timestamp),
        log.action,
        log.offer_title || '',
        log.buyer_name || '',
        log.listing_price ? formatPrice(log.listing_price) : '',
        log.offer_price ? formatPrice(log.offer_price) : '',
        log.payload || ''
      ].join(';'))
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `ebay-bot-protokoll-${new Date().toISOString().split('T')[0]}.csv`
    link.click()
  }

  const parsePayload = (payload) => {
    try {
      return JSON.parse(payload)
    } catch {
      return payload
    }
  }

  return (
    <div className="space-y-6">
      {/* Nachricht anzeigen */}
      {message && (
        <Alert variant={message.type === 'error' ? 'destructive' : 'default'}>
          {message.type === 'error' ? <AlertTriangle className="h-4 w-4" /> : <CheckCircle className="h-4 w-4" />}
          <AlertDescription>{message.text}</AlertDescription>
        </Alert>
      )}

      {/* Filter und Suche */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-5 w-5" />
            <span>Aktivitätsprotokoll</span>
          </CardTitle>
          <CardDescription>
            Detaillierte Nachverfolgung aller Bot-Aktivitäten und Entscheidungen
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Suchleiste */}
          <div className="flex items-center space-x-2">
            <Search className="h-4 w-4 text-gray-400" />
            <Input
              placeholder="Suche nach Nachricht, Aktion, Level..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1"
            />
          </div>

          {/* Filter */}
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4" />
              <span className="text-sm font-medium">Aktion:</span>
              <select
                value={actionFilter}
                onChange={(e) => setActionFilter(e.target.value)}
                className="px-3 py-1 border rounded-md text-sm"
              >
                <option value="all">Alle</option>
                <option value="received">Empfangen</option>
                <option value="ai_analyzed">KI-Analyse</option>
                <option value="response_sent">Antwort gesendet</option>
                <option value="manual_override">Manuell übersteuert</option>
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4" />
              <span className="text-sm font-medium">Zeitraum:</span>
              <select
                value={dateFilter}
                onChange={(e) => setDateFilter(e.target.value)}
                className="px-3 py-1 border rounded-md text-sm"
              >
                <option value="all">Alle</option>
                <option value="today">Heute</option>
                <option value="week">Letzte Woche</option>
                <option value="month">Letzter Monat</option>
              </select>
            </div>
          </div>

          {/* Aktionen */}
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-500">
              {filteredLogs.length} von {logs.length} Einträgen
            </div>
            <div className="flex space-x-2">
              <Button onClick={loadLogs} disabled={isLoading} variant="outline" size="sm">
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                Aktualisieren
              </Button>
              <Button onClick={exportLogs} variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Exportieren
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Protokoll-Tabelle */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Zeitstempel</TableHead>
                <TableHead>Level</TableHead>
                <TableHead>Aktion</TableHead>
                <TableHead>Nachricht</TableHead>
                <TableHead>Details</TableHead>
                <TableHead>Aktionen</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLogs.map((log) => (
                <TableRow key={log.id}>
                  <TableCell>
                    <div className="text-sm">{formatDate(log.timestamp)}</div>
                  </TableCell>
                  <TableCell>
                    {getLevelBadge(log.level)}
                  </TableCell>
                  <TableCell>
                    {getActionBadge(log.action)}
                  </TableCell>
                  <TableCell>
                    <div className="max-w-xs">
                      <div className="truncate font-medium" title={log.message}>
                        {log.message || 'N/A'}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="max-w-xs truncate text-sm text-gray-600">
                      {log.details && Object.keys(log.details).length > 0
                        ? JSON.stringify(log.details).substring(0, 50) + '...'
                        : 'Keine Details'
                      }
                    </div>
                  </TableCell>
                  <TableCell>
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => setSelectedLog(log)}
                        >
                          <Eye className="h-4 w-4" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="max-w-2xl">
                        <DialogHeader>
                          <DialogTitle>Protokoll-Details</DialogTitle>
                          <DialogDescription>
                            Detaillierte Informationen zu dieser Aktivität
                          </DialogDescription>
                        </DialogHeader>
                        
                        {selectedLog && (
                          <div className="space-y-4">
                            {/* Grundinformationen */}
                            <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                              <div>
                                <span className="text-sm font-medium text-gray-600">Zeitstempel:</span>
                                <p className="text-sm">{formatDate(selectedLog.timestamp)}</p>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-gray-600">Aktion:</span>
                                <div className="mt-1">{getActionBadge(selectedLog.action)}</div>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-gray-600">Artikel:</span>
                                <p className="text-sm">{selectedLog.offer_title || 'N/A'}</p>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-gray-600">Käufer:</span>
                                <p className="text-sm">{selectedLog.buyer_name || 'N/A'}</p>
                              </div>
                            </div>

                            {/* Preisinformationen */}
                            {selectedLog.listing_price && selectedLog.offer_price && (
                              <div className="p-4 bg-blue-50 rounded-lg">
                                <h4 className="font-medium mb-2">Preisinformationen</h4>
                                <div className="grid grid-cols-3 gap-4 text-sm">
                                  <div>
                                    <span className="text-gray-600">Angebotspreis:</span>
                                    <p className="font-medium">{formatPrice(selectedLog.listing_price)}</p>
                                  </div>
                                  <div>
                                    <span className="text-gray-600">Käufer-Vorschlag:</span>
                                    <p className="font-medium text-blue-600">{formatPrice(selectedLog.offer_price)}</p>
                                  </div>
                                  <div>
                                    <span className="text-gray-600">Prozentsatz:</span>
                                    <p className="font-medium">
                                      {((selectedLog.offer_price / selectedLog.listing_price) * 100).toFixed(1)}%
                                    </p>
                                  </div>
                                </div>
                              </div>
                            )}

                            {/* Payload-Details */}
                            {selectedLog.payload && (
                              <div className="space-y-2">
                                <span className="text-sm font-medium text-gray-600">Detaillierte Informationen:</span>
                                <div className="p-3 bg-gray-100 rounded-lg">
                                  <pre className="text-sm whitespace-pre-wrap overflow-auto max-h-40">
                                    {typeof selectedLog.payload === 'string' 
                                      ? selectedLog.payload 
                                      : JSON.stringify(parsePayload(selectedLog.payload), null, 2)
                                    }
                                  </pre>
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </DialogContent>
                    </Dialog>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          
          {filteredLogs.length === 0 && !isLoading && (
            <div className="text-center py-8 text-gray-500">
              <Activity className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Keine Protokolleinträge gefunden</p>
              <p className="text-sm">Starten Sie den Bot, um Aktivitäten zu protokollieren</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Zusammenfassung */}
      <Card>
        <CardHeader>
          <CardTitle>Protokoll-Zusammenfassung</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <MessageSquare className="h-6 w-6 mx-auto mb-2 text-blue-600" />
              <div className="text-lg font-bold">
                {logs.filter(log => log.action === 'received').length}
              </div>
              <div className="text-sm text-gray-600">Empfangen</div>
            </div>
            
            <div className="text-center p-3 bg-purple-50 rounded-lg">
              <Bot className="h-6 w-6 mx-auto mb-2 text-purple-600" />
              <div className="text-lg font-bold">
                {logs.filter(log => log.action === 'ai_analyzed').length}
              </div>
              <div className="text-sm text-gray-600">KI-Analysen</div>
            </div>
            
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <CheckCircle className="h-6 w-6 mx-auto mb-2 text-green-600" />
              <div className="text-lg font-bold">
                {logs.filter(log => log.action === 'response_sent').length}
              </div>
              <div className="text-sm text-gray-600">Antworten gesendet</div>
            </div>
            
            <div className="text-center p-3 bg-orange-50 rounded-lg">
              <User className="h-6 w-6 mx-auto mb-2 text-orange-600" />
              <div className="text-lg font-bold">
                {logs.filter(log => log.action === 'manual_override').length}
              </div>
              <div className="text-sm text-gray-600">Manuell übersteuert</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default LogsPanel

