const baseUrl = import.meta.env.VITE_API_BASE_URL
// Catch if response is ok or not

const fetchLogin = async (username: string, password: string) => {
    const url = `${baseUrl}/auth`
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({ username, password }),
        headers: {
            "Content-Type": "application/json"
        }
    })

    return response.ok
}

export default fetchLogin