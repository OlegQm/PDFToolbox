// src/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Пример: два файла переводов в src/locales/en.json и src/locales/sk.json
import en from './locales/en.json';
import sk from './locales/sk.json';

i18n
    .use(initReactI18next) // подключаем интеграцию с React
    .init({
        resources: {
            en: { translation: en },
            sk: { translation: sk },
        },
        lng: 'en',            // язык по умолчанию
        fallbackLng: 'en',    // если перевод отсутствует в текущем
        react: { useSuspense: false },
        interpolation: {
            escapeValue: false  // для React не нужно экранирование
        }
    });

export default i18n;
