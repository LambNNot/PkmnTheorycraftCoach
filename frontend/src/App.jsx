import { BrowserRouter, Routes, Route } from "react-router-dom"
import './App.css'
import NavBar from "./components/navbar/navbar"
import Home from "./pages/home/home"
import Dex from "./pages/dex/dex"
import MySets from "./pages/mySets/mySets"

function App() {

  return (
    <>
      <BrowserRouter>
        <NavBar />
        <Routes className="g-4">
          <Route path="/" element={<Home />} />
          <Route path="/dex" element={<Dex />} />
          <Route path="/mySets" element={<MySets />} />
        </Routes>
      </BrowserRouter>
        
    </>
  )
}

export default App
