import React, { useState } from "react";
import "./App.css";

function App() {
  // State variables for form inputs
  const [url, setUrl] = useState("");
  const [targetPrice, setTargetPrice] = useState("");
  const [email, setEmail] = useState("");
  const [responseMessage, setResponseMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent page reload
    setResponseMessage("Sending request...");

    // Prepare data to send to the backend
    const requestData = {
      url: url,
      targetPrice: parseFloat(targetPrice),
      email: email,
    };

    try {
      // Send POST request to the Flask backend
      const response = await fetch("http://127.0.0.1:5000/track-price", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const responseData = await response.json();

      if (response.ok) {
        setResponseMessage(responseData.message);
      } else {
        setResponseMessage(responseData.error || "An error occurred.");
      }
    } catch (error) {
      setResponseMessage("Failed to connect to the server.");
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Price Tracker</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              Product URL:
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Target Price:
              <input
                type="number"
                value={targetPrice}
                onChange={(e) => setTargetPrice(e.target.value)}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Email:
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
          </div>
          <button type="submit">Track Price</button>
        </form>
        {responseMessage && <p>{responseMessage}</p>}
      </header>
    </div>
  );
}

export default App;
