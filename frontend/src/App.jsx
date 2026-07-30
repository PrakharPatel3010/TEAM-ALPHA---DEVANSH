import { useEffect, useState } from "react";

function App() {
  // Backend status message
  const [message, setMessage] = useState("Loading...");

  // Selected PDF file
  const [selectedFile, setSelectedFile] = useState(null);

  // Extracted text from PDF
  const [pdfText, setPdfText] = useState("");

  // Upload status
  const [loading, setLoading] = useState(false);

  // Check if backend is running
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

  // Upload PDF to backend
  const uploadPDF = async () => {
    if (!selectedFile) {
      alert("Please select a PDF first.");
      return;
    }

    setLoading(true);

    // Create form data
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      // Store extracted text
      setPdfText(data.chunks.join("\n\n"));
    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    }

    setLoading(false);
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

      <h3>Backend Status</h3>
      <p>{message}</p>

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

      <hr />

      <h2>Extracted Text</h2>

      <pre
        style={{
          whiteSpace: "pre-wrap",
          textAlign: "left",
          backgroundColor: "#f5f5f5",
          padding: "20px",
          borderRadius: "10px",
          maxHeight: "500px",
          overflowY: "scroll",
        }}
      >
        {pdfText}
      </pre>
    </div>
  );
}

export default App;