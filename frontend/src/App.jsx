import { useEffect, useState } from "react";

function App() {
  // Backend status
  const [message, setMessage] = useState("Loading...");

  // Selected PDF
  const [selectedFile, setSelectedFile] = useState(null);

  // Upload response
  const [pdfText, setPdfText] = useState("");

  // Uploaded filename
  const [filename, setFilename] = useState("");

  // AI Summary
  const [summary, setSummary] = useState(null);

  // Loading states
  const [loading, setLoading] = useState(false);
  const [summaryLoading, setSummaryLoading] = useState(false);

  // Check backend status
  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);
      })
      .catch((error) => {
        console.error(error);
        setMessage("Could not connect to backend");
      });
  }, []);

  // Upload PDF
  const uploadPDF = async () => {
    if (!selectedFile) {
      alert("Please select a PDF first.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      console.log(data);

      setFilename(data.filename);
      setPdfText(JSON.stringify(data, null, 2));

      // Clear previous summary
      setSummary(null);

    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    }

    setLoading(false);
  };

  // Summarize uploaded paper
  const summarizePaper = async () => {
    if (!filename) {
      alert("Upload a PDF first.");
      return;
    }

    setSummaryLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          filename: filename,
        }),
      });

      const data = await response.json();

      console.log(data);

      setSummary(data);

    } catch (error) {
      console.error(error);
      alert("Summarization failed.");
    }

    setSummaryLoading(false);
  };

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Arial",
        maxWidth: "1000px",
        margin: "auto",
      }}
    >
      <h1>Research Paper Briefing Agent</h1>

      <hr />

      <h2>Select Research Paper</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(event) => {
          setSelectedFile(event.target.files[0]);
        }}
      />

      <br />
      <br />

      <button onClick={uploadPDF} disabled={loading}>
        {loading ? "Uploading..." : "Upload PDF"}
      </button>

      <button
        onClick={summarizePaper}
        disabled={!filename || summaryLoading}
        style={{ marginLeft: "15px" }}
      >
        {summaryLoading ? "Generating..." : "Summarize Paper"}
      </button>

      <hr />

      <h2>Upload Response</h2>

      <pre
        style={{
          whiteSpace: "pre-wrap",
          textAlign: "left",
          backgroundColor: "#f5f5f5",
          padding: "20px",
          borderRadius: "10px",
          maxHeight: "250px",
          overflowY: "scroll",
        }}
      >
        {pdfText}
      </pre>

      {summary && (
        <>
          <hr />

          <h2>AI Summary</h2>

          <div
            style={{
              backgroundColor: "#f5f5f5",
              padding: "20px",
              borderRadius: "10px",
              textAlign: "left",
            }}
          >
            <h3>Overview</h3>
            <p>{summary.overview}</p>

            <h3>Methods</h3>
            <p>{summary.methods}</p>

            <h3>Results</h3>
            <p>{summary.results}</p>

            <h3>Limitations</h3>
            <p>{summary.limitations}</p>
          </div>
        </>
      )}
    </div>
  );
}

export default App;