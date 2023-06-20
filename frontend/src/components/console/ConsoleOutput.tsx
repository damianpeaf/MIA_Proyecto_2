import { FC } from "react"
import { ConsoleOutputI } from "../../hooks"

const styles:
    {
        [key: string]: string
    }
    = {
    "info": "text-gray-500",
    "error": "text-red-500",
    "warning": "text-orange-500",
    "success": "text-[#6F762F]",
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
                <p className={`font-semibold  text-[#5C6D74] mb-2`}>{command}</p>
                <span className={`text-[#798789]`}>
                    {
                        response && response.map(({ text, type }, index) => (
                            <p key={index} className={`${styles[type]}`}>{text}</p>
                        ))
                    }
                </span>
            </div>
        </>
    )
}