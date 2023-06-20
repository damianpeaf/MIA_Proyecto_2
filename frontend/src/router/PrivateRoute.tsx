import { FC, ReactNode } from 'react'
import { Navigate } from 'react-router-dom';


interface PrivateRouteProps {
    children: ReactNode
}

export const PrivateRoute: FC<PrivateRouteProps> = ({ children }) => {

    const status = 'authenticated';

    return status === 'authenticated'
        ? (
            <>{children}</>
        )
        : <Navigate to="/login" />
}