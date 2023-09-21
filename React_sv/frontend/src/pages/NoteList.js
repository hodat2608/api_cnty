import React, { useState, useEffect } from 'react';
import { ReactComponent as AddIcon } from '../assets/add.svg'
import { Link  } from 'react-router-dom';
import axios from 'axios';
import { logout } from '../actions/auth';
import { connect } from 'react-redux';

const NoteList = ({ logout }) => {
    
    const [notes, setNotes] = useState([]);
    const [addingNote, setAddingNote] = useState(false);
    const[formData,setFormData] =useState({note_title:''})

    useEffect(()=>{get_notes(); },[]);

    const logout_user = () => { logout();};
    
    const {note_title} = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value }); 
      
    const get_notes = async () => {
      try {
          const token = localStorage.getItem('token'); 
          const config = {
              headers: {
                  'Authorization': `token ${token}` 
              }
          };
          const response = await axios.get(`${process.env.REACT_APP_API_URL}/call_api/get_all_note/`, config);
          const data = response.data;
          setNotes(data);
          console.log('data', data);
      } catch (error) {
          console.error('Lỗi khi lấy dữ liệu từ API:', error);
      }
    };

    const add_note = async ()=> 
    {
      try {
        if (note_title.trim() === '') {
          return;}
        const token = localStorage.getItem('token'); 
        const config = {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `token ${token}` ,
              'Accept': 'application/json',
            }};
        const body = JSON.stringify(formData); 
        console.log(body)
        await axios.post(`${process.env.REACT_APP_API_URL}/call_api/add_note/`, body, config);
        get_notes();
        setAddingNote(false);
        setFormData({note_title:''});
    } catch (error){
      console.error('Lỗi khi add dữ liệu API về server:', error);
    }
    };

    const handleAddNoteClick = () => {
      setAddingNote(true);
      };
    return(
    <div>
      <div className="notes">
        <div className="notes-header">
            <h2 className="notes-title">&#9782; Notes</h2>
            <p className="notes-count">{notes.length}</p>
        </div>
        <div className='notes-list'>
            {notes.map((note, index) => (
                <h3>{note.note_title}</h3>  
            ))}
            {addingNote ? (
            <div>
                <input
                type='text'
                placeholder='Enter Note Title'
                name='note_title'
                value={note_title}
                onChange={e => onChange(e)}
                />
                <button onClick={add_note}>Submit</button>
            </div>
        ) : null}
        </div> 
        <button onClick={handleAddNoteClick}>
          <Link className="floating-button">
              <AddIcon />
          </Link> 
        </button>    
      </div>                
    </div>        
  )
}


const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout }) (NoteList);
