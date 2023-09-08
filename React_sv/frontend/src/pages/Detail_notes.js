import React from 'react'
import { useState,useEffect } from 'react'
import { useParams,useNavigate } from 'react-router-dom'
import { Link  } from 'react-router-dom';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'


const Detail_notes = ({getNotes}) => {
    let {id} = useParams(); 
    let[item , SetItem] = useState([])
    let navigate = useNavigate();

    useEffect(()=>{detail_note()},[id])

    let detail_note = async() => {
        let response = await fetch(`http://127.0.0.1:2806/call_api/Action/${id}/`)
        let data = await response.json()
        SetItem(data)
        console.log('data:',data)
    }

    let updateNote = async () => {
        fetch(`http://127.0.0.1:2806/call_api/Action/${id}/`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(item)  
        })
    }

    let detele_note = async () =>{
        fetch(`http://127.0.0.1:2806/call_api/Action/${id}/`,{
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(item)  
        })
        // navigate('/all_note/')
        getNotes();
    }

    let handleSubmit = () => {
        updateNote()
        navigate('/all_note/')
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
            <button onClick={detele_note}>DELETE</button>
            <textarea onChange={(e) => {handleChange(e.target.value)}} value={item?.note_conntent}></textarea>
            <div className='date'>
                <p>Created :{item?.created}</p>
                <p>Last updated :<span>{getTime(item)}</span></p>
            </div>
        </div>
    );
}

export default Detail_notes
