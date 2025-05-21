import React, { useState } from "react";
import "./App.css";

export default function App() {
  const [docType, setDocType] = useState("idcard");
  const [mrz1, setMrz1] = useState("");
  const [mrz2, setMrz2] = useState("");
  const [mrz3, setMrz3] = useState("");
  const [result, setResult] = useState(null);

  const maxLen = docType === "passport" ? 44 : 30;

  const detectAndReorderMRZ = (lines) => {
    const cleaned = lines.map((l) => l.trim().toUpperCase());
    let docLine = "", personalLine = "", nameLine = "";

    for (const line of cleaned) {
      if (/^ID[A-Z0-9<]{3,}/.test(line)) {
        docLine = line;
      } else if (/^\d{6}[MF<]/.test(line)) {
        personalLine = line;
      } else if (line.includes("<<")) {
        nameLine = line;
      }
    }

    if (docLine && personalLine && nameLine) {
      // Reorder into what the backend expects:
      // mrz1 = name, mrz2 = doc, mrz3 = personal
      return {
        mrz1: nameLine,
        mrz2: docLine,
        mrz3: personalLine,
      };
    }

    return {
      mrz1: cleaned[0] || "",
      mrz2: cleaned[1] || "",
      mrz3: cleaned[2] || "",
    };
  };


  const validate = async () => {
    let body;

    if (docType === "passport") {
      body = { mrz1, mrz2 };
    } else {
      body = detectAndReorderMRZ([mrz1, mrz2, mrz3]);
    }

    const res = await fetch("/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    setResult(data);
  };

  const padToLen = (setter, currentValue) => {
    const fillerNeeded = maxLen - currentValue.length;
    if (fillerNeeded > 0) {
      setter(currentValue + "<".repeat(fillerNeeded));
    }
  };

  const resetField = (setter) => setter("");

  return (
    <div className="app">
      <header className="app-header">
        <h1>MRZ Validator</h1>
        <div className="doc-type-toggle">
          <button
            className={`toggle-button ${docType === "passport" ? "active" : ""}`}
            onClick={() => {
              setDocType("passport");
              setMrz3("");
              setResult(null);
            }}
          >
            Passport
          </button>
          <button
            className={`toggle-button ${docType === "idcard" ? "active" : ""}`}
            onClick={() => {
              setDocType("idcard");
              setResult(null);
            }}
          >
            ID Card
          </button>
        </div>
      </header>

      <input
        placeholder={`Line 1 (${maxLen} characters)`}
        value={mrz1}
        onChange={(e) => setMrz1(e.target.value.toUpperCase())}
        maxLength={maxLen}
      />
      <div className="button-container">
        <button className="button-30" onClick={() => padToLen(setMrz1, mrz1)}>Pad</button>
        <button className="button-30" onClick={() => resetField(setMrz1)}>Reset</button>
      </div>

      <input
        placeholder={`Line 2 (${maxLen} characters)`}
        value={mrz2}
        onChange={(e) => setMrz2(e.target.value.toUpperCase())}
        maxLength={maxLen}
      />
      <div className="button-container">
        <button className="button-30" onClick={() => padToLen(setMrz2, mrz2)}>Pad</button>
        <button className="button-30" onClick={() => resetField(setMrz2)}>Reset</button>
      </div>

      {docType === "idcard" && (
        <>
          <input
            placeholder="Line 3 (30 characters)"
            value={mrz3}
            onChange={(e) => setMrz3(e.target.value.toUpperCase())}
            maxLength={30}
          />
          <div className="button-container">
            <button className="button-30" onClick={() => padToLen(setMrz3, mrz3)}>Pad</button>
            <button className="button-30" onClick={() => resetField(setMrz3)}>Reset</button>
          </div>
        </>
      )}

      <div className="button-container">
        <button className="button-30" id="button-validate" onClick={validate}>
          Validate
        </button>
      </div>

      {result && (
        <div className="results">
          <h3>Validation Results:</h3>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <>
              <ul>
                {Object.entries(result).map(([key, value]) =>
                  typeof value === "boolean" ? (
                    <li key={key}>
                      {key.replace(/_/g, " ")}:{" "}
                      <strong style={{ color: value ? "green" : "red" }}>
                        {value ? "Valid ✅" : "Invalid ❌"}
                      </strong>
                    </li>
                  ) : null
                )}
              </ul>

              {(result.surname || result.given_names) && (
                <>
                  <h3>Extracted Personal Info:</h3>
                  <ul>
                    {result.surname && <li>Last Name: <strong>{result.surname}</strong></li>}
                    {result.given_names && <li>First Name(s): <strong>{result.given_names}</strong></li>}
                    {result.birth_date_raw && <li>Date of Birth: <strong>{result.birth_date_raw}</strong></li>}
                    {result.sex_raw && <li>Sex: <strong>{result.sex_raw}</strong></li>}
                    {result.nationality && <li>Nationality: <strong>{result.nationality}</strong></li>}
                    {result.expiry_date_raw && <li>Expiry Date: <strong>{result.expiry_date_raw}</strong></li>}
                  </ul>
                </>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
