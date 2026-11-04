import React from "react";
import { createRoot } from "react-dom/client";
import CertlePage from "./components/certle/CertlePage";
import "./index.css";
import "./components/landing/landing.css";
import "./components/certle/certle.css";
const root = document.getElementById("root");
if (root) createRoot(root).render(<CertlePage />);
