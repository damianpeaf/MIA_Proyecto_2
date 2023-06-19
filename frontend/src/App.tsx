import { Toaster } from "react-hot-toast"
import { DashboardPage, LoginPage } from "./pages"
import { useMediaQuery } from "./hooks";

export const App = () => {
  const largeScreen = useMediaQuery('(min-width: 640px)');
  return (
    <>
      <Toaster toastOptions={
        {
          className: 'bg-light text-black text-xs md:text-sm xl:text-lg',
        }
      }

        position={
          largeScreen ? 'top-right' : 'bottom-center'
        } />
      {/* <LoginPage /> */}
      <DashboardPage />
    </>
  )
}

export default App