import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("Loading...");

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

  return (
    <div style={{ padding: "30px" }}>
      <h1>Research Paper Briefing Agent</h1>

      <h3>Backend Status:</h3>

      <p>{message}</p>
    </div>
  );
}

export default App;