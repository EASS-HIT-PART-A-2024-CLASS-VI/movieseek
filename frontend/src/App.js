// src/App.js
import React from 'react';
import Login from './components/Login';  // Import the Login component

function App() {
  return (
    <div className="App">
      <h1>Welcome to My App</h1>
      <Login /> {/* Rendering the Login component */}
    </div>
  );
}

export default App;
