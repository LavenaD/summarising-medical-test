import React, { useEffect } from 'react'
import axiosInstance from '../../axiosInstance'

const baseURL = import.meta.env.VITE_BACKEND_BASE_API

const Dashboard = () => {
    useEffect(() => {
        const fetchProtectedData = async () => {
        try{
            console.log(`${baseURL}/protected-view/`)
            const response = await axiosInstance.get(`${baseURL}protected-view/`);
            console.log('Protected data:', response.data);

        }catch(error){
            console.error('Error fetching protected data:', error)
        }
        }
        fetchProtectedData();
        }, [])
  return (
    <div className="text-light container">Dashboard</div>
  )
}

export default Dashboard