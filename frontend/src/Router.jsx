// src/Router.jsx
import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'

import Login         from './pages/Login.jsx'
import Register      from './pages/Register.jsx'
import App           from './App.jsx'
import PrivateRoute  from './components/PrivateRoute.jsx'

export default function Router() {
  return (
    <Routes>
      {/* Открытые маршруты */}
      <Route path="/login"    element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Защищённый корень */}
      <Route
        path="/"
        element={
          <PrivateRoute>
            <App />
          </PrivateRoute>
        }
      />

      {/* Все остальные маршруты тоже ведут в App */}
      <Route
        path="/*"
        element={
          <PrivateRoute>
            <App />
          </PrivateRoute>
        }
      />

      {/* Любой неизвестный путь – перенаправляем на защищённый корень */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
