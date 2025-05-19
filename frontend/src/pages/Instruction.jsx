import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Instruction.css';

// Base URL for API (set via Vite):
const BASE_URL = import.meta.env.VITE_API_URL || 'https://node100.webte.fei.stuba.sk/PDFToolbox';

export default function InstructionPage() {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();
    const token = Cookies.get('access_token');
    const username = Cookies.get('username');
    const role = Cookies.get('role');
    const isAdmin = role === 'admin';

    // State for conversion button
    const [loadingConvert, setLoadingConvert] = useState(false);

    // Session check: redirect to login if token missing/expired
    useEffect(() => {
        const checkToken = () => {
            const tk = Cookies.get('access_token');
            if (!tk) {
                return navigate('/login');
            }
            try {
                const exp = JSON.parse(atob(tk.split('.')[1])).exp * 1000;
                if (Date.now() >= exp) {
                    return navigate('/login?expired=true');
                }
            } catch {
                return navigate('/login');
            }
        };
        checkToken();
        const interval = setInterval(checkToken, 5000);
        return () => clearInterval(interval);
    }, [navigate]);

    // If not authenticated, show prompt
    if (!token) {
        return (
            <div className="instruction-container">
                <p>{t('loginAction')}</p>
            </div>
        );
    }

    // Convert current page to PDF
    const handleConvert = async () => {
        setLoadingConvert(true);
        try {
            const form = new FormData();
            form.append('url', window.location.href);

            const res = await fetch(`${BASE_URL}/api/url-to-pdf`, {
                method: 'POST',
                body: form,
                headers: { Authorization: `Bearer ${token}` }
            });

            if (res.status === 403) {
                navigate('/login');
                return;
            }
            if (!res.ok) {
                throw new Error(`Conversion failed: ${res.status}`);
            }

            const blob = await res.blob();
            const downloadUrl = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = 'instructions.pdf';
            a.click();
        } catch (err) {
            console.error(err);
            alert(t('errorConvert'));
        } finally {
            setLoadingConvert(false);
        }
    };

    // Your PDF services and overview items (unchanged)
    const services = [
        { emoji: '🔄', key: 'rotate', requiresUpload: true },
        { emoji: '📑', key: 'extractPages', requiresUpload: true },
        { emoji: '📚', key: 'mergePdfs', requiresUpload: true },
        { emoji: '✂️', key: 'splitPdf', requiresUpload: true },
        { emoji: '🖼️', key: 'imagesToPdf', requiresUpload: false },
        { emoji: '🔢', key: 'addPageNumbers', requiresUpload: true },
        { emoji: '💧', key: 'addWatermark', requiresUpload: true },
        { emoji: '➖', key: 'removePages', requiresUpload: true },
        { emoji: '🌐', key: 'urlToPdf', requiresUpload: false },
        { emoji: '⚙️', key: 'compressPdf', requiresUpload: true }
    ];

    const overviewItems = [
        { key: 'overview.pdfServices' },
        { key: 'overview.history' },
        { key: 'overview.login' },
        { key: 'overview.registration' },
        { key: 'overview.language' }
    ];

    return (
        <div className="instruction-container">
            {/* Navigation Header */}
            <section className="nav-header">
                <button
                    type="button"
                    className="back-btn"
                    onClick={() => navigate(-1)}
                >
                    ← {t('back')}
                </button>

                <select
                    className="language-select"
                    value={i18n.language}
                    onChange={e => i18n.changeLanguage(e.target.value)}
                >
                    <option value="en">English</option>
                    <option value="sk">Slovensky</option>
                </select>

                <button
                    className="convert-btn"
                    onClick={handleConvert}
                    disabled={loadingConvert}
                >
                    {loadingConvert ? t('processing') : t('convertToPdf')}
                </button>
            </section>

            {/* 1. PDF Services */}
            <aside className="section-card">
                <h1>{t('instructions.title')}</h1>
                <ul className="instruction-list">
                    {services.map(({ emoji, key, requiresUpload }) => (
                        <li className="instruction-item" key={key}>
                            <div className="instruction-emoji">{emoji}</div>
                            <div className="instruction-content">
                                <h2>
                                    {t(key)}
                                    {requiresUpload && <span className="badge">{t('requiresUpload')}</span>}
                                </h2>
                                <p>{t(`instructions.${key}`)}</p>
                            </div>
                        </li>
                    ))}
                </ul>
            </aside>

            {/* 2. Overview of Functionality */}
            <aside className="section-card">
                <h1>{t('instructions.overviewTitle')}</h1>
                <ul className="instruction-list">
                    {overviewItems.map(({ key }) => (
                        <li className="instruction-item" key={key}>
                            <div className="instruction-content">
                                <h2>{t(`${key}.title`)}</h2>
                                <p>{t(`${key}.description`)}</p>

                                {/* Steps for login */}
                                {key === 'overview.login' && (
                                    <ol className="auth-steps">
                                        <li>{t('login.step1')}</li>
                                        <li>{t('login.step2')}</li>
                                        <li>{t('login.step3')}</li>
                                        <li>{t('login.step4')}</li>
                                    </ol>
                                )}

                                {/* Steps for registration */}
                                {key === 'overview.registration' && (
                                    <ol className="auth-steps">
                                        <li>{t('registration.step1')}</li>
                                        <li>{t('registration.step2')}</li>
                                        <li>{t('registration.step3')}</li>
                                        <li>{t('registration.step4')}</li>
                                        <li>{t('registration.step5')}</li>
                                    </ol>
                                )}
                            </div>
                        </li>
                    ))}
                </ul>

                {/* 3. History for Admin */}
                {isAdmin && (
                    <section className="admin-history">
                        <h2>{t('history.title')}</h2>
                        <div className="history-buttons">
                            <button>{t('history.clear')}</button>
                            <button>{t('history.downloadCsv')}</button>
                        </div>
                    </section>
                )}
            </aside>
        </div>
    );
}
