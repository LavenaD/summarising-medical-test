import React, {useState} from 'react'
import axiosInstance from '../../axiosInstance'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSpinner} from '@fortawesome/free-solid-svg-icons'

const Summarize = () => {
    const [errors, setErrors] = React.useState({})
    const [success, setSuccess] = React.useState(false)
    const [loading, setLoading] = React.useState(false)
    const [summary, setSummary] = React.useState(null)
    const [formData, setFormData] = React.useState({
        findings: ''
    })
    const baseURL = import.meta.env.VITE_BACKEND_BASE_API
    const handleSummarize = async (e) => {
        e.preventDefault()
        console.log('formData:', formData)
        setLoading(true)
        try {
            const response = await axiosInstance.post(`${baseURL}summarize/`, formData)
            console.log('Summary:', response.data)
            setSummary(response.data.summary)
            setSuccess(true)
            setErrors({})
        } catch (error) {
            console.error('Error summarizing findings:', error)
            setErrors({ summarize: 'Failed to summarize findings.' })
        } finally {
            setLoading(false)
        }
    }


  return (
    <>
      <div className='container'>
        <div className='row justify-content-center' >
            <div className='col-md-6 bg-light-dark p-5 mt-5 rounded'>
                <h3 className='text-light text-center'>Summarize Findings</h3>
                <p className='text-light text-center'>Enter your findings to summarize them.</p>
                <form onSubmit={handleSummarize}>
                    <div className='mb-3'>
                        <textarea className='form-control' placeholder='Enter findings here...' rows={10} value={formData.findings}
                            onChange={(e) => setFormData({...formData, findings: e.target.value})}></textarea>
                    </div>
                    {success && <div className='alert alert-success mt-3'>Findings summarized successfully!</div>
                    && <div className='alert alert-info mt-3'>Summary: {summary}</div>}
                    {loading ? (<button className='btn btn-info d-block mx-auto' disabled><FontAwesomeIcon icon={faSpinner} spin /> Please wait...</button> )
                        : ( <button className='btn btn-info d-block mx-auto'>Summarize</button>)}
                </form>
            </div>
        </div>
      </div>
    </>
  )
}

export default Summarize