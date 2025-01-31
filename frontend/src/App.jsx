import { Box, Button } from "@chakra-ui/react"
import { Route, Routes } from "react-router-dom"
import Navbar from "./components/ui/Navbar"
import ChatPage from "./pages/ChatPage"
import Footer from "./components/ui/Footer"
import LoginPage from "./pages/LoginPage"

function App() {
  return (
    <div className="font-[Inter] bg-gray-50 flex flex-col min-h-screen">
      <Navbar/>
      <Routes>
        <Route path="/chat" element = {<ChatPage/>}/>
        <Route path="/login" element = {<LoginPage/>}/>
      </Routes>
      <Footer/>  
    </div>

  );
}

export default App
