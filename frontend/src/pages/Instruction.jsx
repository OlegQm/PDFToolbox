import React from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import "./Instruction.css";

export default function InstructionPage() {
    const { t } = useTranslation();
    const navigate = useNavigate();

    const items = [
        { emoji: "🔄", key: "rotate" },
        { emoji: "📑", key: "extractPages" },
        { emoji: "📚", key: "mergePdfs" },
        { emoji: "✂️", key: "splitPdf" },
        { emoji: "🖼️", key: "imagesToPdf" },
        { emoji: "🔢", key: "addPageNumbers" },
        { emoji: "💧", key: "addWatermark" },
        { emoji: "➖", key: "removePages" },
        { emoji: "🌐", key: "urlToPdf" },
        { emoji: "⚙️", key: "compressPdf" },
    ];

    return (
        <div className="instruction-container">
            <button
                type="button"
                className="back-btn"
                onClick={() => navigate("/")}
            >
                ← {t('back')}
            </button>

            <h1>{t("instructions.title")}</h1>
            <ul className="instruction-list">
                {items.map(({ emoji, key }) => (
                    <li className="instruction-item" key={key}>
                        <div className="instruction-emoji">{emoji}</div>
                        <div className="instruction-content">
                            <h2>{t(key)}</h2>
                            <p>{t(`instructions.${key}`)}</p>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}
