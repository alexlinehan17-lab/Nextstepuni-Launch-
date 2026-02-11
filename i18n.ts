/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import en from './locales/en.json';
import ga from './locales/ga.json';
import pl from './locales/pl.json';
import fr from './locales/fr.json';
import es from './locales/es.json';
import de from './locales/de.json';
import pt from './locales/pt.json';
import ro from './locales/ro.json';
import uk from './locales/uk.json';
import ar from './locales/ar.json';

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    ga: { translation: ga },
    pl: { translation: pl },
    fr: { translation: fr },
    es: { translation: es },
    de: { translation: de },
    pt: { translation: pt },
    ro: { translation: ro },
    uk: { translation: uk },
    ar: { translation: ar },
  },
  lng: 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
