import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Progress } from '@/components/ui/progress.jsx'
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
  CheckCircle, 
  XCircle, 
  MessageSquare, 
  Eye, 
  Bot,
  User,
  Euro,
  Calendar,
  AlertTriangle,
  RefreshCw
} from 'lucide-react'

function OffersPanel({ onStatsUpdate }) {
  const [offers, setOffers] = useState([])
  const [selectedOffer, setSelectedOffer] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState(null)
  const [filter, setFilter] = useState('all')
  const [responseData, setResponseData] = useState({
    action: '',
    counter_price: '',
    message: ''
  })
  const [batchSyncStatus, setBatchSyncStatus] = useState(null)
  const [isBatchSyncing, setIsBatchSyncing] = useState(false)
  const [showBatchProgress, setShowBatchProgress] = useState(false)

  useEffect(() => {
    loadOffers()
  }, [filter])

  const loadOffers = async () => {
    try {
      setIsLoading(true)
      const url = filter === 'all' ? '/api/offers' : `/api/offers?status=${filter}`
      const response = await fetch(url)
      const data = await response.json()
      
      if (data.offers) {
        let filteredOffers = data.offers
        
        // Zusätzlicher Client-seitiger Filter für Gegenvorschläge
        if (filter === 'with_counters') {
          filteredOffers = data.offers.filter(offer => 
            offer.counter_amount || offer.counter_message || offer.offer_type === 'counter'
          )
        }
        
        setOffers(filteredOffers)
      } else if (data.error) {
        setMessage({ type: 'error', text: data.error })
      } else {
        setMessage({ type: 'error', text: 'Unbekanntes Datenformat' })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler beim Laden der Angebote' })
    } finally {
      setIsLoading(false)
    }
  }

  const analyzeOffer = async (offerId) => {
    try {
      setIsLoading(true)
      const response = await fetch(`/api/offers/${offerId}/analyze`, { method: 'POST' })
      const data = await response.json()
      
      if (data.success) {
        setMessage({ type: 'success', text: 'Angebot erfolgreich analysiert!' })
        loadOffers()
        if (onStatsUpdate) onStatsUpdate()
      } else {
        setMessage({ type: 'error', text: data.error })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler bei der KI-Analyse' })
    } finally {
      setIsLoading(false)
    }
  }

  const respondToOffer = async (offerId) => {
    try {
      setIsLoading(true)
      const response = await fetch(`/api/offers/${offerId}/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...responseData,
          counter_price: responseData.counter_price ? parseFloat(responseData.counter_price) : null,
          manual_override: true
        })
      })
      const data = await response.json()
      
      if (data.success) {
        setMessage({ type: 'success', text: data.message })
        setSelectedOffer(null)
        setResponseData({ action: '', counter_price: '', message: '' })
        loadOffers()
        if (onStatsUpdate) onStatsUpdate()
      } else {
        setMessage({ type: 'error', text: data.error })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler beim Senden der Antwort' })
    } finally {
      setIsLoading(false)
    }
  }

  const syncOffersSimple = async () => {
    try {
      setIsLoading(true)
      setMessage({ type: 'info', text: 'Synchronisiere Preisvorschläge von eBay...' })
      
      const response = await fetch('/api/offers/sync-simple', { method: 'POST' })
      const data = await response.json()
      
      if (data.success) {
        setMessage({ 
          type: 'success', 
          text: `${data.message} (${data.new_offers} neue, ${data.updated_offers} aktualisierte)`
        })
        loadOffers()
        if (onStatsUpdate) onStatsUpdate()
      } else {
        setMessage({ type: 'error', text: `Synchronisation fehlgeschlagen: ${data.error}` })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler bei der eBay Synchronisation' })
    } finally {
      setIsLoading(false)
    }
  }

  const syncOffersReal = async () => {
    try {
      setIsLoading(true)
      setMessage({ type: 'info', text: 'Sofortige eBay Best Offers Synchronisation...' })
      
      const response = await fetch('/api/offers/sync-working', { method: 'POST' })
      const data = await response.json()
      
      if (data.success) {
        if (data.new_offers > 0) {
          setMessage({ 
            type: 'success', 
            text: `${data.message} (${data.processing_time}) - Quelle: ${data.sources_used ? data.sources_used.join(', ') : 'eBay API'}`
          })
        } else {
          setMessage({ 
            type: 'info', 
            text: `${data.message} (${data.processing_time}). ${data.note || ''}`
          })
        }
        loadOffers()
        if (onStatsUpdate) onStatsUpdate()
      } else {
        setMessage({ 
          type: 'error', 
          text: `Schnelle Synchronisation fehlgeschlagen: ${data.error}`
        })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler bei der schnellen eBay Synchronisation' })
    } finally {
      setIsLoading(false)
    }
  }

  // Neue Batch-Synchronisierung Funktionen
  const startBatchSync = async () => {
    try {
      setIsBatchSyncing(true)
      setShowBatchProgress(true)
      setMessage({ type: 'info', text: 'Starte schrittweise Synchronisierung des gesamten Bestands...' })
      
      const response = await fetch('/api/offers/sync-batch', { method: 'POST' })
      const data = await response.json()
      
      if (data.success) {
        setBatchSyncStatus(data.status)
        // Starte Polling für Status-Updates
        pollBatchStatus()
      } else {
        setMessage({ type: 'error', text: `Batch-Sync konnte nicht gestartet werden: ${data.message}` })
        setIsBatchSyncing(false)
        setShowBatchProgress(false)
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler beim Starten der Batch-Synchronisierung' })
      setIsBatchSyncing(false)
      setShowBatchProgress(false)
    }
  }

  const pollBatchStatus = async () => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch('/api/offers/sync-batch/status')
        const data = await response.json()
        
        setBatchSyncStatus(data.status)
        
        // Prüfe ob Sync abgeschlossen ist
        if (!data.status.active) {
          clearInterval(pollInterval)
          setIsBatchSyncing(false)
          
          // Zeige Abschluss-Nachricht
          if (data.status.found_offers > 0) {
            setMessage({ 
              type: 'success', 
              text: `Batch-Sync abgeschlossen! ${data.status.found_offers} Best Offers gefunden, ${data.status.errors} Fehler`
            })
          } else {
            setMessage({ 
              type: 'info', 
              text: `Batch-Sync abgeschlossen. ${data.status.status_message}`
            })
          }
          
          // Aktualisiere Angebote
          loadOffers()
          if (onStatsUpdate) onStatsUpdate()
          
          // Verstecke Progress nach 5 Sekunden
          setTimeout(() => setShowBatchProgress(false), 5000)
        }
      } catch (err) {
        console.error('Fehler beim Abfragen des Batch-Status:', err)
      }
    }, 2000) // Alle 2 Sekunden aktualisieren
  }

  const stopBatchSync = async () => {
    try {
      const response = await fetch('/api/offers/sync-batch/stop', { method: 'POST' })
      const data = await response.json()
      
      if (data.success) {
        setMessage({ type: 'info', text: 'Batch-Synchronisierung gestoppt' })
      } else {
        setMessage({ type: 'error', text: data.message })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Fehler beim Stoppen der Batch-Synchronisierung' })
    }
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { variant: 'secondary', text: 'Wartend', icon: RefreshCw },
      accepted: { variant: 'default', text: 'Angenommen', icon: CheckCircle },
      rejected: { variant: 'destructive', text: 'Abgelehnt', icon: XCircle },
      countered: { variant: 'outline', text: 'Gegenangebot', icon: MessageSquare }
    }
    
    const config = statusConfig[status] || statusConfig.pending
    const Icon = config.icon
    
    return (
      <Badge variant={config.variant} className="flex items-center space-x-1">
        <Icon className="h-3 w-3" />
        <span>{config.text}</span>
      </Badge>
    )
  }

  const getOfferTypeBadge = (offer) => {
    const offerType = offer.offer_type || 'initial'
    const hasCounter = offer.counter_amount || offer.counter_message
    
    if (offerType === 'counter' || hasCounter) {
      return (
        <Badge variant="secondary" className="flex items-center space-x-1 bg-blue-100 text-blue-800">
          <MessageSquare className="h-3 w-3" />
          <span>Gegenvorschlag</span>
        </Badge>
      )
    }
    
    return (
      <Badge variant="outline" className="flex items-center space-x-1">
        <User className="h-3 w-3" />
        <span>Erstangebot</span>
      </Badge>
    )
  }

  const formatPrice = (price) => {
    if (typeof price === 'string') {
      const numericValue = parseFloat(price.replace(/[^\d.,]/g, '').replace(',', '.'))
      if (isNaN(numericValue)) return price // Return original if can't parse
      return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR'
      }).format(numericValue)
    }
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR'
    }).format(price || 0)
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Unbekannt'
    try {
      return new Date(dateString).toLocaleString('de-DE')
    } catch (error) {
      return dateString // Return original if can't parse
    }
  }

  const getOfferDetails = (offer) => {
    const parsePrice = (priceStr) => {
      if (typeof priceStr === 'number') return priceStr
      if (typeof priceStr === 'string') {
        const numericValue = parseFloat(priceStr.replace(/[^\d.,]/g, '').replace(',', '.'))
        return isNaN(numericValue) ? 0 : numericValue
      }
      return 0
    }
    
    const originalPrice = parsePrice(offer.original_price || offer.list_price)
    const offerAmount = parsePrice(offer.offer_amount)
    const percentage = originalPrice > 0 ? (offerAmount / originalPrice) * 100 : 0
    const hasCounter = offer.counter_amount || offer.counter_message
    
    return {
      percentage: percentage.toFixed(1),
      hasCounter,
      counterAmount: offer.counter_amount,
      counterMessage: offer.counter_message
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

      {/* Filter und Aktionen */}
      <Card>
        <CardHeader>
          <CardTitle>Preisvorschläge verwalten</CardTitle>
          <CardDescription>
            Übersicht und Verwaltung aller eingegangenen Preisvorschläge
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2 mb-4">
            <Button
              variant={filter === 'all' ? 'default' : 'outline'}
              onClick={() => setFilter('all')}
              size="sm"
            >
              Alle
            </Button>
            <Button
              variant={filter === 'pending' ? 'default' : 'outline'}
              onClick={() => setFilter('pending')}
              size="sm"
            >
              Wartend
            </Button>
            <Button
              variant={filter === 'accepted' ? 'default' : 'outline'}
              onClick={() => setFilter('accepted')}
              size="sm"
            >
              Angenommen
            </Button>
            <Button
              variant={filter === 'rejected' ? 'default' : 'outline'}
              onClick={() => setFilter('rejected')}
              size="sm"
            >
              Abgelehnt
            </Button>
            <Button
              variant={filter === 'countered' ? 'default' : 'outline'}
              onClick={() => setFilter('countered')}
              size="sm"
            >
              Gegenangebote
            </Button>
            <Button
              variant={filter === 'with_counters' ? 'default' : 'outline'}
              onClick={() => setFilter('with_counters')}
              size="sm"
            >
              Mit Gegenvorschlägen
            </Button>
          </div>

          <div className="flex space-x-2 mb-4">
            <Button onClick={loadOffers} disabled={isLoading}>
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Aktualisieren
            </Button>
            <Button 
              onClick={syncOffersSimple} 
              disabled={isLoading} 
              variant="outline"
              className="bg-green-50 hover:bg-green-100"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              eBay Synchronisation
            </Button>
            <Button 
              onClick={syncOffersReal} 
              disabled={isLoading} 
              variant="outline"
              className="bg-orange-50 hover:bg-orange-100"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Echte Best Offers
            </Button>
            <Button 
              onClick={startBatchSync} 
              disabled={isLoading || isBatchSyncing} 
              variant="outline"
              className="bg-purple-50 hover:bg-purple-100"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading || isBatchSyncing ? 'animate-spin' : ''}`} />
              Batch-Sync
            </Button>
            {isBatchSyncing && (
              <Button 
                onClick={stopBatchSync} 
                disabled={isLoading || !isBatchSyncing} 
                variant="outline"
                className="bg-red-50 hover:bg-red-100"
              >
                <XCircle className="h-4 w-4 mr-2" />
                Stoppen
              </Button>
            )}
          </div>

          {showBatchProgress && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <h3 className="font-medium mb-2">Batch-Synchronisierung läuft...</h3>
              <p className="text-sm text-gray-700 mb-2">
                Status: {batchSyncStatus?.status_message || 'Lädt...'}
              </p>
              <Progress 
                value={
                  batchSyncStatus?.total_items > 0 
                    ? Math.round((batchSyncStatus.processed_items / batchSyncStatus.total_items) * 100)
                    : 0
                } 
                className="h-2" 
              />
              <div className="flex justify-between text-xs text-gray-500 mt-2">
                <span>
                  {batchSyncStatus?.processed_items || 0} / {batchSyncStatus?.total_items || 0} Artikel
                </span>
                <span>
                  Batch {batchSyncStatus?.current_batch || 0} | 
                  Gefunden: {batchSyncStatus?.found_offers || 0} | 
                  Fehler: {batchSyncStatus?.errors || 0}
                </span>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Angebots-Tabelle */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Artikel</TableHead>
                <TableHead>Käufer</TableHead>
                <TableHead>Angebotspreis</TableHead>
                <TableHead>Angebot</TableHead>
                <TableHead>Typ</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>KI-Entscheidung</TableHead>
                <TableHead>Datum</TableHead>
                <TableHead>Aktionen</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {offers.map((offer) => {
                const offerDetails = getOfferDetails(offer)
                return (
                  <TableRow key={offer.id}>
                    <TableCell>
                      <div className="max-w-xs truncate" title={offer.item_title}>
                        {offer.item_title}
                      </div>
                      <div className="text-sm text-gray-500">
                        ID: {offer.item_id}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <User className="h-4 w-4" />
                        <span>{offer.buyer_username}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="font-medium">{formatPrice(offer.original_price || offer.list_price)}</div>
                    </TableCell>
                    <TableCell>
                      <div className="font-medium text-blue-600">
                        {formatPrice(offer.offer_amount)}
                      </div>
                      <div className="text-sm text-gray-500">
                        {offerDetails.percentage}%
                      </div>
                      {offerDetails.hasCounter && (
                        <div className="text-xs text-orange-600 mt-1">
                          Gegenvorschlag: {formatPrice(offerDetails.counterAmount)}
                        </div>
                      )}
                    </TableCell>
                    <TableCell>
                      {getOfferTypeBadge(offer)}
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(offer.status)}
                    </TableCell>
                    <TableCell>
                      {offer.ai_recommendation ? (
                        <div className="flex items-center space-x-2">
                          <Bot className="h-4 w-4 text-blue-500" />
                          <div className="flex flex-col">
                            <span className="font-medium text-sm">{offer.ai_recommendation.recommendation}</span>
                            <span className="text-xs text-gray-500">
                              {offer.ai_recommendation.confidence}% sicher
                            </span>
                          </div>
                        </div>
                      ) : (
                        <div className="flex items-center space-x-2 text-gray-400">
                          <Bot className="h-4 w-4" />
                          <span className="text-sm">Wird analysiert...</span>
                        </div>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Calendar className="h-4 w-4" />
                        <span className="text-sm">{formatDate(offer.created_date || offer.created_at)}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => setSelectedOffer(offer)}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                          </DialogTrigger>
                        <DialogContent className="max-w-2xl">
                          <DialogHeader>
                            <DialogTitle>Angebot bearbeiten</DialogTitle>
                            <DialogDescription>
                              Antworten Sie auf den Preisvorschlag von {offer.buyer_username}
                            </DialogDescription>
                          </DialogHeader>
                          
                          {selectedOffer && (
                            <div className="space-y-6">
                              {/* Angebots-Details */}
                              <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                                <div>
                                  <Label className="text-sm font-medium">Artikel</Label>
                                  <p className="text-sm font-bold">{selectedOffer.item_title}</p>
                                </div>
                                <div>
                                  <Label className="text-sm font-medium">Angebotspreis</Label>
                                  <p className="text-sm font-bold">{formatPrice(selectedOffer.original_price || selectedOffer.list_price)}</p>
                                </div>
                                <div>
                                  <Label className="text-sm font-medium">Käufer-Angebot</Label>
                                  <p className="text-sm font-bold text-blue-600">
                                    {formatPrice(selectedOffer.offer_amount)}
                                  </p>
                                </div>
                                <div>
                                  <Label className="text-sm font-medium">Prozentsatz</Label>
                                  <p className="text-sm">
                                    {getOfferDetails(selectedOffer).percentage}%
                                  </p>
                                </div>
                              </div>

                              {/* KI-Empfehlung */}
                              {selectedOffer.ai_decision && (
                                <div className="p-4 bg-blue-50 rounded-lg">
                                  <div className="flex items-center space-x-2 mb-2">
                                    <Bot className="h-5 w-5 text-blue-600" />
                                    <Label className="font-medium">KI-Empfehlung</Label>
                                  </div>
                                  <p className="text-sm mb-2">
                                    <strong>Entscheidung:</strong> {selectedOffer.ai_decision}
                                  </p>
                                  {selectedOffer.ai_reasoning && (
                                    <p className="text-sm mb-2">
                                      <strong>Begründung:</strong> {selectedOffer.ai_reasoning}
                                    </p>
                                  )}
                                  {selectedOffer.counter_price && (
                                    <p className="text-sm mb-2">
                                      <strong>Gegenangebot:</strong> {formatPrice(selectedOffer.counter_price)}
                                    </p>
                                  )}
                                  {selectedOffer.response_message && (
                                    <p className="text-sm">
                                      <strong>Nachricht:</strong> {selectedOffer.response_message}
                                    </p>
                                  )}
                                </div>
                              )}

                              {/* Antwort-Formular */}
                              <div className="space-y-4">
                                <div>
                                  <Label>Aktion wählen</Label>
                                  <div className="flex space-x-2 mt-2">
                                    <Button
                                      variant={responseData.action === 'accept' ? 'default' : 'outline'}
                                      onClick={() => setResponseData(prev => ({ ...prev, action: 'accept' }))}
                                      size="sm"
                                    >
                                      <CheckCircle className="h-4 w-4 mr-1" />
                                      Annehmen
                                    </Button>
                                    <Button
                                      variant={responseData.action === 'reject' ? 'default' : 'outline'}
                                      onClick={() => setResponseData(prev => ({ ...prev, action: 'reject' }))}
                                      size="sm"
                                    >
                                      <XCircle className="h-4 w-4 mr-1" />
                                      Ablehnen
                                    </Button>
                                    <Button
                                      variant={responseData.action === 'counter' ? 'default' : 'outline'}
                                      onClick={() => setResponseData(prev => ({ ...prev, action: 'counter' }))}
                                      size="sm"
                                    >
                                      <MessageSquare className="h-4 w-4 mr-1" />
                                      Gegenangebot
                                    </Button>
                                  </div>
                                </div>

                                {responseData.action === 'counter' && (
                                  <div>
                                    <Label htmlFor="counter_price">Gegenangebotspreis (€)</Label>
                                    <Input
                                      id="counter_price"
                                      type="number"
                                      step="0.01"
                                      value={responseData.counter_price}
                                      onChange={(e) => setResponseData(prev => ({ ...prev, counter_price: e.target.value }))}
                                      placeholder="0.00"
                                    />
                                  </div>
                                )}

                                <div>
                                  <Label htmlFor="response_message">Nachricht an Käufer (optional)</Label>
                                  <Textarea
                                    id="response_message"
                                    value={responseData.message}
                                    onChange={(e) => setResponseData(prev => ({ ...prev, message: e.target.value }))}
                                    placeholder="Persönliche Nachricht..."
                                    rows={3}
                                  />
                                </div>

                                <div className="flex justify-end space-x-2">
                                  <Button
                                    variant="outline"
                                    onClick={() => {
                                      setSelectedOffer(null)
                                      setResponseData({ action: '', counter_price: '', message: '' })
                                    }}
                                  >
                                    Abbrechen
                                  </Button>
                                  <Button
                                    onClick={() => respondToOffer(selectedOffer.id)}
                                    disabled={!responseData.action || isLoading}
                                  >
                                    Antwort senden
                                  </Button>
                                </div>
                              </div>
                            </div>
                          )}
                        </DialogContent>
                      </Dialog>
                    </div>
                  </TableCell>
                </TableRow>
                )
              })}
            </TableBody>
          </Table>
          
          {offers.length === 0 && !isLoading && (
            <div className="text-center py-8 text-gray-500">
              Keine Angebote gefunden
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default OffersPanel

