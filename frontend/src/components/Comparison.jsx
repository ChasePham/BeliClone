import { useState } from 'react'
import { addRanking } from '../api.js'

// Places a new restaurant in the user's ranked list with a binary search.
// lo/hi bound the index where it belongs; each answer cuts that range in half.
function Comparison({ userId, restaurant, currRankings, onDone }) {
    const [lo, setLo] = useState(0)
    const [hi, setHi] = useState(currRankings.length)

    if (lo === hi) {
        const position = lo + 1
        return (<>
            <p>{restaurant.name} goes at #{position}.</p>
            <button onClick = {() => addRanking(userId, restaurant.id, position).then(onDone)}>Save</button>
        </>)
    }

    const mid = Math.floor((lo + hi) / 2)
    const existing = currRankings[mid]

    return (<>
        <p>Which did you prefer?</p>
        <button onClick = {() => setHi(mid)}>{restaurant.name}</button>
        <button onClick = {() => setLo(mid + 1)}>{existing.name}</button>
    </>)
}

export default Comparison
