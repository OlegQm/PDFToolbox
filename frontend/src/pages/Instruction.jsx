import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Instruction.css';
import globe from "../assets/planet.png";

const BASE_URL = import.meta.env.VITE_API_URL || 'https://node100.webte.fei.stuba.sk/PDFToolbox';

export default function InstructionPage() {
    const { t, i18n } = useTranslation();
    const navigate = useNavigate();
    const token = Cookies.get('access_token');
    const username = Cookies.get('username');
    const isAdmin = username === 'admin';

    const [loadingConvert, setLoadingConvert] = useState(false);
    const [langOpen, setLangOpen] = useState(false);

    useEffect(() => {
        if (!token || !username) {
            const timer = setTimeout(() => {
                if (token) {
                    Cookies.remove("access_token");
                }
                if (username) {
                    Cookies.remove("username");
                }
                navigate("/");
            }, 1000);
            return () => clearTimeout(timer);
        }
    }, [token, username, navigate]);

    if (!token || !username) {
        return (
        <div className="instruction-container">
            <p>{t("loginAction")}</p>
        </div>
        );
    }

    useEffect(() => {
        const checkToken = () => {
            const token = Cookies.get('access_token');
            if (!token) return;
            try {
                const exp = JSON.parse(atob(token.split('.')[1])).exp * 1000;
                if (Date.now() >= exp) {
                    Cookies.remove('access_token');
                    navigate('/login?expired=true');
                }
            } catch {
                Cookies.remove('access_token');
                navigate('/login');
            }
        };
        checkToken();
        const iv = setInterval(checkToken, 5000);
        return () => clearInterval(iv);
    }, [navigate]);

    const handleConvert = async () => {
        setLoadingConvert(true);
        try {
            window.print();
        } catch (err) {
            console.error(err);
            alert(t('errorConvert'));
        } finally {
            setLoadingConvert(false);
        }
    };

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

                <div className="lang-switcher-instruction">
                    <button
                        type="button"
                        className="language-btn"
                        onClick={() => setLangOpen(open => !open)}
                    >
                        <img src={globe} alt="Language" width="24" height="24" className="icon-img"/>
                        {i18n.language.toUpperCase()}
                    </button>

                    {langOpen && (
                        <ul className="lang-menu">
                            <li onClick={() => {
                                i18n.changeLanguage('en');
                                setLangOpen(false);
                            }}>English
                            </li>
                            <li onClick={() => {
                                i18n.changeLanguage('sk');
                                setLangOpen(false);
                            }}>Slovenčina
                            </li>
                        </ul>
                    )}
                </div>


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
                    {services.map(({emoji, key, requiresUpload}) => (
                        <li className="instruction-item" key={key}>
                            <div className="instruction-emoji">{emoji}</div>
                            <div className="instruction-content">
                                <h2>
                                    {t(key)}
                                    {requiresUpload && <span className="badge">{` (${t('requiresUpload')})`}</span>}
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
            </aside>
        </div>
    );
}
