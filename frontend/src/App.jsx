import { BrowserRouter, Routes, Route } from "react-router-dom"
import './App.css'
import NavBar from "./components/navbar/navbar"
import Home from "./pages/home/home"
import Dex from "./pages/dex/dex"

function App() {

  return (
    <>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dex" element={<Dex />} />
        </Routes>
      </BrowserRouter>
        
    </>
  )
}

export default App
