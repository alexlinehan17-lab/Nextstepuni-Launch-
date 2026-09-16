import React from 'react';
import { createRoot } from 'react-dom/client';
import SignInDirections from './components/sign-in-directions/SignInDirections';
import './components/sign-in-directions/sign-in-directions.css';

// Local design review only. This document is not a production build entry.
const root = document.getElementById('root');
if (root) createRoot(root).render(<SignInDirections />);
