import React from "react";

const InputField = ({ type, name, placeholder, value, onChange }) => {
  return (
    <div style={{ marginBottom: "10px" }}>
      <input
        type={type}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        style={{
          width: "100%",
          padding: "12px",
          border: "2px solid #ccc",
          borderRadius: "25px",
          fontSize: "16px",
        }}
      />
    </div>
  );
};

export default InputField;
