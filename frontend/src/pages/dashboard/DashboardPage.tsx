import { ConsoleOutput } from "../../components";
import { useDashboard } from "../../hooks";

export const DashboardPage = () => {

    const {
        consoleOutput,
        fileInputRef,
        handleFileChange,
        handleKeyDown,
        handleLogout,
        handleExecuteCommand,
    } = useDashboard();


    return (
        <>
            <section className="h-screen">
                <div className="flex flex-row gap-4 items-center justify-center px-6 py-8 mx-auto lg:py-0 h-1/4">
                    <div className="flex flex-col md:flex-row w-full">
                        <label className="block mb-2 text-sm font-medium text-gray-900" htmlFor="multiple_files">Cargar archivo</label>
                        <input ref={fileInputRef} className="block w-full file:h-full file:bg-primary-600 file:cursor-pointer file:text-white file:border-0 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50  focus:outline-none" type="file" onChange={handleFileChange} />
                    </div>
                    <button type="submit"
                        id="run-btn"
                        onClick={handleExecuteCommand}
                        aria-label="Ejecutar programa"
                        className=" text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Ejecutar</button>
                </div>
                <div className="flex flex-col w-full p-4 gap-4 h-3/4">
                    {/* Output console */}
                    <div className="flex overflow-y-auto flex-col-reverse border border-gray-300 rounded flex-1 bg-gray-100 ">
                        {
                            consoleOutput.slice().reverse().map(({ command, response }, index) => (
                                <ConsoleOutput key={index} command={command} response={response} />
                            )
                            )
                        }
                    </div>

                    {/* Input console, aling text in the middle vertical*/}
                    <textarea name="" className="border border-gray-300 rounded h-16 p-2 items-center align-middle" onKeyDown={handleKeyDown}></textarea>
                </div>
            </section>

            <button
                onClick={handleLogout}
                className="fixed text-sm top-5 right-5 px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg"
                id="logoutBtn">
                Cerrar sesión
            </button>
        </>
    )
}