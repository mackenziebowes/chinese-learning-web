import { useState } from "react";
import { StartCapture } from "../../../wailsjs/go/main/App";

function App() {
  const [status, setStatus] = useState("Idle");

  const handleMicTest = async () => {
    setStatus("Initializing Mic...");
    const result = await StartCapture();
    setStatus(result);
  };

  return (
    <div className="p-8 font-sans">
      <h1 className="text-2xl font-bold mb-4">Mandarin Tone Master</h1>
      <button
        onClick={handleMicTest}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
      >
        Test Native Mic
      </button>
      <p className="mt-4 text-gray-600">Status: {status}</p>
    </div>
  );
}

export default App;
