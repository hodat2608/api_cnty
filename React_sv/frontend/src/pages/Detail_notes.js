import React from 'react'
import { useState,useEffect } from 'react'
import { useParams,useNavigate } from 'react-router-dom'
import { Link  } from 'react-router-dom';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'
import NoteList from './List_note';
 

const Detail_notes = () => {
    let {id} = useParams(); 
    let[item , SetItem] = useState([])
    let navigate = useNavigate();

    useEffect(()=>{detail_note()},[id])

    let detail_note = async() => {
        let response = await fetch(`/call_api/Action/${id}/`)
        let data = await response.json()
        SetItem(data)
        console.log('data:',data)
    }

    let updateNote = async () => {
        fetch(`/call_api/Action/${id}/`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(item)  
        })
    }

    let detele_note = async =>{
        fetch(`/call_api/Action/${id}/`,{
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(item)  
        })
    }

    let handleSubmit = () => {
        updateNote()
        navigate('/all_note/')
    }
    let compound = () => {
        detele_note()
        // navigate('/all_note/')
        NoteList()
    }
    
    let handleChange = (value) => {
        SetItem(item => ({ ...item, 'note_conntent': value }))
        console.log('Handle Change:', item)
    }

    let getTime = (item) => {
        return new Date(item.updated).toLocaleDateString()
      }
      
    return (
        <div className='note'>
            <div className='note-header'>
                <ArrowLeft onClick ={handleSubmit}/>
            </div>
            <Link onClick={compound}>Delete</Link>
            <textarea onChange={(e) => { handleChange(e.target.value) }} value={item?.note_conntent}></textarea>
            <div className='date'>
                <p>Created :{item?.created}</p>
                <p>Last updated :<span>{getTime(item)}</span></p>
            </div>
        </div>
    );
}

export default Detail_notes
