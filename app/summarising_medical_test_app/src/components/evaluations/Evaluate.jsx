import React, { useEffect, useRef, useState }  from 'react'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSpinner} from '@fortawesome/free-solid-svg-icons'

function Evaluate() {
    const [errors, setErrors] = React.useState({})
    const [success, setSuccess] = React.useState(false)
    const [loading, setLoading] = React.useState(false)

    const [jobId, setJobId] = useState(null)
    const [progress, setProgress] = useState(0)
    const [status, setStatus] = useState('')
    const [results, setResults] = useState(null)

    const [responseMessage, setResponseMessage] = useState('')

    const [formData, setFormData] = React.useState({
        input_file_name: ''
    })

    const pollIntervalRef = useRef(null)
    const baseURL = import.meta.env.VITE_BACKEND_BASE_API

    const stopPolling = () => {
        if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current)
        pollIntervalRef.current = null
        }
    }

    const fetchStatus = async (currentJobId) => {
        try {
        const response = await axios.get(
            `${baseURL}evaluate/get_status/${currentJobId}/`
        )

        const data = response.data

        setStatus(data.status || 'Processing...')
        setProgress(data.progress ?? 0)

        if (data.results) {
            setResults(data.results)
        }

        const isCompleted =
            (data.progress ?? 0) >= 100 ||
            (data.status && data.status.toLowerCase().includes('completed'))

        if (isCompleted) {
            setSuccess(true)
            setLoading(false)
            stopPolling()
        }
        } catch (error) {
        console.error('Error fetching evaluation status:', error)
        setErrors({ evaluation: 'Failed to fetch evaluation status.' })
        setLoading(false)
        stopPolling()
        }
    }    

    const handleSubmit = async(e) => {
        e.preventDefault()
        console.log('Evaluating model performance on test dataset...')
        const baseURL = import.meta.env.VITE_BACKEND_BASE_API
        setLoading(true)
        setSuccess(false)
        setErrors({})
        setProgress(0)
        setStatus('Starting evaluation...')
        setResults(null)
        stopPolling()
        try {
            console.log(`${baseURL}evaluate/`)
            const response =  await axios.post(`${baseURL}evaluate/`, formData)
            // Here you would implement the logic to evaluate the model's performance on a test dataset
            const newJobId = response.data.job_id

            if (!newJobId) {
                throw new Error('job_id not returned from evaluate endpoint' + JSON.stringify(response.data))
            }

            setJobId(newJobId)

            // Fetch immediately once
            await fetchStatus(newJobId)

            // Then poll every 60 seconds
            pollIntervalRef.current = setInterval(() => {
                fetchStatus(newJobId)
            }, 10000)
            console.log('Model evaluation response:', response.data)

        } catch (error) {
            console.error('Error occurred while evaluating model:', error)
            setErrors({ evaluation: 'Failed to evaluate model.' + error.message })
            setResponseMessage('Failed to evaluate model. Please try again later.')
            setLoading(false)
            stopPolling()
        }finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        return () => {
        stopPolling()
        }
    }, [])

  return (
    <>
        <div className='container'>
            <div className='row justify-content-center' >
                <div className='col-md-6 bg-light-dark p-5 mt-5 rounded'>
                    <h3 className='text-light text-center'>Evaluate Model</h3>
                    <p className='text-light text-center'>This page will be used to evaluate the model&apos;s performance on a test dataset.</p>
                <form onSubmit={handleSubmit}>
                    <div className='mb-3'>
                        <input type='text' className='form-control' placeholder='Enter input file name like test_data.csv' value={formData.input_file_name} 
                        onChange={(e) => setFormData({...formData, input_file_name: e.target.value})} />
                    </div>
                     {loading || progress > 0 && progress < 100 ? (
                        <>
                        <button className='btn btn-info d-block mx-auto' disabled><FontAwesomeIcon icon={faSpinner} spin /> Evaluating...</button> 
                                

                        <div className='mt-4'>
                            <div className='progress' role='progressbar' aria-valuenow={progress} aria-valuemax='100' style={{ height: '25px' }}>
                                <div className='progress-bar progress-bar-striped progress-bar-animated' style={{ width: `${progress}%` }}>
                                    {progress}%
                                </div>
                            </div>

                            <div className='text-light mt-2'>
                                <strong>Status:</strong> {status || 'Waiting for update...'}
                            </div>
                        </div>
                        </>
                        ) : ( <button type='submit' className='btn btn-info d-block mx-auto'>Evaluate</button>)}
                              
                    {errors.evaluation && <div className='alert alert-danger mt-3'>{errors}</div>}

                    {results && (
                        <div className='alert alert-success mt-3'>
                            <h5>Model evaluated successfully! - The ROUGE Scores</h5>
                            <div><small>ROUGE-1: {results.rouge1}</small></div>
                            <div><small>ROUGE-2: {results.rouge2}</small></div>
                            <div><small>ROUGE-L: {results.rougeL}</small></div>
                            <div><small>ROUGE-Lsum: {results.rougeLsum}</small></div>
                        </div>
                    )}

                    {jobId && ( <div className='text-light mt-2'><small>Job ID: {jobId}</small></div>)}
                </form>
                </div>
            </div>

        </div>

    </>
  )
}

export default Evaluate