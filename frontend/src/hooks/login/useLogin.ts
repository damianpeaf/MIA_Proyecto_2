import { useContext, useRef, useState } from "react"
import toast from "react-hot-toast"
import { AuthContext } from "../../context/AuthContext"

const initialUser = {
    username: "",
    password: ""
}

export const useLogin = () => {
    const [user, setUser] = useState(initialUser)
    const { setIsAuthorized } = useContext(AuthContext)

    // Reference to form
    const form = useRef<HTMLFormElement>(null)

    const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        // const { username, password } = user
        // TODO: connect to backend

        // Set isAuthorized to true
        setIsAuthorized(true)

        // Reset form
        setUser(initialUser)
        form.current?.reset()

        // Show toast
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