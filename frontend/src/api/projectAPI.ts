// import { ConsoleOutputResponse } from "../hooks";

const baseUrl = 'http://127.0.0.1:8000/command';

// Fetch data from API

const fetchCommand = async (commands: string) => {
    const response = await fetch(baseUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "command": commands
        })
    })
    const data = await response.json()
    return data
}

export default fetchCommand