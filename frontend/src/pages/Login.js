import React, { useState } from 'react';
import Background from '../components/Background';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // For now, just log the credentials, later you'll connect to the backend.
    console.log('Username:', username);
    console.log('Password:', password);

    // Here, you can add logic to check the user against the backend.
  };

  return (
    <Background>
      <div className="bg-white p-8 rounded shadow-lg max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">Login</h2>
        <form>
          <div className="mb-4">
            <label htmlFor="username" className="block text-gray-700 font-medium mb-2">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="password" className="block text-gray-700 font-medium mb-2">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="mb-4">
            <button
              type="button"
              onClick={handleLogin}
              className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Login
            </button>
          </div>
        </form>
        <div>
          <button className="w-full bg-gray-500 text-white p-2 rounded hover:bg-gray-600">
            Register
          </button>
        </div>
      </div>
    </Background>
  );
};

export default Login;
