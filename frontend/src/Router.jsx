import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import App from './App.jsx';

const LOGIN_PATH    = '/login';
const REGISTER_PATH = '/register';
const APP_PATH      = '/*';

export default function Router() {
  return (
    <Routes>
      {/* <Route path="/" element={<Navigate to={LOGIN_PATH} replace />} /> */}

      <Route path={LOGIN_PATH}    element={<Login />} />
      <Route path={REGISTER_PATH} element={<Register />} />

      <Route path={APP_PATH}      element={<App />} />

      {/* <Route path="*" element={<Navigate to={LOGIN_PATH} replace />} /> */}
    </Routes>
  );
}
