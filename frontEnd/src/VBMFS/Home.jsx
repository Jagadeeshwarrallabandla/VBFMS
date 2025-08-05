import React, { useState } from 'react';
import './Home.css';
import file_logo from '../VBMFS/Images/file_logo.jpg';

const Home = () => {
  const [text, setText] = useState('');
  const [backend, setBackend] = useState('');

  // Extract file name from voice command
  const extractFileName = (command) => {
    const lower = command.toLowerCase();
    if (lower.includes('move') && lower.includes('to')) {
      const parts = lower.split('move')[1].split('to');
      return parts[0]?.trim(); // extract filename
    }
    return null;
  };

  // Voice recording + backend communication
  const voiceRecording = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser.');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;

    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript;
      setText(transcript);
      console.log("Recognized Speech:", transcript);

      const filename = extractFileName(transcript);
      if (!filename) {
        setBackend("Couldn't identify file name from your voice.");
        return;
      }

      try {
        const res = await fetch('http://localhost:5000/MoveFilesource_Folder', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ filename }),
        });

        const data = await res.json();
        console.log("Backend response:", data);

        // Conditions if File not handled correctly
        if (data.message) {
          setBackend(`✅ ${data.message}`);
        } else if (data.error) {
          setBackend(`❌ ${data.error}`);
        } else {
          setBackend('❓ No proper response from backend.');
        }
      } catch (err) {
        console.error('❌ Error communicating with backend:', err);
        setBackend('❌ Failed to fetch from backend.');
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setBackend(`❌ Please On your : ${event.error}`);
    };

    recognition.start();
  };

  return (
    <div className="main-div">
      <div className="left-div">
        <div>
          <img src={file_logo} alt="Project_Logo" />
          <span>VBFMS</span>
        </div>
        <div className="ul-design">
          <ul>
            <li>Search</li>
            <li>Library</li>
            <li>Filter</li>
            <li>Rename</li>
          </ul>
        </div>
      </div>

      <div className="right-div">
        <div className="top-content">
          <h3>Voice Based File Management System</h3>
          <div className="search-settings">
            <i className="fa-solid fa-magnifying-glass search"></i>
            <i className="fa-solid fa-gear settings"></i>
          </div>
        </div>

        <div className="mic">
          <div className="mic-container" onClick={voiceRecording}>
            <i className="fa-solid fa-microphone"></i>
          </div>
          <p className="text-output">🎙 {text}</p>
          <p className="backend-output">{backend}</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
