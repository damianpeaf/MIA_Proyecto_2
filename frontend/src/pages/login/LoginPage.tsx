import { useLogin } from "../../hooks"


export const LoginPage = () => {

    const { form, onSubmit, handleInputChange } = useLogin();

    return (
        <>
            <section>
                <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                    <a href="#" className="flex items-center mb-6 text-2xl font-semibold text-gray-900">
                        <img className="w-8 h-8 mr-2" src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/logo.svg"
                            alt="logo" />
                        Proyecto 2
                    </a>
                    <div className="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
                        <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                            <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
                                Inicia sesión
                            </h1>
                            <form className="space-y-4 md:space-y-6" action="#" id="login-form" onSubmit={onSubmit} ref={form}>
                                <div>
                                    <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900">Usuario</label>
                                    <input type="username" name="username" id="username"
                                        aria-describedby="username-description"
                                        className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                                        placeholder="2021000000" autoComplete="off" onChange={handleInputChange} />
                                </div>
                                <div>
                                    <label htmlFor="password"
                                        className="block mb-2 text-sm font-medium text-gray-900">Contraseña</label>
                                    <input type="password" name="password" id="password" placeholder="••••••••"
                                        autoComplete="off"
                                        onChange={handleInputChange}
                                        className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                                    />
                                </div>

                                <button type="submit" id="login-btn"
                                    aria-label="Iniciar sesión"
                                    className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Iniciar
                                    sesión</button>
                            </form>
                        </div>
                    </div>
                </div>
            </section>
        </>
    )
}