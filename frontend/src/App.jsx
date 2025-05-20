import React, { useState, useRef, useEffect } from "react"; import "./App.css";
import { useTranslation } from "react-i18next";
import catImg from './components/white_cat.png';
import HoverPawButton from "./components/HoverPawButton";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import "./App.css";
import AlertModal from "./components/AlertModal";
import clockGif from "./assets/clock.png";
import infoGif from "./assets/info.png";
import globe from "./assets/planet.png";
import refresh from "./assets/refresh_token.png"


const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const canWorkWithoutMainFile = ["/images-to-pdf", "/url-to-pdf", "/merge-pdfs"]

function getTokenExpiration(token) {
  try {
    if (!token || token === "undefined" || token.split(".").length !== 3) return null;
    const payload = token.split(".")[1];
    const decoded = atob(payload);
    const parsed = JSON.parse(decoded);
    return parsed.exp * 1000;
  } catch (err) {
    console.error("Token decode error:", err);
    return null;
  }
}


export default function App() {
  const dropInputRef = useRef(null);
  const navigate = useNavigate();
  const username = Cookies.get("username");
  const { t, i18n } = useTranslation();
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const mergeInputRef = useRef(null);
  const imagesInputRef = useRef(null);

  const [pageUrl, setPageUrl] = useState("");
  const [file, setFile] = useState(null);

  const [mergeFiles, setMergeFiles] = useState([]);
  const [imageFiles, setImageFiles] = useState([]);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedTool, setSelectedTool] = useState(null);
  const [rotations, setRotations] = useState([{ page: 1, degrees: 90 }]);
  const [pages, setPages] = useState("1");
  const [splitAt, setSplitAt] = useState(1);
  const [watermark, setWatermark] = useState({
    text: "",
    font_name: "Helvetica",
    bold: false,
    italic: false,
    font_size: 24,
    color: "#000000",
    alpha: 0.5,
    position: "center",
    offset_x: 0,
    offset_y: 0,
    angle: 0,
  });
  const emojiMap = {
    "Rotate": "🔄",
    "Extract Pages": "📑",
    "Merge PDFs": "📚",
    "Split PDF": "✂️",
    "Images to PDF": "🖼️",
    "Page Numbers": "🔢",
    "Watermark": "💧",
    "Remove Pages": "➖",
    "URL to PDF": "🌐",
    "Compress": "⚙️",
  };

  const tools = [
    { label: "Rotate", path: "/rotate-pdf", needsConfig: true, i18nKey: "rotate" },
    { label: "Extract Pages", path: "/extract-pages", needsConfig: true, i18nKey: "extractPages" },
    { label: "Merge PDFs", path: "/merge-pdfs", needsConfig: true, i18nKey: "mergePdfs" },
    { label: "Split PDF", path: "/split-pdf", needsConfig: true, i18nKey: "splitPdf" },
    { label: "Images to PDF", path: "/images-to-pdf", needsConfig: true, i18nKey: "imagesToPdf" },
    { label: "Page Numbers", path: "/add-page-numbers", needsConfig: true, i18nKey: "addPageNumbers" },
    { label: "Watermark", path: "/add-watermark", needsConfig: true, i18nKey: "addWatermark" },
    { label: "Remove Pages", path: "/remove-pages", needsConfig: true, i18nKey: "removePages" },
    { label: "URL to PDF", path: "/url-to-pdf", needsConfig: true, i18nKey: "urlToPdf" },
    { label: "Compress", path: "/compress-pdf", needsConfig: true, i18nKey: "compressPdf" },
  ];
  const [modal, setModal] = useState({ open: false, title: "", message: "", type: "info" });

  async function callApi(path, file, extraBody = {}) {
    const form = new FormData();
    if (file) {
      form.append("file", file, file.name);
    }
    if (extraBody.files && Array.isArray(extraBody.files)) {
      extraBody.files.forEach(f => form.append("files", f, f.name));
      delete extraBody.files;
    }
    Object.entries(extraBody).forEach(([k, v]) => {
      form.append(k, typeof v === "string" ? v : JSON.stringify(v));
    });

    const token = Cookies.get("access_token");
    if (!token) {
      setTimeout(() => {
        Cookies.remove("access_token");
        navigate("/login");
      }, 1000);
      throw new Error("You must LOG IN before using services!");
    }

    const res = await fetch(`${BASE_URL}/api${path}`, {
      method: "POST",
      body: form,
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (res.status === 401) {
      Cookies.remove("access_token");
      throw new Error("Your session has expired. Please log in again.");
    }

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `Error ${res.status}`);
    }

    return res.blob();
  }

  function isPdfFile(file) {
    return file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
  }

  const handleFile = (e) => {
    const f = e.target.files[0];
    if (f) {
      if (!isPdfFile(f)) {
        setError("Only PDF files are allowed.");
        setFile(null);
        setDownloadUrl("");
        return;
      }
      setFile(f);
      setError("");
      setDownloadUrl("");
    }
  };

  const handleMergeFiles = (e) => {
    const arr = Array.from(e.target.files);
    const notPdf = arr.find(f => !isPdfFile(f));
    if (notPdf) {
      setError(`File ${notPdf.name} is not a PDF.`);
      return;
    }
    setMergeFiles(arr);
    setError("");
    setDownloadUrl("");
  };

  const handleImageFiles = (e) => { setImageFiles(Array.from(e.target.files)); setError(""); setDownloadUrl(""); };

  const openTool = tool => {
    const noFileNeeded = canWorkWithoutMainFile.includes(tool.path);
    if (!noFileNeeded && !file) {
      setError("Please select a PDF file first.");
      return;
    }
    setError("");
    setSelectedTool(tool);
  };

  const runTool = async (tool, body) => {
    if (tool.path === "/merge-pdfs" && mergeFiles.length < 2) {
      setError("Select at least two PDFs to merge.");
      return;
    }
    if (tool.path === "/split-pdf" && splitAt < 1) {
      setError("Split position must be >= 1.");
      return;
    }
    if (tool.path === "/images-to-pdf" && imageFiles.length === 0) {
      setError("Select at least one image.");
      return;
    }

    const needsMainPdf = !canWorkWithoutMainFile.includes(tool.path);
    if (tool.needsConfig && needsMainPdf && !file) {
      setError("Please select a PDF first.");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const primary = tool.path === "/merge-pdfs"
        ? mergeFiles[0]
        : tool.path === "/images-to-pdf"
          ? imageFiles[0]
          : file;

      const blob = await callApi(tool.path, primary, body);
      setDownloadUrl(URL.createObjectURL(blob));
      setSelectedTool(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const addRotation = () => setRotations(rs => [...rs, { page: rs.length + 1, degrees: 90 }]);
  const updateRotation = (i, f, v) => setRotations(rs => rs.map((r, idx) => idx === i ? { ...r, [f]: v } : r));
  const removeRotation = (i) => setRotations(rs => rs.filter((_, idx) => idx !== i));

  const actionLabels = {
    "/rotate-pdf": "applyRotate",
    "/extract-pages": "extract",
    "/merge-pdfs": "merge",
    "/split-pdf": "split",
    "/images-to-pdf": "convertImages",
    "/add-page-numbers": "addNumbers",
    "/add-watermark": "watermark",
    "/remove-pages": "remove",
    "/url-to-pdf": "convertUrl",
    "/compress-pdf": "compress"
  };
  const containerRef = useRef(null);
  const pupilRef = useRef(null);
  const regenerateToken = async () => {
    const currentToken = Cookies.get("access_token");
    if (!currentToken || currentToken === "undefined") {
      setModal(
        {
          open: true, title: t('authorizationError'),
          message: t('authorizationErrorMessage'),
          type: "error"
        }
      );
      navigate("/login");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/api/authorization/regenerate-token`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${currentToken}`,
        },
      });

      if (response.status === 401) {
        Cookies.remove("access_token");
        setModal(
          {
            open: true,
            title: t('sessionExpired'),
            message: t('sessionExpiredMessage'),
            type: "warning"
          }
        );
        navigate("/login");
        return;
      }

      const data = await response.json();
      console.log("Response from the server:", data);

      const newToken = data.access_token;

      if (!newToken || newToken === "undefined") {
        setModal(
          {
            open: true,
            title: t('responseError'),
            message: t('responseErrorMessage'),
            type: "warning"
          }
        );
        return;
      }

      Cookies.set("access_token", newToken);
      setModal(
        {
          open: true,
          title: t('tokenUpdated'),
          message: t('tokenUpdatedMessage'),
          type: "success"
        }
      );
    } catch (error) {
      setModal(
        {
          open: true,
          title: t('updateError'),
          message: t('updateErrorMessage'),
          type: "warning"
        }
      );
      console.error(error);
    }
  };

  useEffect(() => {
    const onMouseMove = (e) => {
      const rect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const minX = 85,
        maxX = 100,
        minY = 40,
        maxY = 55;
      const px = Math.min(Math.max(x, minX), maxX);
      const py = Math.min(Math.max(y, minY), maxY);
      pupilRef.current.style.left = px + "px";
      pupilRef.current.style.top = py + "px";
    };

    window.addEventListener("mousemove", onMouseMove);
    return () => window.removeEventListener("mousemove", onMouseMove);
  }, []);


  useEffect(() => {
    if (error === "Your session has expired. Please log in again.") {
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    }
  }, [error]);


  useEffect(() => {
    const checkToken = () => {
      const token = Cookies.get("access_token");
      if (!token) return;

      const exp = getTokenExpiration(token);
      if (!exp) return;

      const now = Date.now();
      if (now >= exp) {
        Cookies.remove("access_token");
        navigate("/login?expired=true");
      }
    };

    const interval = setInterval(checkToken, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    ['access_token', 'username'].forEach(k => Cookies.remove(k));
    navigate("/login");
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>📁 {t('instruments')}</h1>

        <div className="header-actions">
          {/* History */}
          {username === 'admin' && (
              <button
                  type="button"
                  className="icon-btn history-btn"
                  onClick={() => navigate("/history")}
              >
                <img src={clockGif} alt={t('history')} width="24" height="24"/>
                <span>{t('history')}</span>
              </button>
          )}

          {/* Language */}
          <div className="lang-switcher">
            <button
                type="button"
                className="icon-btn language-btn"
                onClick={() => setLangMenuOpen(open => !open)}
            >
              <img src={globe} alt="Language" width="24" height="24" className="icon-img"/>
              <span>{i18n.language === 'en' ? t('language') : t('language')}</span>
            </button>

            {langMenuOpen && (
                <ul className="lang-menu">
                  <li onClick={() => {
                    i18n.changeLanguage('en');
                    setLangMenuOpen(false);
                  }}>
                    English
                  </li>
                  <li onClick={() => {
                    i18n.changeLanguage('sk');
                    setLangMenuOpen(false);
                  }}>
                    Slovenčina
                  </li>
                </ul>
            )}
          </div>
          <button
              type="button"
              className="icon-btn"
              onClick={regenerateToken}
          >
            <img src={refresh} alt={t('updateToken')} width="24" height="24"/>
            <span>{t('updateToken')}</span>
          </button>

          <button
              type="button"
              className="icon-btn instruction-btn"
              onClick={() => navigate("/instruction")}
          >
            <img src={infoGif} alt={t('instruction')} width="24" height="24"/>
            <span>{t('instruction')}</span>
          </button>
        </div>

        <button onClick={handleLogout} className="logout-btn">
          {t('logout')}
        </button>

        {downloadUrl && (
          <div className="modal" onClick={() => setDownloadUrl("")}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <button
                type="button"
                className="modal-close"
                onClick={() => setDownloadUrl("")}
              >
                ×
              </button>

              <a href={downloadUrl} download className="download-btn">
                Download result
              </a>
            </div>
          </div>
        )}

      </header>

      <div className="main-area">
        <div className="dropzone-wrapper">
          <div className="cat-wrapper">
            <div className="cat-container" ref={containerRef}>
              <img src={catImg} className="cat" alt="cat" />
              <div className="pupil" ref={pupilRef} />
            </div>
          </div>
          <div className={`dropzone ${error ? "drop-error-active" : ""}`}>

            <div className="drop-icon">📄</div>

            {file ? (
              <div className="file-btns" onClick={e => e.stopPropagation()}>
                <span className="drop-text">{file.name}</span>
                <button
                  type="button"
                  className="clear-btn"
                  onClick={e => {
                    e.stopPropagation();
                    setFile(null);
                    setDownloadUrl("");
                    setError("");
                  }}
                >
                  ×
                </button>
              </div>
            ) : (
              <div className="drop-text">{t('dragDrop')}</div>
            )}

            <button
              type="button"
              className="primary-btn"
              onClick={e => {
                e.stopPropagation();
                dropInputRef.current.click();

              }}
            >
              {t('chooseFile')}
            </button>
            <input
              ref={dropInputRef}
              type="file"
              accept="application/pdf"
              className="hidden-input"
              onChange={handleFile}
            />
            {error && <div className="drop-error">{t(error)}</div>}
          </div>

        </div>
        <div className="tools-grid">
          {tools.map(tool => {
            const noFileNeeded = canWorkWithoutMainFile.includes(tool.path);
            const needsFile = !noFileNeeded;

            const disabled =
              loading ||
              (needsFile && !file) ||
              (noFileNeeded && !!file);

            return (
              <HoverPawButton
                key={tool.path}
                className="tool-btn"
                onClick={() => openTool(tool)}
                disabled={disabled}
              >
                <span className="tool-sticker">{emojiMap[tool.label]}</span>
                <span className="tool-label">{t(tool.i18nKey)}</span>
              </HoverPawButton>
            );
          })}
        </div>

      </div>

      {selectedTool && (
        <aside className="sidebar">
          <div className="sidebar-header">
            <h2>{t(`actionLabels.${actionLabels[selectedTool.path]}`)}</h2>
            <button className="sidebar-close" onClick={() => setSelectedTool(null)}>×</button>
          </div>

          {/* Rotate PDF */}
          {selectedTool.path === "/rotate-pdf" && (
            <div className="settings-panel">
              <div className="rotations-list">
                {rotations.map((r, i) => (
                  <div key={i} className="rotation-item">
                    <div className="field-group"><label>{t('page')}</label><input type="number" min="1"
                      value={r.page}
                      onChange={e => updateRotation(i, "page", +e.target.value)} />
                    </div>
                    <div className="field-group">
                      <label>{t('rotateDegrees')}</label>
                      <input type="number" step="90"
                        value={r.degrees}
                        onChange={e => updateRotation(i, "degrees", +e.target.value)} />
                    </div>
                    <button
                      type="button"
                      className="remove-rot"
                      onClick={() => removeRotation(i)}
                      aria-label={t('removeRotation')}
                      title={t('removeRotation')}
                    >
                      ×
                    </button>
                  </div>
                ))}
                <button className="add-rot" onClick={addRotation}>{t('addRotation')}</button>
              </div>
            </div>
          )}

          {/* Extract PDFs */}
          {selectedTool.path === "/extract-pages" && (
            <div className="settings-panel">
              <div className="extract-list">
                <label>{t('pagesExample')}</label>
                <input type="text" value={pages} onChange={e => setPages(e.target.value)}
                  placeholder={t('placeholder_pages')} />
              </div>
            </div>
          )}

          {/* Merge PDFs */}
          {selectedTool.path === "/merge-pdfs" && (
            <div className="settings-panel">
              <div className="merge-list">
                <label>{t('selectPdfs')}</label>

                <button
                  type="button"
                  className="primary-btn"
                  onClick={() => mergeInputRef.current.click()}
                >
                  {t('chooseFiles')}
                </button>

                <input
                  ref={mergeInputRef}
                  type="file"
                  accept="application/pdf"
                  multiple
                  onChange={handleMergeFiles}
                  className="hidden-input"
                />

                {mergeFiles.length > 0 ? (
                  <div className="file-btns" onClick={e => e.stopPropagation()}>
                    <span className="drop-text">
                      {mergeFiles.map(f => f.name).join(', ')}
                    </span>
                    <button
                      type="button"
                      className="clear-btn"
                      onClick={e => {
                        e.stopPropagation();
                        setMergeFiles([]);
                        setError("");
                      }}
                    >
                      ×
                    </button>
                  </div>
                ) : (
                  <span>{t('fileNotSelected')}</span>
                )}
              </div>
            </div>
          )}


          {/* Splid PDF */}
          {selectedTool.path === "/split-pdf" && (
            <div className="settings-panel">
              <div className="split-list">
                <label>{t('splitAtPage')}</label>
                <input
                  type="number"
                  min="1"
                  value={splitAt}
                  onChange={e => setSplitAt(+e.target.value)}
                />
              </div>
            </div>
          )}

          {/* Images to PDF */}
          {selectedTool.path === "/images-to-pdf" && (
            <div className="settings-panel">
              <div className="images-list">
                <label>{t('selectImages')}</label>

                <button
                  type="button"
                  className="primary-btn"
                  onClick={() => imagesInputRef.current.click()}
                >
                  {t('chooseFiles')}
                </button>

                <input
                  ref={imagesInputRef}
                  type="file"
                  accept="image/*"
                  multiple
                  onChange={handleImageFiles}
                  className="hidden-input"
                />

                {imageFiles.length > 0 ? (
                  <div className="file-btns" onClick={e => e.stopPropagation()}>
                    <span className="drop-text">
                      {imageFiles.map(f => f.name).join(', ')}
                    </span>
                    <button
                      type="button"
                      className="clear-btn"
                      onClick={e => {
                        e.stopPropagation();
                        setImageFiles([]);
                        setError("");
                      }}
                    >
                      ×
                    </button>
                  </div>
                ) : (
                  <span>{t('fileNotSelected')}</span>
                )}
              </div>
            </div>
          )}

          {/* Add page numbers */}
          {selectedTool.path === "/add-page-numbers" && (
            <div className="settings-panel">
              <div className="generic-list">
                <p>{t('noSettings')}</p>
              </div>
            </div>
          )}

          {/* Watermark */}
          {selectedTool.path === "/add-watermark" && (
            <div className="settings-panel">
              <div className="watermark-list">
                {Object.entries(watermark).map(([key, val]) => (
                  <div key={key} className="field-group">
                    <label>{t(`watermark.${key}`)}</label>
                    {typeof val === "boolean" ? (
                      <input
                        type="checkbox"
                        checked={val}
                        onChange={e =>
                          setWatermark(wm => ({ ...wm, [key]: e.target.checked }))
                        }
                      />
                    ) : (
                      <input
                        type={typeof val === "number" ? "number" : "text"}
                        value={val}
                        onChange={e => {
                          const v = e.target.value;
                          setWatermark(wm => ({
                            ...wm,
                            [key]:
                              typeof watermark[key] === "number" ? +v : v
                          }));
                        }}
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Remove Pages */}
          {selectedTool.path === "/remove-pages" && (
            <div className="settings-panel">
              <div className="extract-list">
                <label>{t('pagesToRemove')}</label>
                <input
                  type="text"
                  value={pages}
                  onChange={e => setPages(e.target.value)}
                  placeholder={t('placeholder_pagesRemove')}
                />
              </div>
            </div>
          )}

          {/* URL to PDF */}
          {selectedTool.path === "/url-to-pdf" && (
            <div className="settings-panel">
              <div className="extract-list">
                <label>{t('pageUrl')}</label>
                <input
                  type="text"
                  value={pageUrl}
                  onChange={e => setPageUrl(e.target.value)}
                  placeholder={t('placeholder_url')}
                />
              </div>
            </div>
          )}

          {selectedTool.path === "/compress-pdf" && (
            <div className="settings-panel">
              <div className="generic-list">
                <p>{t('noSettings')}</p>
              </div>
            </div>
          )}
          <button className="submit-rot"
            onClick={() => {
              let body = {};
              if (selectedTool.path === "/url-to-pdf" && !pageUrl.trim()) {
                setError("Please enter a valid URL.");
                return;
              }
              if (selectedTool.path === "/rotate-pdf" && rotations.length === 0) {
                setError("Please specify at least one rotation.");
                return;
              }
              if (selectedTool.path === "/extract-pages" && !pages.trim()) {
                setError("Please specify pages to extract (e.g. 1,3,5).");
                return;
              }
              if (selectedTool.path === "/remove-pages" && !pages.trim()) {
                setError("Please specify pages to remove (e.g. 2,4,5).");
                return;
              }
              if (selectedTool.path === "/add-watermark" && !watermark.text.trim()) {
                setError("Please enter watermark text.");
                return;
              }
              switch (selectedTool.path) {
                case "/rotate-pdf":
                  body = { rotations };
                  break;
                case "/extract-pages":
                  body = { pages: pages.split(",").map(s => +s.trim()).filter(n => !isNaN(n)) };
                  break;
                case "/merge-pdfs":
                  body = { files: mergeFiles };
                  break;
                case "/split-pdf":
                  body = { split_at: splitAt };
                  break;
                case "/images-to-pdf":
                  body = { files: imageFiles };
                  break;
                case "/add-page-numbers":
                  body = {};
                  break;
                case "/add-watermark":
                  body = { ...watermark };
                  break;
                case "/remove-pages":
                  body = { pages: pages.split(",").map(s => +s.trim()).filter(n => !isNaN(n)) };
                  break;
                case "/url-to-pdf":
                  body = { url: pageUrl };
                  break;
                case "/compress-pdf":
                  body = {};
                  break;
                default:
                  body = {};
              }
              runTool(selectedTool, body);
            }}
            disabled={
              loading ||
              (selectedTool.path === "/rotate-pdf" && rotations.length === 0) ||
              (selectedTool.path === "/extract-pages" && !pages.trim()) ||
              (selectedTool.path === "/remove-pages" && !pages.trim()) ||
              (selectedTool.path === "/url-to-pdf" && !pageUrl.trim()) ||
              (selectedTool.path === "/add-watermark" && !watermark.text.trim())
            }
          >
            {loading
              ? t('processing')
              : t(`actionLabels.${actionLabels[selectedTool.path]}`)}
          </button>
        </aside>
      )}
      <AlertModal
        open={modal.open}
        onClose={() => setModal({ ...modal, open: false })}
        title={modal.title}
        message={modal.message}
        type={modal.type}
     />
    </div>
  );
}
