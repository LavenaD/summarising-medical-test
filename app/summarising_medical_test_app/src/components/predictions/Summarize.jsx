import React from 'react'
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
    const handleSummarize = async (e) => {
        e.preventDefault()
        setLoading(true)
        try {
            const response = await axiosInstance.post(`summarize/`, formData)
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
                    {errors.summarize && <div className='alert alert-danger mt-3'>{errors.summarize}</div>}
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