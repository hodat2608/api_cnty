import React, { useState, useEffect } from 'react';
import ListItem from '../components/list_item';

const NoteList = () => {
    
    const [notes, setNotes] = useState([]);
    
    useEffect(() => { 
        getNotes(); 
    }, []);
       
    const getNotes = async () => {
        const response = await fetch('/call_api/All_Note/');
        const data = await response.json();
        setNotes(data);
        console.log('data:',data)
    }
    return (
        <div>
            <div className="notes">
                <div className="notes-header">
                    <h2 className="notes-title">&#9782; Notes</h2>
                    <p className="notes-count">{notes.length}</p>
                </div>
                <div className='notes-list'>
                    {notes.map((note, index) => 
                        <ListItem key={index} note={note} />
                    )}
                </div>
            </div>
        </div>
    )
}

export default NoteList;
