import React, { useState } from "react";
import InputField from "../components/InputField";

const Login = () => {
  const [userData, setUserData] = useState({ username: "", password: "" });

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Logging in with:", userData);
    // Here you'd call an API or handle authentication logic
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        flexDirection: "column", // Aligns items in a column layout
      }}
    >
      <h2>Login</h2>
      <form onSubmit={handleSubmit} style={{ textAlign: "center" }}>
        <InputField
          type="text"
          name="username"
          placeholder="Username"
          value={userData.username}
          onChange={handleChange}
        />
        <InputField
          type="password"
          name="password"
          placeholder="Password"
          value={userData.password}
          onChange={handleChange}
        />
        <button
          type="submit"
          style={{
            marginTop: "10px",
            padding: "10px 15px",
            cursor: "pointer",
            border: "none",
            backgroundColor: "#007bff",
            color: "white",
            borderRadius: "5px",
            fontSize: "16px",
          }}
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
