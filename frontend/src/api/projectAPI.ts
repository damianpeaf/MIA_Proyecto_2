import { ConsoleOutputResponse } from "../hooks";

const baseUrl = 'http://100.26.201.62/health';

// Fetch data from API

const fetchCommand = async (command: string[]) => {
    const response = await fetch(baseUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(command)
    })
    const data: ConsoleOutputResponse[] = await response.json()
    return data
}

export default fetchCommand