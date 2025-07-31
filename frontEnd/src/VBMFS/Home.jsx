import React , {useState} from 'react'
import './Home.css'
import file_logo from '../VBMFS/Images/file_logo.jpg'

const Home = () =>{
  const [text,setText] = useState(' ');

  const voiceRecording = () => {
    if (!('webkitSpeechRecognition' in window)){
      alert('webkitSpeechRecognition doesnt exisits in the Browser')
    }
    const voice = new window.webkitSpeechRecognition();
    voice.lang = 'en-US';
    voice.continuous = false;
    voice.continuous = false;

    voice.onresult = (response) => {
       const speechResult = response.results[0][0].transcript;
      setText(speechResult);
    };

    voice.onerror = (response) => {
      console.error('Speech recognition error:', response.error);
    };

    voice.start()
  }

  return (
    <>
    <div className="main-div">
      <div className="left-div">
        <div> 
          <img src={file_logo} alt="Project_Logo" /> <span>VBFMS</span>
        </div>
       
       <div className="ul-design">
        <ul>
          <li>Serach</li>
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
                <i class="fa-solid fa-gear settings"></i>
                </div>

                
            </div>
      <div>
              <i className="fa-solid fa-microphone mic-container" onClick={voiceRecording}></i>
              <p className='text-output'>{text}</p>
      </div>

      
      </div>

    </div>
    </>
  )
}


export default Home
