import { Box, Button } from "@chakra-ui/react"
import { Route, Routes } from "react-router-dom"
import Navbar from "./components/ui/Navbar"
import HomePage from "./pages/HomePage"
import TestPage from "./pages/TestPage"

function App() {
  return (
    <Box minH={"100vh"}>
      <Navbar/>
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/test" element={<TestPage/>}/>
      </Routes>
    </Box>
  );
}

export default App
