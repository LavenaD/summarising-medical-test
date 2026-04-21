import axios from 'axios'

// create axiosinstance with baseURL and default headers
const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_BASE_API,
    headers: {
        'Content-Type': 'application/json',
    }
})


axiosInstance.interceptors.request.use(
    function(config){
        const accessToken = localStorage.getItem('accessToken')
        if(accessToken){
            config.headers['Authorization'] = `Bearer ${accessToken}`
        }   
        return config
    },
    function(error){
        return Promise.reject(error)
    }
)

axiosInstance.interceptors.response.use(
    function(response){
        return response 
    },
    async function(error){
        const originalRequest = error.config    
        if(error.response.status === 401 && !originalRequest._retry){
            originalRequest._retry = true
            try{
                const refreshToken = localStorage.getItem('refreshToken')
                const response = await axiosInstance.post('token/refresh/', { refresh: refreshToken })
                const newAccessToken = response.data.access
                localStorage.setItem('accessToken', newAccessToken)
                originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`
                return axiosInstance(originalRequest)
            }catch(refreshError){
                console.error('Error refreshing token:', refreshError)
                localStorage.removeItem('accessToken')
                localStorage.removeItem('refreshToken')
                window.location.href = '/login'
                return Promise.reject(refreshError)
            }
        }
        return Promise.reject(error)
    })   


export default axiosInstance