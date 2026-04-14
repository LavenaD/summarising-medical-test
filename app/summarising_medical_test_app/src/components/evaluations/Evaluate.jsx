import React from 'react'
import axios from 'axios'
import {useState} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSpinner} from '@fortawesome/free-solid-svg-icons'

function Evaluate() {
    const [errors, setErrors] = React.useState({})
    const [success, setSuccess] = React.useState(false)
    const [loading, setLoading] = React.useState(false)
    const handleSubmit = async(e) => {
        e.preventDefault()
        console.log('Evaluating model performance on test dataset...')
        const baseURL = import.meta.env.VITE_BACKEND_BASE_API
        setLoading(true)
        try {
            const response =  await axios.get(`${baseURL}evaluate/`)
            // Here you would implement the logic to evaluate the model's performance on a test dataset
            // For demonstration purposes, we'll just simulate a successful evaluation
            console.log('Model evaluation response:', response.data)
            setSuccess(true)
            setErrors({})
        } catch (error) {
            console.error('Error occurred while evaluating model:', error)
            setErrors({ evaluation: 'Failed to evaluate model.' })
        }finally {
            setLoading(false)
        }
    }
  return (
    <>
        <div className='container'>
            <div className='row justify-content-center' >
                <div className='col-md-6 bg-light-dark p-5 mt-5 rounded'>
                    <h3 className='text-light text-center'>Evaluate Model</h3>
                    <p className='text-light text-center'>This page will be used to evaluate the model's performance on a test dataset.</p>
                <form onSubmit={handleSubmit}>
                    <button type='submit' className='btn btn-info d-block mx-auto'>Evaluate</button>
                    {success && <div className='alert alert-success mt-3'>Model evaluated successfully!</div>}
                    {errors.evaluation && <div className='alert alert-danger mt-3'>{errors.evaluation}</div>}
                    {loading && <div className='alert alert-info mt-3'>Evaluating model, please wait...</div>}
                </form>
                </div>
            </div>

        </div>

    </>
  )
}

export default Evaluate