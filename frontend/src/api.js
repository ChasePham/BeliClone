

//Function to get all users
export async function getUsers() {
    const response = await fetch("/api/users")
    const data = await response.json()
    return data
}

export async function getRankings(userId) {
    const response = await fetch(`/api/users/${userId}/rankings`)
    const data = await response.json()
    return data
}

export async function searchRestaurants(search) {
    const response = await fetch(`/api/restaurants?q=${encodeURIComponent(search)}`)
    const data = await response.json()
    return data
}

export async function addRanking(userId, restaurantId, rankPosition) {
    const body = {
        restaurant_id: restaurantId,
        rank_position: rankPosition
    }
    const response = await fetch(`/api/users/${userId}/rankings`, {
        method: 'POST',
        headers: {
            'Content-type':'application/json'
        },
        body: JSON.stringify(body)
    })
    const result = await response.json()
    return result
}