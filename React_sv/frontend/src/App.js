
import './styles.css';
import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NoteList from './pages/NoteList';
import Detail_notes from './pages/Detail_notes'; 
import { Provider } from 'react-redux';
import store from './store';
import Home from './components/Home';
import Layout from './hocs/Layout';
import Google from './containers/Google';
import Main from './containers/Main';
import ResetPassword from './containers/ResetPassword';
import ResetPasswordConfirm from './containers/ResetPasswordConfirm';
import Notificationresetpassword from './containers/Notification_resetpassword';
import Facebook from './containers/Facebook';
import ChangePassword from './containers/ChangePassword';
import SignInSide from './containers/SignInSide';
import SignUp from './containers/SignUpSide';
import Toast1 from './containers/Toastify';
import { ToastContainer, toast } from 'react-toastify';
// import Dashboard from './dashboard/Dashboard';
import VeryfiedAccount from './containers/VeryfiedAccount';
import Dashboard from './dash_board/Dashboard';
function App() {
  return (
    <Provider store={store}>
    <BrowserRouter>
      <Layout />
      <ToastContainer />
        <Routes>

          <Route path="/all_note/" element={<NoteList />} />
          <Route path="/detail_note/:id" element={<Detail_notes/>} />

          <Route path='/main/' element={<Main/>} />

          <Route path="/" element={<Home/>} />
          <Route path='/google/' element={<Google/>} />
          <Route path='/facebook/' element={<Facebook/>} />

          <Route path='/activate/:uid/:token/' element={<VeryfiedAccount/>}/>
          
          <Route path='/reset-password/' element={<ResetPassword/>} />
          <Route path='/password/reset/confirm/:uid/:token/' element={<ResetPasswordConfirm/>} /> 

          <Route path='/change-password/' element={<ChangePassword/>} />   

          <Route path='/notification/' element={<Notificationresetpassword/>} />
           
          <Route path='/login/' element={<SignInSide/>} />
          <Route path='/signup/' element={<SignUp/>} />
          <Route path='/toats/' element={<Toast1/>} />
          <Route path='/dashboard/' element={<Dashboard/>} />
        </Routes>
    </BrowserRouter>
  </Provider>
  );
}

export default App;

