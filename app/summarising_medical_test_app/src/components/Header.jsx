import React from 'react'
import Button from './Button'
import { Link } from 'react-router-dom'
import { useContext } from 'react'
import AuthContext from '../AuthProvider'

const Header = () => {
  const {isLoggedIn, setIsLoggedIn } = useContext(AuthContext)
  const handleLogout = () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    setIsLoggedIn(false)
  }

  return (
    <>
        <nav className='navbar container pt-3 pb-3'>
        <Link className='navbar-brand text-light' to="/">Summarising Medical Tests</Link>

        <div>
            {isLoggedIn ? (
              <>      
              <Button text="Dashboard" class="btn btn-info" url="/dashboard" />
                &nbsp;
                <button className='btn btn-danger' onClick={handleLogout}>
                    Logout
                </button>
              </>
            ) : (
                <>
                    <Button text="Login" class="btn-outline-info" url="/login"/>
                    &nbsp;
                    <Button text="Register" class="btn-info" url = "/register"/>
                </>
            )}
        </div>
        </nav>
    </>


  )
}

export default Header