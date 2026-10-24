import { useState } from 'react'
import {searchRestaurants} from '../api.js'


function RestaurantsList({addRestaurant}) {
    const [restaurants, setRestaurants] = useState([])
    const [search, setSearch] = useState("")

    // Runs when the user presses Enter or clicks the button.
    function handleSubmit(event) {
        event.preventDefault()  // stop the browser from reloading the page
        searchRestaurants(search).then(setRestaurants)
    }
    function handleClick(restaurant) {
        console.log("user selected restaurant for ranking:", restaurant)
        addRestaurant(restaurant)
    }

    // Build one <li> per restaurant; React renders the whole array below.
    const items = []
    for (const restaurant of restaurants) {
        items.push(
        <li key = {restaurant.id}>
            {restaurant.name} ({restaurant.cuisine}, {restaurant.city})
            <button onClick= {() => {handleClick(restaurant)}}>Add</button>
            
        </li>)
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
