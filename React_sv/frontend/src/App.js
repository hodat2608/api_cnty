
import './App.css';
import Header from "./components/header";
import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import './App.css';
import NoteList from './pages/NoteList';
import Detail_notes from './pages/Detail_notes'; 
import { Provider } from 'react-redux';
import store from './store';
import Login_user from './users/Login';
import Signup_user from './users/Signup';
import Home from './components/Home';
import Layout from './hocs/Layout';

function App() {
  return (
    <Provider store={store}>
    <BrowserRouter>
      {/* <div className="container dark">
        <div className="app"> */}
          <Layout />
          <Routes>
            <Route path="/all_note/" element={<NoteList />} />
            <Route path="/detail_note/:id" element={<Detail_notes/>} />
            <Route path="/login" element={<Login_user/>} />
            <Route path="/signup" element={<Signup_user/>} />
            <Route path="/" element={<Home/>} />
          </Routes>
        {/* </div>
      </div> */}
    </BrowserRouter>
  </Provider>
  );
}

export default App;

