import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "@/index.css";

import App from "@/routes";
import Flashcard from "@/routes/flashcard";

const container = document.getElementById("root");

const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/flashcard" element={<Flashcard />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
