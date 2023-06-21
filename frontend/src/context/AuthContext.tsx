import { FC, ReactNode, createContext, useReducer } from 'react';

interface AuthContextType {
    isAuthorized: boolean;
    setIsAuthorized: (isAuthorized: boolean) => void;
}

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthContext = createContext({} as AuthContextType);

const authReducer = (state: boolean, action: { type: string; payload: boolean }) => {
    switch (action.type) {
        case 'SET_AUTH':
            return action.payload;
        default:
            return state;
    }
};


export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
    const [isAuthorized, dispatch] = useReducer(authReducer, false);

    const setIsAuthorized = (isAuthorized: boolean) => {
        dispatch({ type: 'SET_AUTH', payload: isAuthorized });
    };

    return (
        <AuthContext.Provider value={{ isAuthorized, setIsAuthorized }}>
            {children}
        </AuthContext.Provider>
    );
};

