import { useState, useEffect} from 'react'
import {getUsers, getRankings} from './api.js'
import './App.css'

function App() {

  const [users, setUsers] = useState([])
  const [currentUserId, setCurrentUserId] = useState(1)
  const [rankings, setRankings] = useState([])

  useEffect(() => {
    getUsers().then(setUsers)
  },[])

  useEffect(() => {
    getRankings(currentUserId).then(setRankings)
  },[currentUserId])

  return (
    <>
      <h1>Beli Clone</h1>
      <p>{users.length} users</p>
      <select
        value = {currentUserId}
        onChange = {(event) => setCurrentUserId(Number(event.target.value))}
      >
        {
          users.map((user) => {
            return <option key = {user.id} value = {user.id}>{user['display_name']}</option>
          })
        }
      </select>
      <p>Current user id: {currentUserId}</p>
      <p>Rankings for user:</p>
      <ul>
        {
          rankings.map((ranking) => {
            return <li key = {ranking.restaurant_id}>{ranking.rank_position}. {ranking.name} ({ranking.score})</li>
          })
        }
      </ul>
    </>
  )
}

export default App
