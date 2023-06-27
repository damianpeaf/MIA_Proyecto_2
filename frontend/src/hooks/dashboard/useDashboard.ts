import { useContext, useRef, useState } from "react";
import { readFiles } from "../../utils";
import { AuthContext } from "../../context";
import toast from 'react-hot-toast';
import fetchCommand from "../../api/commandAPI";
import { ConsoleOutputI, ConsoleOutputResponse } from "../../api/api.types";

const initialConsoleOutput: ConsoleOutputI[] = []

export const useDashboard = () => {
    const [consoleOutput, setConsoleOutput] = useState<ConsoleOutputI[]>(initialConsoleOutput);
    const [contentFromFile, setContentFromFile] = useState<string[]>([]);
    const { setIsAuthorized } = useContext(AuthContext);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const textAreaRef = useRef<HTMLTextAreaElement>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;
        readFiles(files)
            .then((data) => {
                setContentFromFile(data[0].split('\n'));
                toast.success('Archivo cargado correctamente');
            })
            .catch((error) => {
                toast.error('Error al cargar el archivo', error);
            });
    };

    const handleKeyDown = async (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const command = e.currentTarget.value;

            if (command === '') return;

            if (command === 'clear') {
                setConsoleOutput([]);
                e.currentTarget.value = '';
                return;
            }

            const loadingToast = toast.loading('Esperando al servidor...');

            try {
                const response: ConsoleOutputResponse = await fetchCommand(command);
                setConsoleOutput(prev => prev.concat({
                    'command': command,
                    'response': response
                }));
                toast.success('Solicitud completada correctamente', { id: loadingToast });
            } catch (error) {
                toast.error('Error al procesar la solicitud', { id: loadingToast });
            }

            if (textAreaRef.current) {
                textAreaRef.current.value = '';
            }
        }
    };

    const handleLogout = () => {
        setIsAuthorized(false);
        toast.success('Sesión cerrada correctamente');
    };

    const handleExecuteCommand = async () => {
        
        for (const command of contentFromFile) {

            if(command.trim() === '') continue;

            const loadingToast = toast.loading('Esperando al servidor...');

            try {
                const response: ConsoleOutputResponse = await fetchCommand(command);
                setConsoleOutput(prev => prev.concat({
                    'command': command,
                    'response': response
                }));
                toast.success('Solicitud completada correctamente', { id: loadingToast });
            } catch (error) {
                setConsoleOutput(prev => prev.concat({
                    'command': command,
                   response:{
                    output: [],
                    "overall_status": false,
                    "data": {
                    }
                   }
                    
                }));
                console.log(error)
                toast.error('Error al procesar la solicitud', { id: loadingToast });
            }
        }

        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return {
        consoleOutput,
        fileInputRef,
        textAreaRef,
        handleExecuteCommand,
        handleFileChange,
        handleKeyDown,
        handleLogout
    };
};
