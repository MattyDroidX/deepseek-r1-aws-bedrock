import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const handleGenerate = async () => {
    if (!prompt) return;

    try {
      const res = await axios.post("http://localhost:8000/generate/", {
        prompt: prompt,
      });

      setResponse(res.data.response);
    } catch (error) {
      console.error("Error fetching response:", error);
      setResponse("Failed to generate response.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>DeepSeek-R1 Chat</h1>
      <textarea
        rows="4"
        cols="50"
        placeholder="Enter a prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <br />
      <button onClick={handleGenerate} style={{ marginTop: "10px" }}>
        Generate
      </button>
      <h2>Response:</h2>
      <p>{response}</p>
    </div>
  );
}

export default App;
