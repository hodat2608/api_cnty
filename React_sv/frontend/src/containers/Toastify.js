import React from 'react';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const showNotification = (message, type = 'info') => {
  toast[type](message, {
    position: 'top-center',
    autoClose: 1000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
  });
};

function Toast1() {
  return (
    <div>
      <button onClick={() => showNotification('Wow so easy!')}>Notify!</button>
      <ToastContainer />
    </div>
  );
}

export default Toast1;
