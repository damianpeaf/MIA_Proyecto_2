import { FC } from "react"
import { ConsoleOutputI } from "../../api/api.types"

const styles:
    {
        [key: string]: string
    }
    = {
    "INFO": "text-gray-500 bg-gray-200 border-l-2 border-gray-700",
    "ERROR": "text-red-500 bg-red-100 border-l-2 border-red-700",
    "WARNING": "text-orange-500 bg-orange-100 border-l-2 border-orange-700",
    "SUCCESS": "text-green-500 bg-green-100 border-l-2 border-green-700",
}

export const ConsoleOutput: FC<ConsoleOutputI> = (
    {
        command,
        response
    }
) => {

    return (
        <>
            <div className={`text-sm border-b-[1px] px-2 py-4 border-gray-300`}>
                <p className={`font-semibold  text-[#5C6D74] mb-2`}>  {command}</p>
                {
                    response && response.output.map(({ msg_type, message, io_type, date }, index) => (

                        <p key={index} className={`${styles[msg_type]} p-2`}>
                            <span className="text-xs">
                                {
                                    new Date(date).toLocaleTimeString()
                                }
                            </span>
                            {
                                `
                                ${io_type === "INPUT" ? ">>" : "<<"} ${message}
                                `
                            }
                        </p>
                    ))
                }

            </div>
        </>
    )
}