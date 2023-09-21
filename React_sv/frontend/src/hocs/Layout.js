import React, { useEffect } from 'react';
import Navbar from '../components/Navbar';
import { connect } from 'react-redux';
import { load_user } from '../actions/auth';

const Layout = ({ load_user,children }) => {
    useEffect(() => {
        load_user();
    }, []);

    return (
        <div>
            <Navbar />
            {children}
        </div>
    );
};

export default connect(null, {load_user})(Layout);
