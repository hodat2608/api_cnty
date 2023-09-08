import React, { useState, useEffect } from 'react';
import ListItem from '../components/list_item';
import Add_note from '../components/add_note'
import Detail_notes from './Detail_notes';

const NoteList = () => {
    
    const [notes, setNotes] = useState([]);
    const [addingNote, setAddingNote] = useState(false);
    const [newNoteTitle, setNewNoteTitle] = useState('');
    
    useEffect(() => { 
        getNotes(); 
    }, []);
       
    const getNotes = async () => {
        const response = await fetch('http://127.0.0.1:2806/call_api/All_Note/');
        const data = await response.json();
        setNotes(data);
        console.log('data:',data)
    }

    const add_another_note = async () => {
        try {
          const response = await fetch(`http://127.0.0.1:2806/call_api/All_Note/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ note_title: newNoteTitle })
          });
      
          if (response.ok) {
                getNotes();
          } else {
                console.error('Failed to add note');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      };
      
    const onoffadnote = () => {
    setAddingNote(true);
    };

    const handleNoteTitleChange = (e) => {
    setNewNoteTitle(e.target.value);
    };

    const handleSubmitNote = () => {
        if (newNoteTitle) {
          add_another_note();
          setAddingNote(false);
          setNewNoteTitle('');
        }
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
                            <ListItem key={index} note={note} />
                        ))}
                        {addingNote ? (
                        <div>
                            <input
                            type='text'
                            placeholder='Enter Note Title'
                            value={newNoteTitle}
                            onChange={handleNoteTitleChange}
                            />
                            <button onClick={handleSubmitNote}>Submit</button>
                        </div>
                        ) : null}
                    </div>                
            </div>
            <button onClick={onoffadnote}>
                <Add_note/>
            </button>
            <div>
              <Detail_notes getNotes={getNotes} />
            </div>
        </div>
    )
}

export default NoteList;
