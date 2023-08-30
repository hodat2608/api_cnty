import React from 'react'
import { ReactComponent as AddIcon } from '../assets/add.svg'
import { Link } from 'react-router-dom';

const Add_note = () => {
  return (
    <Link  to = {'/all_note/'} className='floating-button'>
        <AddIcon />
    </Link>
  )
}

export default Add_note;
