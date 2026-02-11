import React from "react";
import { createRoot } from "react-dom/client";

import "@/index.css";

import MainApp from "@/App";

const container = document.getElementById("root");

const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <MainApp />
  </React.StrictMode>,
);
