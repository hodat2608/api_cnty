
import './App.css';
import Header from "./components/header";

import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import './App.css';
import NoteList from './pages/List_note';
import Detail_notes from './pages/Detail_notes'; 


function App() {
  return (
    <BrowserRouter>
      <div className="container dark">
        <div className="app">
          <Header />
          <Routes>
            <Route path="/all_note/" element={<NoteList />} />
            <Route path="/detail_note/:id" element={<Detail_notes/>} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;

