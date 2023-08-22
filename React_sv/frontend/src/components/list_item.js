import React from 'react';
import { Link  } from 'react-router-dom';

const ListItem = ({ note }) => {
  return (
    <div>
      <div className="notes-list-item" >
        <Link to={`/detail_note/${note.id}/`}>
          <h3>{note.note_title}</h3>
        </Link>
      </div>
    </div>
  )
}

export default ListItem;