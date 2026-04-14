import React, {useState} from 'react'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSpinner} from '@fortawesome/free-solid-svg-icons'

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    })
    const [errors, setErrors] = useState({})
    const [success, setSuccess] = useState(false)
    const [loading, setLoading] = useState(false)

    const handleRegistration = async (e) => {
                    e.preventDefault()
                    console.log(formData)
                    setLoading(true)
    
        try{
            const response = await axios.post('http://127.0.0.1:8000/api/v1/register/', formData)
            console.log(response.data)
            console.log('User registered successfully')
            setErrors({})
            setSuccess(true)
        } catch (error) {
            setErrors(error.response.data)
            setSuccess(false)
            console.error('Error registering user:', error)
        }finally{
            setLoading(false)
        }
    }
    return (
    <>
    <div className='container'>
        <div className='row justify-content-center'>
            <div className='col-md-6 bg-light-dark p-5 mt-5 rounded'>
                <h3 className='text-light text-center'>Create an Account</h3>
                <form onSubmit={handleRegistration}>
                    <div className='mb-3'>
                        <input type="text" className='form-control' placeholder='Username' value = {formData.username} onChange={(e) => setFormData({...formData, username: e.target.value})} />
                        {errors.username && <small className='text-danger'>{errors.username}</small>}
                    </div>
                    <div className='mb-3'>
                        <input type="email" className='form-control' placeholder='Email' value = {formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} />
                        {errors.email && <small className='text-danger'>{errors.email}</small>}
                    </div>
                    <div className='mb-3'>
                        <input type="password" className='form-control' placeholder='Password' value = {formData.password} onChange={(e) => setFormData({...formData, password: e.target.value})} />
                        {errors.password && <small className='text-danger'>{errors.password}</small>}   
                    </div>
                    <div className='mb-3'>
                        <input type="password" className='form-control' placeholder='Confirm Password' value = {formData.confirmPassword} onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})} />
                        
                    </div>
                    <div>
                        {success && <div className='alert alert-success'>User registered successfully!</div>}
                        {loading ? (<button className='btn btn-info d-block mx-auto' disabled><FontAwesomeIcon icon={faSpinner} spin /> Please wait...</button> )
                                : ( <button type='submit' className='btn btn-info d-block mx-auto'>Register</button>)}
                    </div>
                </form>
            </div>
        </div>
    </div>

    </>
    
  )
}

export default Register