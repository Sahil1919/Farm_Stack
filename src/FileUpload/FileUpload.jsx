import React from 'react'
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import { faPlus } from '@// import axios from 'axios'
import { useState } from 'react'
function FileUpload () {
    const [files,setFile] = useState([])

    const handlefileinput = (event ) => {
        // console.log(event.target.files[0].name)
        setFile(Array.from(event.target.files))
        
    }
    const handleSubmit = async (event) =>{
        event.preventDefault()

        const formData = new FormData()

        files.forEach( file =>{
            formData.append('file_upload',file)
            console.log(file)
        })

        try{
            const endpoint = "http://localhost:8000/uploadfile/"
            const response = await fetch (endpoint,{
                method:"POST",
                body: formData
            })

            if (response.ok){
                console.log("File is Uploaded")
            }
            else{
                console.log("File is not Uploaded")
            }
        }catch (error){
            console.log(error)
        }
    }
    return (
        <>
            <div>
                <h1> Upload File</h1>
                <form onSubmit={handleSubmit}>
                    <div style={{marginBottom:"20px"}}>
                        <input type="file" webkitdirectory="" onChange={handlefileinput} multiple  />
                    <button type='submit'>Upload</button>
                    </div>
                </form>
                { files &&  files.forEach(file =>{ <p style={{alignItems:'center'}}>{file.name} </p>})}
            </div>
        </>
    )
}

export default FileUpload
