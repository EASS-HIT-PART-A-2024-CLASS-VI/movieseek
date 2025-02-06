import React, { useState } from "react";

const Register = () => {
  const [userData, setUserData] = useState({ username: "", password: "" });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      setMessage("Registration successful! Redirecting to login...");
      setTimeout(() => {
        window.location.href = "/"; // Redirect to login page
      }, 2000);
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh", // Full viewport height for centering
        flexDirection: "column",
      }}
    >
      <div
        style={{
          width: "300px",
          textAlign: "center",
        }}
      >
        <h2>Register</h2>
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={userData.username}
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "10px",
              border: "1px solid #ccc",
              borderRadius: "5px",
              fontSize: "16px",
            }}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={userData.password}
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "15px",
              border: "1px solid #ccc",
              borderRadius: "5px",
              fontSize: "16px",
            }}
          />
          <button
            type="submit"
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: "#28a745", // Green color for register button
              color: "white",
              border: "none",
              borderRadius: "5px",
              fontSize: "16px",
              cursor: "pointer",
            }}
          >
            Register
          </button>
        </form>
        {message && <p style={{ marginTop: "10px", color: message.includes("successful") ? "green" : "red" }}>{message}</p>}
        <p style={{ marginTop: "10px" }}>
          Already have an account? <a href="/">Login here</a>
        </p>
      </div>
    </div>
  );
};

export default Register;
