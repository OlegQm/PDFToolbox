// src/App.jsx
import React, { useState } from "react";
import "./App.css"; // Tailwind imported here

const BASE_URL = import.meta.env.VITE_BASE_URL || "http://localhost:8000";

async function callApi(path, options = {}) {
  const response = await fetch(`${BASE_URL}/api${path}`, options);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }
  return response;
}

async function rotatePdf(file, rotations) {
  const formData = new FormData();
  formData.append("file", file, file.name);
  formData.append("rotations", JSON.stringify(rotations));
  const res = await callApi("/rotate-pdf", { method: "POST", body: formData });
  const raw = await res.blob();
  return new Blob([raw], { type: "application/pdf" });
}

export default function App() {
  const [file, setFile] = useState(null);
  const [rotations, setRotations] = useState([{ page: 1, degrees: 90 }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleFileChange = e => {
    setFile(e.target.files[0]);
    setDownloadUrl("");
    setError("");
  };

  const handleRotationChange = (i, field, val) => {
    setRotations(rs =>
      rs.map((r, idx) => (idx === i ? { ...r, [field]: val } : r))
    );
  };

  const addRotation = () =>
    setRotations(rs => [...rs, { page: rs.length + 1, degrees: 90 }]);

  const removeRotation = i =>
    setRotations(rs => rs.filter((_, idx) => idx !== i));

  const handleSubmit = async e => {
    e.preventDefault();
    if (!file) return setError("Please select a PDF file.");
    setLoading(true);
    setError("");
    try {
      const blob = await rotatePdf(file, rotations);
      setDownloadUrl(URL.createObjectURL(blob));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-8">
      <h1 className="text-5xl font-extrabold text-gray-800 mb-8">
        PDF Toolbox
      </h1>

      <fieldset className="relative w-full max-w-md border-2 border-blue-500 rounded-xl bg-white p-6 overflow-hidden">
        <legend className="absolute left-1/2 top-0 transform -translate-x-1/2 -translate-y-1/2 bg-white px-4 text-blue-600 font-semibold text-xl">
          🚀 Rotate pages
        </legend>

        <form onSubmit={handleSubmit} className="space-y-6 mt-4">
          <div className="flex flex-col">
            <label className="mb-2 text-gray-700 font-medium">Upload PDF</label>
            <input
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-3 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200"
            />
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Page Rotations
            </h2>
            <div className="space-y-4">
              {rotations.map((r, idx) => (
                <div key={idx} className="grid grid-cols-3 gap-4 items-end">
                  <div>
                    <label className="block text-sm text-gray-600">Page</label>
                    <input
                      type="number"
                      min={1}
                      value={r.page}
                      onChange={e =>
                        handleRotationChange(idx, "page", +e.target.value)
                      }
                      className="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-600">
                      Degrees
                    </label>
                    <input
                      type="number"
                      step={90}
                      placeholder="90"
                      value={r.degrees === "" ? "" : r.degrees}
                      onChange={e => {
                        const v = e.target.value;
                        handleRotationChange(
                          idx,
                          "degrees",
                          v === "" ? "" : +v
                        );
                      }}
                      className="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => removeRotation(idx)}
                    className="px-3 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={addRotation}
                className="px-4 py-2 bg-green-100 text-green-800 rounded-md hover:bg-green-200"
              >
                + Add Rotation
              </button>
            </div>
          </div>

          {error && <p className="text-red-600">⚠️ {error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Rotating..." : "Rotate PDF"}
          </button>

          {downloadUrl && (
            <a
              href={downloadUrl}
              download="rotated.pdf"
              className="block text-center text-blue-600 hover:underline mt-4"
            >
              📥 Download Rotated PDF
            </a>
          )}
        </form>
      </fieldset>
    </div>
  );
}
