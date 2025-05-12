import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'

import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import App from './App.jsx'
import PrivateRoute from './components/PrivateRoute.jsx'
import PublicRoute from './components/PublicRoute.jsx'

export default function Router() {
  return (
    <Routes>
      <Route
        path="/login"
        element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        }
      />
      <Route path="/register" element={<Register />} />

      <Route
        path="/*"
        element={
          <PrivateRoute>
            <App />
          </PrivateRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
