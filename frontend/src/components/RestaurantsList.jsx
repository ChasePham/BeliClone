import { useState } from 'react'
import {searchRestaurants} from '../api.js'

function RestaurantsList() {
    const [restaurants, setRestaurants] = useState([])
    const [search, setSearch] = useState("")

    // Runs when the user presses Enter or clicks the button.
    function handleSubmit(event) {
        event.preventDefault()  // stop the browser from reloading the page
        searchRestaurants(search).then(setRestaurants)
    }

    // Build one <li> per restaurant; React renders the whole array below.
    const items = []
    for (const restaurant of restaurants) {
        items.push(<li key = {restaurant.id}>{restaurant.name} ({restaurant.cuisine}, {restaurant.city})</li>)
    }

    return(<>
        <form onSubmit = {handleSubmit}>
            <input
                type = "text"
                placeholder = "Search restaurants"
                value = {search}
                onChange = {(event) => setSearch(event.target.value)}
            />
            <button type = "submit">Search</button>
        </form>
        <ul>{items}</ul>
    </>)
}

export default RestaurantsList
