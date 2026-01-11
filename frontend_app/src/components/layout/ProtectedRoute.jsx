import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { getUser } from "../../hooks/user.actions";

function ProtectedRoute() {
    const user = getUser();
    return user ? <Outlet /> : <Navigate to="/login/" />;
}

export default ProtectedRoute;