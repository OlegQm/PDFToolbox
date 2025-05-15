import './i18n';
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter } from 'react-router-dom';
import Router from './Router.jsx';

const basename = import.meta.env.BASE_URL

createRoot(document.getElementById('root')).render(
    <BrowserRouter basename={basename}>
        <Router />
    </BrowserRouter>
);
