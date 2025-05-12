import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { HashRouter as RouterProvider } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import Router from './Router.jsx';

const basename = import.meta.env.BASE_URL

createRoot(document.getElementById('root')).render(
    <RouterProvider basename={basename}>
        <Router />
    </RouterProvider>
);
