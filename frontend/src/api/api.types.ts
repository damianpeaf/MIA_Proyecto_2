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
    }[],
    overall_status: boolean;
}

export interface AuthResponse {
    detail: ConsoleOutputResponse;
}