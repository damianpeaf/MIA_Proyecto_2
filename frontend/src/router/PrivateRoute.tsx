import { FC, ReactNode, useContext } from 'react'
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';


interface PrivateRouteProps {
    children: ReactNode
}

export const PrivateRoute: FC<PrivateRouteProps> = ({ children }) => {

    // Use context to get the current authentication status
    const { isAuthorized } = useContext(AuthContext);

    return isAuthorized
        ? (
            <>{children}</>
        )
        : <Navigate to="/login" />
}