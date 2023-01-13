import React, { useState, useEffect } from 'react'
// import axios from 'axios'
import publicAxios from '../utils/public-axios';

const TemporaryPage = () => {
  const [data, setData] = useState({ loading: true })

  useEffect(() => {
    async function fetchData() {
    //   const response = await axios.get('http://127.0.0.1:8000/auth/registered_user')
        const response = await publicAxios.get(`/auth/registered_user`);
        setData(response.data)
        console.log(response.data)
    }
    fetchData()
  }, [])

  return (
    <div>
      { data.loading ? 'Loading...' : JSON.stringify(data) }
    </div>
  )
}

export default TemporaryPage
