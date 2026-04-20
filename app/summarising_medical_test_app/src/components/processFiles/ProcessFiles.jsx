import React, {useState} from 'react'
import axiosInstance from '../../axiosInstance'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSpinner} from '@fortawesome/free-solid-svg-icons'

function ProcessFiles() {
    const [formData, setFormData] = React.useState({
        input_folder_path: '',
        max_rows_per_outputfile: ''
    })
    const [errors, setErrors] = useState({})
    const [success, setSuccess] = useState(false)
    const [loading, setLoading] = useState(false)
    const [responseMessage, setResponseMessage] = useState('')
    const baseURL = import.meta.env.VITE_BACKEND_BASE_API

    const handleProcessFile = async (e) => {
        e.preventDefault()
        // Get the input folder path and max rows from the form
        console.log('formData:', formData)
        setLoading(true)
        // Make an API call to the backend to process the files
        try{
            const response = await axiosInstance.post(`${baseURL}medical_records/process/`, formData)
            console.log(response.data)
            console.log('Files processed successfully:', response.data)
            setErrors({})
            setSuccess(true)
            setLoading(false)
            setResponseMessage(response.data.message)
        }catch(error){
            console.error('Error processing files:', error)
            setErrors(error.response.data)
            setSuccess(false)
            setLoading(false)
        }
    }

  return (
    <>
    <div className='container'>
        <div className='row justify-content-center' >
            <div className='col-md-6 bg-light-dark p-5 mt-5 rounded'>
                <h3 className='text-light text-center'>Processing Files</h3>
                <form onSubmit={handleProcessFile}>
                    <div className='mb-3'>
                        <input type='text' className='form-control' placeholder='Enter input folder path like data//ecgen-radiology//train' value={formData.input_folder_path} 
                        onChange={(e) => setFormData({...formData, input_folder_path: e.target.value})} />
                    </div>
                    <div className='mb-3'>
                        <input type='number' className='form-control' placeholder='Enter maximum number of rows to write in the output file' value={formData.max_rows_per_outputfile}
                        onChange={(e) => setFormData({...formData, max_rows_per_outputfile: e.target.value})} />
                    </div>

                    {success && <div className='alert alert-success mt-3'>Files processed successfully- {responseMessage}!</div>}
                    {errors.error && <div className='alert alert-danger mt-3'>{errors.error}</div>}
                    {responseMessage && <div className='alert alert-info mt-3'>{responseMessage}</div>}
                    {loading ? (<button className='btn btn-info d-block mx-auto' disabled><FontAwesomeIcon icon={faSpinner} spin /> Please wait...</button> )
                                                    : ( <button type='submit' className='btn btn-info d-block mx-auto'>Process</button>)}
                </form>

            </div>
        </div>
    </div>
    </>
  )
}

export default ProcessFiles