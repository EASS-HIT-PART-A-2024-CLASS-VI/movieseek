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
        style={{ width: "100%", padding: "8px", border: "1px solid #ccc", borderRadius: "4px" }}
      />
    </div>
  );
};

export default InputField;
