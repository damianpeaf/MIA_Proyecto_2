
import { FC, ReactNode } from "react"
import { Navigate } from 'react-router-dom';


interface PublicRouteProps {
    children: ReactNode
}

export const PublicRoute: FC<PublicRouteProps> = ({ children }) => {
    const status = 'authenticated';

    return status === 'authenticated'
        ? <Navigate to="/dashboard" />
        : (
            <>
                {children}
            </>
        )
}