import React from 'react';
import { Navigate } from 'react-router-dom';
import Cookies from 'js-cookie';

export default function PublicRoute({ children }) {
  const token = Cookies.get('access_token');
  return token ? <Navigate to="/" replace /> : children;
}
