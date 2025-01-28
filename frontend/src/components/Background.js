import React from "react";

const Background = ({ children }) => {
  return (
    <div className="bg-gray-800 min-h-screen flex items-center justify-center">
      {children}
    </div>
  );
};

export default Background;
