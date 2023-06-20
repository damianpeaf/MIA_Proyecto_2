import { Route, Routes } from "react-router-dom";
import { PublicRoute, PrivateRoute } from "./";
import { DashboardPage, LoginPage } from "../pages";

export const AppRoute = () => {
    const status = 'authenticated';

    return (
        <>
            <Routes>
                <Route
                    path="/login"
                    element={
                        <PublicRoute>
                            <LoginPage />
                        </PublicRoute>
                    }
                />

                <Route
                    path="/dashboard"
                    element={
                        <PrivateRoute>
                            <DashboardPage />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/*"
                    element={
                        <PublicRoute>
                            <LoginPage />
                        </PublicRoute>
                    }
                />
            </Routes>
        </>
    );
}