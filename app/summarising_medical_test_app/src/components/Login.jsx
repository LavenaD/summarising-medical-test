import React, {useState} from 'react'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faSpinner} from '@fortawesome/free-solid-svg-icons'
import { useNavigate } from 'react-router-dom'
import { useContext } from 'react'
import AuthContext from '../AuthProvider'

const Login = () => {
     const [formData, setFormData] = useState({
        username: '',
        password: ''
    })
    const [loading, setLoading] = useState(false)
    const [errors, setErrors] = useState({})
    const { setIsLoggedIn } = useContext(AuthContext)
    const navigate = useNavigate()
    const baseURL = import.meta.env.VITE_BACKEND_BASE_API
    

    const handleLogin = async (e) => {
                    e.preventDefault()
                    setLoading(true)
    
        try{
            const response = await axios.post(`${baseURL}token/`, formData)
            console.log('User logged in successfully')
            localStorage.setItem('accessToken', response.data.access)
            localStorage.setItem('refreshToken', response.data.refresh)
            setFormData({
                username: '',
                password: ''
            })
            setErrors({})
            setIsLoggedIn(true)
            navigate('/dashboard')

        } catch (error) {
            setErrors(error.response.data)
            console.error('Error logging in user:', error)
        }finally{
            setLoading(false)
        }
    } 
  return (
    <>
       <div className='container'>
        <div className='row justify-content-center'>
            <div className='col-md-6 bg-light-dark p-5 mt-5 rounded'>
                <h3 className='text-light text-center'>Login to our portal</h3>
                <form onSubmit={handleLogin}>
                    <div className='mb-3'>
                        <input type="text" className='form-control' placeholder='Username' value = {formData.username} onChange={(e) => setFormData({...formData, username: e.target.value})} />
                    </div>
                    <div className='mb-3'>
                        <input type="password" className='form-control' placeholder='Password' value = {formData.password} onChange={(e) => setFormData({...formData, password: e.target.value})} />
                    </div>
                    <div>
                          {errors.detail && <div className='alert alert-danger'>{errors.detail}</div>}
                        {loading ? (<button className='btn btn-info d-block mx-auto' disabled><FontAwesomeIcon icon={faSpinner} spin /> Logging in...</button> )
                                : ( <button type='submit' className='btn btn-info d-block mx-auto'>Login</button>)}
                    </div>
                </form>
            </div>
        </div>
    </div>
    </>
  )
}

export default Login