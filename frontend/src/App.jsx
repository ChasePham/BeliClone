import { useState, useEffect} from 'react'
import {getUsers, getRankings} from './api.js'
import RankingsList from './components/RankingsList.jsx'
import UserSwitcher from './components/UserSwitcher.jsx'
import RestaurantsList from './components/RestaurantsList.jsx'
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
      <UserSwitcher
        users = {users}
        currentUserId = {currentUserId}
        onChange = {setCurrentUserId}
      />
      <p>Current user id: {currentUserId}</p>
      <p>Rankings for user:</p>
      <RankingsList rankings = {rankings} />
      <RestaurantsList></RestaurantsList>
    </>
  )
}

export default App
