import React from 'react'
import Button from './Button'

const Main = () => {
    
    return (
    <>
            <div className='container'>
            <div className='p-5 text-center bg-light-dark rounded-3 mt-5 align-items-start' >
            <h1 className='mb-3 text-light'>Summarising Medical Tests</h1>
                <p className='mb-3 text-light lead'>This is a web application that summarises medical tests.</p>
                <Button text="Explore Now" class="btn-outline-warning" url="/dashboard"/>
            </div>
        </div>
    
    </>

    )
    

}

export default Main