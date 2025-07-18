import React from 'react'
import './Home.css'

const Home = () => {
  return (
    <>
    <div className = " d-flex main-div ">
        <div className = "left-div" >

        </div>

        <div className="right-div">
  <div className="top-content">
    <h3>Voice Based File Management System</h3>
    <i className="fa-solid fa-magnifying-glass search"></i>
  </div>
  <div className="mic-container">
    <i className="fa-solid fa-microphone mic"></i>
  </div>
</div>

    </div>
    </>
    // <div class = "main-div d-flex justify-content-center ">
    //     <div class="left-div" className='left-div'>Hello</div>
    //     <div class="right-div d-flex justify-content-center align-items-center">
    //         <i class="fa-solid fa-microphone color-white "></i>
    //     </div>
      
    // </div>
  )
}

export default Home
