import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ValidationPage from './pages/ValidationPage'
import ReportPage from './pages/ReportPage'
import Header from './components/Header'
import './App.css'

function AppContent() {
  const { token } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      {token && <Header />}
      <Routes>
        <Route path="/login" element={!token ? <LoginPage /> : <Navigate to="/dashboard" />} />
        <Route path="/register" element={!token ? <RegisterPage /> : <Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={token ? <DashboardPage /> : <Navigate to="/login" />} />
        <Route path="/validate" element={token ? <ValidationPage /> : <Navigate to="/login" />} />
        <Route path="/report/:id" element={token ? <ReportPage /> : <Navigate to="/login" />} />
        <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} />} />
      </Routes>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  )
}

export default App
