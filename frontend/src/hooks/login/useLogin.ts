import { useContext, useRef, useState } from "react"
import toast from "react-hot-toast"

import { AuthContext } from "../../context"
import fetchLogin from "../../api/authAPI"

const initialUser = {
    username: "",
    password: ""
}



export const useLogin = () => {
    const [user, setUser] = useState(initialUser)
    const { setIsAuthorized } = useContext(AuthContext)

    // Reference to form
    const form = useRef<HTMLFormElement>(null)

    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        const { username, password } = user

        // Reset form
        setUser(initialUser)
        form.current?.reset()

        // Fetch data from API
        const response = await fetchLogin(username, password)

        if (!response) {
            toast.error("Usuario o contraseña incorrectos")
            return
        }


        // Set isAuthorized to true
        setIsAuthorized(true)
        toast.success("Inicio de sesión exitoso")

    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUser({
            ...user,
            [e.target.name]: e.target.value
        })
    }

    return {
        user,
        form,
        onSubmit,
        handleInputChange
    }
}