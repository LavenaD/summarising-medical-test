// import { useState } from 'react'
import './assets/css/style.css'
import Header from './components/Header'
import Main from './components/Main'
import Footer from './components/Footer'
import Register from './components/Register'
import Login from './components/Login'
import Dashboard from './components/dashboard/Dashboard'
import ProcessFiles from './components/processFiles/ProcessFiles'
import Summarize from './components/predictions/Summarize'
import Evaluate from './components/evaluations/Evaluate'
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './AuthProvider'
import PrivateRoute from './PrivateRoute'
import PublicRoute from './PublicRoute'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
    <AuthProvider>  
      <BrowserRouter>
      <Header/>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
          <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/process-files" element={<PrivateRoute><ProcessFiles /></PrivateRoute>} />
          <Route path="/summarize" element={<PrivateRoute><Summarize /></PrivateRoute>} />
          <Route path="/evaluate" element={<PrivateRoute><Evaluate /></PrivateRoute>} />
        </Routes>
        <Footer/>
      </BrowserRouter>
    </AuthProvider>
    </>
  )
}

export default App
