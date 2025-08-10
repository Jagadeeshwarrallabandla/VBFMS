import React, { useState } from 'react';
import './Home.css';
import file_logo from '../VBMFS/Images/file_logo.jpg';

const Home = () => {
  const [text, setText] = useState('');
  const [backend, setBackend] = useState('');

  // Extract filename, main folder, and subfolder from voice command
  const parseVoiceCommand = (command) => {
    let lower = command.toLowerCase();
    let filename = "";
    let mainfolder = "";
    let subfolder = "";

    // Split by "move" and "to"
    if (lower.includes("move") && lower.includes("to")) {
      let afterMove = lower.split("move")[1].trim();
      let parts = afterMove.split("to");

      filename = parts[0]?.trim();

      // Check for subfolder phrases
      if (parts[1]?.includes("and place it on")) {
        let mainAndSub = parts[1].split("and place it on");
        mainfolder = mainAndSub[0]?.trim();
        subfolder = mainAndSub[1]?.trim();
      } else if (parts[1]?.includes(" in ")) {
        let mainAndSub = parts[1].split(" in ");
        mainfolder = mainAndSub[0]?.trim();
        subfolder = mainAndSub[1]?.trim();
      } else {
        mainfolder = parts[1]?.trim();
      }
    }

    return { filename, mainfolder, subfolder };
  };

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
      console.log("🎙 Recognized:", transcript);

      const { filename, mainfolder, subfolder } = parseVoiceCommand(transcript);

      if (!filename || !mainfolder) {
        setBackend("❌ Could not identify file or folder from your voice.");
        return;
      }

      try {
        const res = await fetch('http://localhost:5000/move_file', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filename, mainfolder, subfolder })
        });

        const data = await res.json();
        console.log("Backend Response:", data);

        if (data.message) {
          setBackend(`✅ ${data.message}`);
        } else if (data.error) {
          setBackend(`❌ ${data.error}`);
        } else {
          setBackend("❓ No proper response from backend.");
        }
      } catch (err) {
        console.error("Fetch Error:", err);
        setBackend("❌ Failed to fetch from backend.");
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech Recognition Error:", event.error);
      setBackend(`❌ Speech error: ${event.error}`);
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
