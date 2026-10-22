

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