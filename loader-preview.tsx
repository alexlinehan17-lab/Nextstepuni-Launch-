import React from 'react';
import ReactDOM from 'react-dom/client';

import { LoadingSpinner } from './components/LoadingSpinner';
import './index.css';

const root = document.getElementById('root');
if (!root) throw new Error('Loader preview root was not found');

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <LoadingSpinner />
  </React.StrictMode>,
);
