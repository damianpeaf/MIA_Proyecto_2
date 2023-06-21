const baseUrl = import.meta.env.VITE_API_BASE_URL;

// Fetch data from API

const fetchCommand = async (command: string) => {
    const url = `${baseUrl}/command`
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "command": command
        })
    })
    const data = await response.json()
    return data
}

export default fetchCommand