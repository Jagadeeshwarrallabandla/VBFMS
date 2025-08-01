import React, { useEffect, useState } from 'react';
import './Home.css';
import file_logo from '../VBMFS/Images/file_logo.jpg';

const Home = () => {
  const [text, setText] = useState('');
  const [backend, setBackend] = useState('');

  // Connecting to Backend 
  useEffect(() => {
    fetch('http://localhost:5000/SuccessFullMessage')
      .then(response => response.json())
      .then(data => {
        setBackend(data.message);
      })
      .catch(error => {
        setBackend('Error fetching from backend: ' + error.message);
      });
  }, []);

  // Function that Converts Sppech to Text using WebKitSpeech Recognition 
  const voiceRecording = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser.');
      return;
    }

    const voice = new window.webkitSpeechRecognition();
    voice.lang = 'en-US';
    voice.continuous = false;

    voice.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      setText(speechResult);
    };

    voice.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
    };

    voice.start();
  };

  return (
    // Developing UI Begins Here
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
          <p className="text-output">{text}</p>
          <p>{backend}</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
