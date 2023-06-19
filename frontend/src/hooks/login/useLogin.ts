import { useRef, useState } from "react"
import toast from "react-hot-toast"

const initialUser = {
    username: "",
    password: ""
}

export const useLogin = () => {
    const [user, setUser] = useState(initialUser)

    // Reference to form
    const form = useRef<HTMLFormElement>(null)

    const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        // TODO: Send user to backend
        console.log(
            `Carnet: ${user.username}\nPassword: ${user.password}`
        )

        // Reset form
        setUser(initialUser)
        form.current?.reset()

        // Show toast
        toast.success("Login successful")
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