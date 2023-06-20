import { FC } from "react"
import { ConsoleOutputI } from "../../hooks"

const styles:
    {
        [key: string]: string
    }
    = {
    "info": "",
    "error": "bg-red-100",
    "warning": "",
    "success": "",
}

export const ConsoleOutput: FC<ConsoleOutputI> = (
    {
        command,
        type,
        response
    }
) => {


    return (
        <>
            <div className={`text-sm border-b-[1px] px-2 py-4 border-gray-300 ${styles[type]}`}>
                {
                    type === 'error' && <span className="relative bg-red-500 w-2 h-full">

                    </span>
                }
                <p className={`font-semibold  text-[#5C6D74] mb-2`}>{command}</p>
                <span className={`text-[#798789]`}>
                    {
                        response && response.map((res, index) => (
                            <p key={index}>{res}</p>
                        ))
                    }
                </span>
            </div>
        </>
    )
}