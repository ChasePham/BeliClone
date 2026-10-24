import { useState, useEffect} from 'react'
import {getUsers, getRankings} from './api.js'
import RankingsList from './components/RankingsList.jsx'
import UserSwitcher from './components/UserSwitcher.jsx'
import RestaurantsList from './components/RestaurantsList.jsx'
import Comparison from './components/Comparison.jsx'
import './App.css'

function App() {

  const [users, setUsers] = useState([])
  const [currentUserId, setCurrentUserId] = useState(1)
  const [rankings, setRankings] = useState([])
  // The restaurant being placed in the list right now, or null when not comparing.
  const [selectedRestaurant, setSelectedRestaurant] = useState(null)

  let addComparison = null
  useEffect(() => {
    getUsers().then(setUsers)
  },[])

  useEffect(() => {
    getRankings(currentUserId).then(setRankings)
  },[currentUserId])


  function handleUserChange(userId) {
    setSelectedRestaurant(null)
    setCurrentUserId(userId)
  }

  function handleComparisonDone() {
    setSelectedRestaurant(null)
    getRankings(currentUserId).then(setRankings)
  }

  if (selectedRestaurant !== null) {
    // key makes React start a fresh Comparison (new lo/hi) for each restaurant.
    addComparison = <Comparison
      key = {selectedRestaurant.id}
      userId = {currentUserId}
      restaurant = {selectedRestaurant}
      currRankings = {rankings}
      onDone = {handleComparisonDone}
    />
  }

  return (
    <>
      <h1>Beli Clone</h1>
      <p>{users.length} users</p>
      <UserSwitcher
        users = {users}
        currentUserId = {currentUserId}
        onChange = {handleUserChange}
      />
      <p>Current user id: {currentUserId}</p>
      <p>Rankings for user:</p>
      <RankingsList rankings = {rankings} />
      <RestaurantsList addRestaurant={setSelectedRestaurant} currUser={currentUserId}></RestaurantsList>
      {addComparison}
    </>
  )
}

export default App
