import React, { useState } from "react";
import "./App.css";

export default function App() {
  const [mrz1, setMrz1] = useState("");
  const [mrz2, setMrz2] = useState("");
  const [result, setResult] = useState(null);

  const validate = async () => {
    const res = await fetch("/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mrz1, mrz2 }),
    });
    const data = await res.json();
    setResult(data);
  };

  const padTo44 = (setter, currentValue) => {
    const fillerNeeded = 44 - currentValue.length;
    if (fillerNeeded > 0) {
      setter(currentValue + "<".repeat(fillerNeeded));
    }
  };

  const resetField = (setter) => {
    setter("");
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Passport MRZ Validator</h1>
      </header>

      <input
        placeholder="Line 1 (44 characters)"
        value={mrz1}
        onChange={(e) => setMrz1(e.target.value.toUpperCase())}
        maxLength={44}
      />
      <div className="button-container">
        <button className="button-30" onClick={() => padTo44(setMrz1, mrz1)}>Pad to 44</button>
        <button className="button-30" onClick={() => resetField(setMrz1)}>Reset</button>
      </div>

      <input
        placeholder="Line 2 (44 characters)"
        value={mrz2}
        onChange={(e) => setMrz2(e.target.value.toUpperCase())}
        maxLength={44}
      />
      <div className="button-container">
        <button className="button-30" onClick={() => padTo44(setMrz2, mrz2)}>Pad to 44</button>
        <button className="button-30" onClick={() => resetField(setMrz2)}>Reset</button>
      </div>

      <div className="button-container">
        <button className="button-30" id="button-validate" role="button" onClick={validate}>
          Validate
        </button>
      </div>

      {/* This is now correctly inside the .app container */}
      {result && (
        <div className="results">
          <h3>Validation Results:</h3>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <ul>
              {Object.entries(result).map(([key, value]) => (
                <li key={key}>
                  {key.replace(/_/g, " ")}:{" "}
                  <strong style={{ color: value ? "green" : "red" }}>
                    {value ? "Valid ✅" : "Invalid ❌"}
                  </strong>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
