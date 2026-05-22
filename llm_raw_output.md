# LLM Output

=== FILE: src/App.jsx ===
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { HashRouter } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import { Toast } from 'react-toastify';
import { FaUser } from 'react-icons/fa';
import { FiLogIn, FiLogOut } from 'react-icons/fi';
import { format, parseISO } from 'date-fns';
import { useForm } from 'react-hook-form';
import { clsx } from 'clsx';
import 'react-toastify/dist/ReactToastify.css';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [user, setUser] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [newSession, setNewSession] = useState({ score: 0, date: new Date() });
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const { register, handleSubmit } = useForm();

  const handleLogin = async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/login`, data);
      const user = response.data;
      setUser(user);
      setIsLoggedIn(true);
      toast.success('Logged in successfully');
    } catch (error) {
      toast.error('Invalid credentials');
    }
  };

  const handleLogout = () => {
    axios.post(`${BASE_URL}/logout`);
    setUser(null);
    setIsLoggedIn(false);
    toast.success('Logged out successfully');
  };

  const handleCreateSession = async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/sessions`, data);
      const session = response.data;
      setSessions([...sessions, session]);
      toast.success('Session created successfully');
    } catch (error) {
      toast.error('Failed to create session');
    }
  };

  const handleUpdateSession = async (id, data) => {
    try {
      const response = await axios.put(`${BASE_URL}/sessions/${id}`, data);
      const updatedSession = response.data;
      setSessions(sessions.map((session) => (session.id === id ? updatedSession : session)));
      toast.success('Session updated successfully');
    } catch (error) {
      toast.error('Failed to update session');
    }
  };

  const handleDeleteSession = async (id) => {
    try {
      await axios.delete(`${BASE_URL}/sessions/${id}`);
      setSessions(sessions.filter((session) => session.id !== id));
      toast.success('Session deleted successfully');
    } catch (error) {
      toast.error('Failed to delete session');
    }
  };

  const handleFetchSessions = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/sessions`);
      const sessions = response.data;
      setSessions(sessions);
    } catch (error) {
      toast.error('Failed to fetch sessions');
    }
  };

  useEffect(() => {
    handleFetchSessions();
  }, []);

  return (
    <HashRouter>
      <div className="container mx-auto p-4 mt-10">
        <header className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold">Game Session Tracker</h1>
          {isLoggedIn ? (
            <button
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              onClick={handleLogout}
            >
              <FiLogOut className="mr-2" /> Logout
            </button>
          ) : (
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              onClick={() => toast.success('Please login first')}
            >
              <FaUser className="mr-2" /> Login
            </button>
          )}
        </header>
        <main className="flex flex-col items-center">
          {isLoggedIn ? (
            <form
              className="flex flex-col w-full max-w-lg"
              onSubmit={handleSubmit(handleCreateSession)}
            >
              <label className="block text-sm font-medium text-gray-700" htmlFor="score">
                Score
              </label>
              <input
                className="block w-full p-2 pl-10 text-sm text-gray-700 border border-gray-200 rounded-lg"
                type="number"
                id="score"
                {...register('score')}
              />
              <label className="block text-sm font-medium text-gray-700" htmlFor="date">
                Date
              </label>
              <input
                className="block w-full p-2 pl-10 text-sm text-gray-700 border border-gray-200 rounded-lg"
                type="date"
                id="date"
                {...register('date')}
              />
              <button
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4"
                type="submit"
              >
                Create Session
              </button>
            </form>
          ) : (
            <form
              className="flex flex-col w-full max-w-lg"
              onSubmit={handleSubmit(handleLogin)}
            >
              <label className="block text-sm font-medium text-gray-700" htmlFor="username">
                Username
              </label>
              <input
                className="block w-full p-2 pl-10 text-sm text-gray-700 border border-gray-200 rounded-lg"
                type="text"
                id="username"
                {...register('username')}
              />
              <label className="block text-sm font-medium text-gray-700" htmlFor="password">
                Password
              </label>
              <input
                className="block w-full p-2 pl-10 text-sm text-gray-700 border border-gray-200 rounded-lg"
                type="password"
                id="password"
                {...register('password')}
              />
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
                type="submit"
              >
                <FiLogIn className="mr-2" /> Login
              </button>
            </form>
          )}
          <ul className="flex flex-col w-full max-w-lg mt-4">
            {sessions.map((session) => (
              <li key={session.id} className="flex justify-between items-center py-2 px-4 bg-gray-100 rounded-lg mb-2">
                <span className="text-sm font-medium text-gray-700">
                  {format(parseISO(session.date), 'yyyy-MM-dd')} - {session.score} points
                </span>
                <div className="flex items-center">
                  <button
                    className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1 px-2 rounded mr-2"
                    onClick={() => handleUpdateSession(session.id, { score: session.score + 10 })}
                  >
                    +10 points
                  </button>
                  <button
                    className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded"
                    onClick={() => handleDeleteSession(session.id)}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </main>
      </div>
      <ToastContainer />
    </HashRouter>
  );
}

export default App;
=== END ===

=== FILE: src/main.jsx ===
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
=== END ===

=== FILE: src/index.css ===
@tailwind base;
@tailwind components;
@tailwind utilities;
=== END ===

=== FILE: src/api.js ===
// No need for this file as API calls are made directly in App.jsx
=== END ===