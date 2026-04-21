import React, { useEffect } from 'react'
import axiosInstance from '../../axiosInstance'
import Button from '../Button'

const Dashboard = () => {
    useEffect(() => {
        const fetchProtectedData = async () => {
        try{
            const response = await axiosInstance.get('protected-view/');

        }catch(error){
            console.error('Error fetching protected data:', error)
        }
        }
        fetchProtectedData();
        }, [])
  return (
    <>
            <div className='container'>
                <div className='p-5 text-center bg-light-dark rounded-3 mt-5 align-items-start' >
                    <h1 className='mb-3 text-light'>Cleaning Data</h1>
                    <p className='mb-3 text-light lead'>Process and clean medical test data.
                        This will read findings, impressions and write it to the output file.</p>
                    <Button text="Process Files" class="btn-outline-warning" url="/process-files"/>
                    &nbsp;&nbsp;
                    <Button text="Summarize Findings" class="btn-outline-warning" url="/summarize"/>
                    &nbsp;&nbsp;
                    <Button text="Evaluate" class="btn-outline-warning" url="/evaluate"/>
                </div>
            </div>
    </>
    
  )
}

export default Dashboard