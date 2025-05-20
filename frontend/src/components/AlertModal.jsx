import React from 'react';
import './AlertModal.css';

export default function AlertModal({ open, onClose, title, message, type = 'info' }) {
  if (!open) return null;
  return (
    <div className="alert-modal-overlay" onClick={onClose}>
      <div className={`alert-modal alert-modal--${type}`} onClick={e => e.stopPropagation()}>
        <button className="alert-modal__close" onClick={onClose}>×</button>
        {title && <h2 className="alert-modal__title">{title}</h2>}
        <p className="alert-modal__message">{message}</p>
      </div>
    </div>
  );
}
