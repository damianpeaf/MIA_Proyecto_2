import { useContext, useRef, useState } from "react"
import { readFiles } from "../../utils";
import { AuthContext } from "../../context";
import toast from 'react-hot-toast';
import fetchCommand from "../../api/projectAPI";

export interface ConsoleOutputI {
    command: string;
    response?: ConsoleOutputResponse[];
}

export interface ConsoleOutputResponse {
    text: string;
    type: 'warning' | 'error' | 'success' | 'info';
    'io_type'?: 'input' | 'output';
    'date'?: '2021-10-10 10:10:10';
}

const initialConsoleOutput: ConsoleOutputI[] = [
    {
        'command': 'create -name->prueba1.txt -path->/carpeta1/ -body->”Este es el contenido del archivo 1” -type->server',
        'response': [
            { 'text': 'This is a test info message', 'type': 'info', },
            { 'text': 'This is a test info message', 'type': 'warning', },
            { 'text': 'This is a test info message', 'type': 'error', },
            { 'text': 'This is a test info message', 'type': 'success', }]
    },
    {
        'command': 'delete -path->/carpeta1/ -name->prueba1.txt -type->server',
        'response': [{ 'text': 'This is a test info message', 'type': 'warning', }]
    },
    {
        'command': 'Copy -from->/carpeta1/prueba1.txt -to->/”carpeta 2”/ -type_to->sever -type_from->bucket',
        'response': [{ 'text': 'This is a test info message', 'type': 'error', }]
    },
    {
        'command': 'Backup -type_to->server -type_from->bucket -name->”copia_1 G7”',
        'response': [{ 'text': 'This is a test info message', 'type': 'success', }]
    }
]

export const useDashboard = () => {

    // This state will be used to store the console output from the backend, use an array of objects

    const [consoleOutput, setConsoleOutput] = useState<ConsoleOutputI[]>(initialConsoleOutput)
    const [contentFromFile, setContentFromFile] = useState<string[]>([])

    const { setIsAuthorized } = useContext(AuthContext)
    const fileInputRef = useRef<HTMLInputElement>(null);


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

            const response = await fetchCommand([command])
            console.log(response)

            // Concat new line if there is already text
            setConsoleOutput(prev => prev.concat({
                'command': command,
                'response': [{ 'text': 'This is a test info message', 'type': 'info', }]
            }))

            // Clear input
            e.currentTarget.value = ''

        }
    }

    const handleLogout = () => {
        setIsAuthorized(false)
        toast.success('Sesión cerrada correctamente')
    }

    const handleExecuteCommand = async () => {

        const response = await fetchCommand(contentFromFile)
        console.log(response)

        if (fileInputRef.current) {
            fileInputRef.current.value = ''
        }
    }

    return {
        consoleOutput,
        fileInputRef,
        handleExecuteCommand,
        handleFileChange,
        handleKeyDown,
        handleLogout
    }
}