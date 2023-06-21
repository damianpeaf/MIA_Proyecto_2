import { useContext, useRef, useState } from "react"
import { readFiles } from "../../utils";
import { AuthContext } from "../../context";
import toast from 'react-hot-toast';
import fetchCommand from "../../api/projectAPI";

export interface ConsoleOutputI {
    command: string;
    response?: ConsoleOutputResponse;
}

export interface ConsoleOutputResponse {
    data: {
        'file_content'?: string;
    },
    output:
    {
        date: string;
        io_type: 'INPUT' | 'OUTPUT';
        message: string;
        msg_type: 'INFO' | 'ERROR' | 'WARNING' | 'SUCCESS';
    }[]
}


const initialConsoleOutput: ConsoleOutputI[] = []

export const useDashboard = () => {

    // This state will be used to store the console output from the backend, use an array of objects

    const [consoleOutput, setConsoleOutput] = useState<ConsoleOutputI[]>(initialConsoleOutput)
    const [contentFromFile, setContentFromFile] = useState<string[]>([])

    const { setIsAuthorized } = useContext(AuthContext)
    const fileInputRef = useRef<HTMLInputElement>(null);
    const textAreaRef = useRef<HTMLTextAreaElement>(null);



    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;
        readFiles(files).then((data) => {
            // Store data in state
            setContentFromFile(data[0].split('\n'))
            toast.success('Archivo cargado correctamente')
        }

        ).catch((error) => {
            toast.error('Error al cargar el archivo', error)
        }
        );

    }

    const handleKeyDown = async (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const command = e.currentTarget.value;

            if (command === '') return;

            if (command === 'clear') {
                setConsoleOutput([])
                e.currentTarget.value = ''
                return;
            }

            const response = await fetchCommand(command)
            setConsoleOutput(prev => prev.concat({
                'command': command,
                'response': response
            }))

            // Clear input
            if (textAreaRef.current) {
                textAreaRef.current.value = ''
            }

        }
    }

    const handleLogout = () => {
        setIsAuthorized(false)
        toast.success('Sesión cerrada correctamente')
    }

    const handleExecuteCommand = async () => {

        // Fetch each command from API

        contentFromFile.forEach(async (command) => {
            const response: ConsoleOutputResponse = await fetchCommand(command)
            setConsoleOutput(prev => prev.concat({
                'command': command,
                'response': response
            }))
        })

        if (fileInputRef.current) {
            fileInputRef.current.value = ''
        }
    }

    return {
        consoleOutput,
        fileInputRef,
        textAreaRef,
        handleExecuteCommand,
        handleFileChange,
        handleKeyDown,
        handleLogout
    }
}