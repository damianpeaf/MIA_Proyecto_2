import { createRef, useState } from "react"

export interface ConsoleOutputI {
    command: string;
    type: 'warning' | 'error' | 'success' | 'info';
    response?: string[];
}

const initialConsoleOutput: ConsoleOutputI[] = [
    {
        'command': 'create -name->prueba1.txt -path->/carpeta1/ -body->”Este es el contenido del archivo 1” -type->server',
        'type': 'info',
        'response': ['This is a test info message', 'Prueba create']
    },
    {
        'command': 'delete -path->/carpeta1/ -name->prueba1.txt -type->server',
        'type': 'warning',
        'response': ['This is a test warning message']
    },
    {
        'command': 'Copy -from->/carpeta1/prueba1.txt -to->/”carpeta 2”/ -type_to->sever -type_from->bucket',
        'type': 'error',
        'response': ['OUTPUT - La ruta no existe']
    },
    {
        'command': 'Backup -type_to->server -type_from->bucket -name->”copia_1 G7”',
        'type': 'success',
        'response': ['OUTPUT - Se ha creado el backup']
    }
]

export const useConsole = () => {

    // This state will be used to store the console output from the backend, use an array of objects
    // 
    const [consoleOutput, setConsoleOutput] = useState<ConsoleOutputI[]>(initialConsoleOutput)
    const consoleRef = createRef<HTMLDivElement>();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;
        console.log(files);
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const command = e.currentTarget.value;

            if (command === '') return;

            if (command === 'clear') {
                setConsoleOutput([])
                e.currentTarget.value = ''
                return;
            }

            // Concat new line if there is already text
            setConsoleOutput(prev => prev.concat({
                'command': command,
                'type': 'success',
                'response': ['This is a test success message']
            }))


            // Clear input
            e.currentTarget.value = ''

        }
    }

    return {
        consoleOutput,
        consoleRef,
        handleFileChange,
        handleKeyDown
    }
}