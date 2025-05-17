import React, { useState, useEffect, useRef, useLayoutEffect } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import bg from "../assets/font.png";
import emptyImg from '../assets/no_record.png';
import './history.css';

import { useTranslation } from 'react-i18next';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_MAX_LIMIT = 200;
const CSV_MAX_LIMIT = 1000;

export default function HistoryPage() {
    const [logs, setLogs] = useState([]);
    const [total, setTotal] = useState(0);
    const [skip, setSkip] = useState(0);
    const [limit, setLimit] = useState(10);
    const [allMode, setAllMode] = useState(false);
    const [error, setError] = useState('');

    const navigate = useNavigate();
    const tableRef = useRef(null);
    const prevBtnRef = useRef(null);
    const [pageWindowSize, setPageWindowSize] = useState(1);

    const [infoMessage, setInfoMessage] = useState('');
    const [showConfirm, setShowConfirm] = useState(false);

    const [reloadKey, setReloadKey] = useState(0);

    useEffect(() => {
        if (!infoMessage) return;
        const t = setTimeout(() => setInfoMessage(''), 3000);
        return () => clearTimeout(t);
    }, [infoMessage]);

    const { t } = useTranslation();

    useEffect(() => {
        Object.assign(document.body.style, {
            backgroundImage: `url(${bg})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            backgroundAttachment: 'fixed',
            margin: '0',
        });
        return () => {
            Object.assign(document.body.style, {
                backgroundImage: '',
                backgroundSize: '',
                backgroundPosition: '',
                backgroundRepeat: '',
                backgroundAttachment: '',
                margin: '',
            });
        };
    }, []);


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

    useEffect(() => {
        const fetchAll = async () => {
            setError('');
            const token = Cookies.get('access_token');
            if (!token) {
                setError('Token missing — please log in again.');
                return;
            }

            try {
                const chunkSize = allMode ? API_MAX_LIMIT : limit;
                const serverSkip = allMode ? 0 : skip;
                const qs1 = new URLSearchParams({
                    skip: serverSkip.toString(),
                    limit: chunkSize.toString()
                });
                const r1 = await fetch(
                    `${BASE_URL}api/database/get-history-logs?${qs1}`,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                if (r1.status === 401) throw new Error('Your session has expired. Please log in again.');
                if (!r1.ok) throw new Error(`Error ${r1.status}: ${await r1.text()}`);

                const { total: tot, logs: firstLogs } = await r1.json();
                setTotal(tot);

                let allLogs = firstLogs;
                if (allMode && tot > chunkSize) {
                    const offsets = [];
                    for (let s = chunkSize; s < tot; s += chunkSize) offsets.push(s);
                    const rest = await Promise.all(
                        offsets.map(s => {
                            const qs = new URLSearchParams({ skip: s.toString(), limit: chunkSize.toString() });
                            return fetch(`${BASE_URL}api/database/get-history-logs?${qs}`, {
                                headers: { Authorization: `Bearer ${token}` }
                            })
                                .then(r => { if (!r.ok) throw new Error(`Error ${r.status}`); return r.json(); })
                                .then(b => b.logs);
                        })
                    );
                    allLogs = firstLogs.concat(...rest);
                }

                setLogs(allLogs);


            } catch (err) {
                setError(err.message);
            }
        };

        fetchAll();
    }, [skip, limit, allMode, navigate, reloadKey]);


    useLayoutEffect(() => {
        function calcWindow() {
            if (!tableRef.current || !prevBtnRef.current) return;
            const tableW = tableRef.current.clientWidth;
            const btnW = prevBtnRef.current.clientWidth;
            const gap = 8;
            const cnt = Math.floor(tableW / (btnW + gap));
            setPageWindowSize(Math.max(1, cnt));
        }
        calcWindow();
        window.addEventListener('resize', calcWindow);
        return () => window.removeEventListener('resize', calcWindow);
    }, []);

    const chunkSize = allMode ? API_MAX_LIMIT : limit;
    const totalPages = allMode
        ? Math.ceil(total / chunkSize)
        : Math.ceil(total / limit);
    const currentPage = allMode
        ? Math.floor(skip / chunkSize) + 1
        : Math.floor(skip / limit) + 1;

    const winSize = pageWindowSize;
    const winStart = Math.floor((currentPage - 1) / winSize) * winSize + 1;
    const winEnd = Math.min(winStart + winSize - 1, totalPages);

    const goPrev = () => setSkip(s => Math.max(0, s - chunkSize));
    const goNext = () => setSkip(s => Math.min(s + chunkSize, (totalPages - 1) * chunkSize));

    const onLimitChange = e => {
        const v = Number(e.target.value);
        if (v === -1) {
            setAllMode(true);
            setSkip(0);
        } else {
            setAllMode(false);
            setSkip(0);
            setLimit(v);
        }
    };

    const formatTS = iso => {
        const d = new Date(iso);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ` +
            `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}:${String(d.getSeconds()).padStart(2, '0')}`;
    };

    const handleDownload = async () => {
        setInfoMessage('historyPage.Downloadingthispage');
        const token = Cookies.get('access_token');
        if (!token) {
            setInfoMessage('Token missing — please log in again.');
            return;
        }
        try {
            const csvParts = [];
            if (allMode) {
                for (let offset = 0; offset < total; offset += CSV_MAX_LIMIT) {
                    const chunk = Math.min(CSV_MAX_LIMIT, total - offset);
                    const qs = new URLSearchParams({ skip: offset, limit: chunk });
                    const resp = await fetch(`${BASE_URL}api/database/history-export-to-csv?${qs}`, {
                        headers: { Authorization: `Bearer ${token}` },
                    });
                    if (!resp.ok) throw new Error(`Error ${resp.status} during CSV export`);
                    const text = await resp.text();
                    if (offset === 0) csvParts.push(text);
                    else {
                        const [, ...lines] = text.split('\n');
                        csvParts.push(lines.join('\n'));
                    }
                }
            } else {
                const qs = new URLSearchParams({ skip, limit });
                const resp = await fetch(`${BASE_URL}api/database/history-export-to-csv?${qs}`, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                if (!resp.ok) throw new Error(`Error ${resp.status} during CSV export`);
                csvParts.push(await resp.text());
            }
            const blob = new Blob([csvParts.join('\n')], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `history_${Date.now()}.csv`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        } catch (err) {
            setInfoMessage(err.message);
        }
    };

    const handleClearClick = () => setShowConfirm(true);
    const confirmClearYes = async () => {
        setShowConfirm(false);
        setInfoMessage('Clearing all history...');
        const token = Cookies.get('access_token');
        if (!token) { setInfoMessage('Token missing — please log in again.'); return; }
        try {
            const resp = await fetch(`${BASE_URL}api/database/clear-history`, {
                method: 'DELETE',
                headers: { Authorization: `Bearer ${token}` },
            });
            if (!resp.ok) throw new Error(`Error ${resp.status} clearing history`);
            setLogs([]);
            setTotal(0);
            setInfoMessage('historyPage.Allhistorycleared.');
            setTimeout(() => {
                setAllMode(false);
                setLimit(10);
                setSkip(0);
                setReloadKey(key => key + 1);
            }, 3000);

        }


        catch (err) {
            setInfoMessage(err.message);
        }
    };
    const confirmClearNo = () => {
        setShowConfirm(false);
        setInfoMessage('historyPage.Clearcancelled');
    };


    return (
        <div className="history-container">

            {error && <div className="error">⚠ {error}</div>}
            <div className="history-table-wrapper">
                <div className="btn-tabs">
                    <button className="icon-btn history-btn" title="History">
                        <span className="btn-text"> {t('historyPage.History')}</span>
                    </button>

                    <button type="button" className="icon-btn clear-btn" title="Clear history" onClick={handleClearClick}>
                        ✖ <span className="btn-text">{t('historyPage.ClearHistory')}</span>
                    </button>
                    <button type="button" className="icon-btn download-btn" title="Download CSV" onClick={handleDownload}>
                        ⬇ <span className="btn-text">{t('historyPage.DownloadCSV')}</span>
                    </button>
                </div>


                <table ref={tableRef} className="history-table">
                    <thead>
                        <tr className="table-title-row">
                            <th colSpan={5}>
                                <div className="header-row">
                                    <div className="header-left">
                                        <span className="table-title">{t('historyPage.logHistory')}</span>
                                        <div className="total-count">
                                            {t('historyPage.totalRecords', { count: total })}
                                        </div>
                                    </div>
                                    <div className="header-right">
                                        {showConfirm ? (
                                            <span className="confirm-span">
                                                {t('historyPage.confirmClear')}&nbsp;
                                                <button onClick={confirmClearYes}>{t('historyPage.Yes')}</button>
                                                <button onClick={confirmClearNo}>{t('historyPage.No')}</button>
                                            </span>
                                        ) : infoMessage ? (
                                            <span className="info-span">{t(infoMessage)}</span>
                                        ) : null}


                                        <span className="table-show"> {t('historyPage.show')}: <select value={allMode ? -1 : limit}
                                            onChange={onLimitChange}>
                                            <option value={10}>10</option>
                                            <option value={20}>20</option>
                                            <option value={50}>50</option>
                                            <option value={-1}>All</option>
                                        </select>
                                        </span>

                                    </div>
                                </div>
                            </th>
                        </tr>

                        <tr>
                            <th>{t('historyPage.User')}</th>
                            <th>{t('historyPage.Action')}</th>
                            <th>{t('historyPage.City')}</th>
                            <th>{t('historyPage.Country')}</th>
                            <th>{t('historyPage.Date')}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs.length > 0 ? (
                            logs.map((log, i) => (
                                <tr key={i}>
                                    <td>{log.username}</td>
                                    <td>{log.action}</td>
                                    <td>{log.city}</td>
                                    <td>{log.country}</td>
                                    <td>{formatTS(log.timestamp)}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan={5} className="no-records">
                                    {t('historyPage.noRecords')}
                                    <br />
                                    <img
                                        src={emptyImg}
                                        alt="No records"
                                        style={{
                                            width: '80px',
                                            height: 'auto',
                                            marginTop: '0.5rem'
                                        }}
                                    />
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {!allMode && (
                <div className="paging">
                    <button ref={prevBtnRef} onClick={goPrev} disabled={skip === 0}>
                        &lt; {t('historyPage.Prev')}
                    </button>
                    {Array.from({ length: winEnd - winStart + 1 }, (_, idx) => {
                        const p = winStart + idx;
                        return (
                            <button
                                key={p}
                                onClick={() => setSkip((p - 1) * chunkSize)}
                                disabled={currentPage === p}
                            >
                                {p}
                            </button>
                        );
                    })}
                    <button onClick={goNext} disabled={skip + chunkSize >= total}>
                        {t('historyPage.Next')}&gt;
                    </button>
                </div>
            )}
        </div>
    );
}
