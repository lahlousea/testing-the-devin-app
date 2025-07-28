import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { ArrowLeft, CheckCircle, Clock, AlertCircle, TrendingUp, Target } from 'lucide-react'

interface ValidationReport {
  id: number
  status: string
  overall_score: number
  recommendations: string
  market_analysis: string
  competition_analysis: string
  risk_assessment: string
  created_at: string
  completed_at: string
  startup: {
    id: number
    name: string
    description: string
    industry: string
    target_market: string
    business_model: string
  }
  hypotheses: Array<{
    id: number
    type: string
    statement: string
    confidence_score: number
    validation_status: string
  }>
}

export default function ReportPage() {
  const { id } = useParams<{ id: string }>()
  const [report, setReport] = useState<ValidationReport | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { token } = useAuth()
  const navigate = useNavigate()

  const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchReport()
    const interval = setInterval(() => {
      if (report?.status === 'processing') {
        fetchReport()
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [id, report?.status])

  const fetchReport = async () => {
    try {
      const response = await fetch(`${API_URL}/api/reports/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setReport(data)
      } else {
        setError('Failed to load report')
      }
    } catch (err) {
      setError('Error loading report')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.7) return 'text-green-600'
    if (score >= 0.5) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 0.7) return 'Strong Validation'
    if (score >= 0.5) return 'Moderate Validation'
    return 'Weak Validation'
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Loading Report...</h2>
          <p className="text-gray-600">Please wait while we fetch your validation report.</p>
        </div>
      </div>
    )
  }

  if (error || !report) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading Report</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Button onClick={() => navigate('/dashboard')}>
            Back to Dashboard
          </Button>
        </div>
      </div>
    )
  }

  if (report.status === 'processing') {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Button
          variant="ghost"
          onClick={() => navigate('/dashboard')}
          className="mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>

        <Card>
          <CardContent className="text-center py-12">
            <Clock className="h-16 w-16 text-blue-500 mx-auto mb-4 animate-spin" />
            <h2 className="text-2xl font-semibold mb-4">Processing Your Validation</h2>
            <p className="text-gray-600 mb-6">
              Our AI is analyzing your startup idea and gathering validation data from multiple sources.
            </p>
            <Progress value={65} className="w-full max-w-md mx-auto" />
            <p className="text-sm text-gray-500 mt-4">
              This usually takes 2-3 minutes. The page will update automatically.
            </p>
          </CardContent>
        </Card>
      </div>
    )
  }

  const recommendations = report.recommendations ? JSON.parse(report.recommendations) : []
  const marketAnalysis = report.market_analysis ? JSON.parse(report.market_analysis) : []

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Button
        variant="ghost"
        onClick={() => navigate('/dashboard')}
        className="mb-6"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Dashboard
      </Button>

      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-3xl font-bold text-gray-900">{report.startup.name}</h1>
          <Badge variant="outline" className="flex items-center space-x-1">
            <CheckCircle className="h-4 w-4 text-green-500" />
            <span>Completed</span>
          </Badge>
        </div>
        <p className="text-gray-600">{report.startup.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Overall Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className={`text-3xl font-bold ${getScoreColor(report.overall_score)}`}>
              {Math.round(report.overall_score * 100)}%
            </div>
            <p className="text-sm text-gray-600 mt-1">
              {getScoreLabel(report.overall_score)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Industry</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold capitalize">
              {report.startup.industry}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Hypotheses</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">
              {report.hypotheses.length}
            </div>
            <p className="text-sm text-gray-600 mt-1">
              Generated for testing
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span>Key Insights</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {marketAnalysis.map((insight: string, index: number) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                  <span className="text-sm">{insight}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5" />
              <span>Recommendations</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {recommendations.map((rec: string, index: number) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0" />
                  <span className="text-sm">{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generated Hypotheses</CardTitle>
          <CardDescription>
            Key assumptions about your startup that need validation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {report.hypotheses.map((hypothesis) => (
              <div key={hypothesis.id} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="secondary" className="capitalize">
                    {hypothesis.type.replace('_', ' ')}
                  </Badge>
                  <span className="text-sm text-gray-500">
                    Confidence: {Math.round(hypothesis.confidence_score * 100)}%
                  </span>
                </div>
                <p className="text-sm">{hypothesis.statement}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
