import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import App from './App.jsx'; // Ваш старый интерфейс–Dashboard

export default function Router() {
    return (
        <Routes>
            {/* По корню сразу на логин */}
            <Route path="/" element={<Navigate to="/login" replace />} />

            {/* Страницы логина/регистрации */}
            <Route path="/login"   element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Ваш Dashboard без проверок */}
            <Route path="/app/*" element={<App />} />

            {/* Всё, что не вхoдит — обратно на логин */}
            <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
    );
}
