import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { 
  TrendingUp, 
  TrendingDown, 
  CheckCircle, 
  XCircle, 
  MessageSquare,
  Clock
} from 'lucide-react'

function StatsPanel({ stats }) {
  // Daten für Diagramme vorbereiten
  const chartData = [
    {
      name: 'Wartend',
      value: stats.pending_offers,
      color: '#f59e0b'
    },
    {
      name: 'Angenommen',
      value: stats.accepted_offers,
      color: '#10b981'
    },
    {
      name: 'Abgelehnt',
      value: stats.rejected_offers,
      color: '#ef4444'
    },
    {
      name: 'Gegenangebote',
      value: stats.countered_offers,
      color: '#6366f1'
    }
  ]

  const barData = [
    {
      name: 'Wartend',
      count: stats.pending_offers,
      fill: '#f59e0b'
    },
    {
      name: 'Angenommen',
      count: stats.accepted_offers,
      fill: '#10b981'
    },
    {
      name: 'Abgelehnt',
      count: stats.rejected_offers,
      fill: '#ef4444'
    },
    {
      name: 'Gegenangebote',
      count: stats.countered_offers,
      fill: '#6366f1'
    }
  ]

  const COLORS = ['#f59e0b', '#10b981', '#ef4444', '#6366f1']

  const formatPrice = (price) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR'
    }).format(price)
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Erfolgsrate und Trends */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5 text-green-500" />
            <span>Erfolgsrate</span>
          </CardTitle>
          <CardDescription>
            Prozentsatz der erfolgreich abgeschlossenen Verhandlungen
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="text-3xl font-bold text-green-600">
            {stats.success_rate}%
          </div>
          <Progress value={stats.success_rate} className="w-full" />
          
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <div className="flex items-center justify-center space-x-2 mb-1">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium">Erfolgreich</span>
              </div>
              <div className="text-lg font-bold text-green-600">
                {stats.accepted_offers + stats.countered_offers}
              </div>
            </div>
            
            <div className="text-center p-3 bg-red-50 rounded-lg">
              <div className="flex items-center justify-center space-x-2 mb-1">
                <XCircle className="h-4 w-4 text-red-600" />
                <span className="text-sm font-medium">Abgelehnt</span>
              </div>
              <div className="text-lg font-bold text-red-600">
                {stats.rejected_offers}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Durchschnittlicher Angebotspreis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <span>Durchschnittlicher Angebotspreis</span>
          </CardTitle>
          <CardDescription>
            Mittlerer Wert aller eingegangenen Preisvorschläge
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold text-blue-600">
            {formatPrice(stats.avg_offer_price || 0)}
          </div>
          
          <div className="mt-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span>Basierend auf {stats.total_offers} Angeboten</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Verteilung der Angebote (Balkendiagramm) */}
      <Card>
        <CardHeader>
          <CardTitle>Angebots-Verteilung</CardTitle>
          <CardDescription>
            Übersicht über den Status aller Preisvorschläge
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Kreisdiagramm */}
      <Card>
        <CardHeader>
          <CardTitle>Status-Übersicht</CardTitle>
          <CardDescription>
            Prozentuale Verteilung der Angebots-Status
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Detaillierte Statistiken */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Detaillierte Statistiken</CardTitle>
          <CardDescription>
            Umfassende Übersicht über alle Bot-Aktivitäten
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 border rounded-lg">
              <Clock className="h-8 w-8 mx-auto mb-2 text-yellow-500" />
              <div className="text-2xl font-bold">{stats.pending_offers}</div>
              <div className="text-sm text-gray-500">Wartende Angebote</div>
            </div>
            
            <div className="text-center p-4 border rounded-lg">
              <CheckCircle className="h-8 w-8 mx-auto mb-2 text-green-500" />
              <div className="text-2xl font-bold">{stats.accepted_offers}</div>
              <div className="text-sm text-gray-500">Angenommene Angebote</div>
            </div>
            
            <div className="text-center p-4 border rounded-lg">
              <XCircle className="h-8 w-8 mx-auto mb-2 text-red-500" />
              <div className="text-2xl font-bold">{stats.rejected_offers}</div>
              <div className="text-sm text-gray-500">Abgelehnte Angebote</div>
            </div>
            
            <div className="text-center p-4 border rounded-lg">
              <MessageSquare className="h-8 w-8 mx-auto mb-2 text-blue-500" />
              <div className="text-2xl font-bold">{stats.countered_offers}</div>
              <div className="text-sm text-gray-500">Gegenangebote</div>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium mb-2">Leistungskennzahlen</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Annahmequote:</span>
                <span className="ml-2 font-medium">
                  {stats.total_offers > 0 ? ((stats.accepted_offers / stats.total_offers) * 100).toFixed(1) : 0}%
                </span>
              </div>
              <div>
                <span className="text-gray-600">Ablehnungsquote:</span>
                <span className="ml-2 font-medium">
                  {stats.total_offers > 0 ? ((stats.rejected_offers / stats.total_offers) * 100).toFixed(1) : 0}%
                </span>
              </div>
              <div>
                <span className="text-gray-600">Verhandlungsquote:</span>
                <span className="ml-2 font-medium">
                  {stats.total_offers > 0 ? ((stats.countered_offers / stats.total_offers) * 100).toFixed(1) : 0}%
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default StatsPanel

