import './Home.css'
import file_logo from '../VBMFS/Images/file_logo.jpg'

const Home = () =>{
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
      <div className="mic-container">
                <i className="fa-solid fa-microphone mic"></i>
             </div>
      </div>

    </div>
    </>
  )
}


// import React from 'react'
// import './Home.css'

// const Home = () => {
//   return (
//     <>
//     <div className = " d-flex main-div ">
//         <div className = "left-div" >
//           <ul>Filter</ul>
//           <ul>Lo</ul>
//           <ul>Rename</ul>
//           <ul>Search</ul>
//           <ul>Settings</ul>
//         </div>

//         <div className="right-div">

//             <div className="top-content">
//                 <h3>Voice Based File Management System</h3>
//                 <i className="fa-solid fa-magnifying-glass search"></i>
//             </div>

//             <div className="mic-container">
//                 <i className="fa-solid fa-microphone mic"></i>
//             </div>
//         </div>

//     </div>
//     </>
//   )
// }

export default Home
