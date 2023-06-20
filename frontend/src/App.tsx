import { Toaster } from "react-hot-toast"
import { useMediaQuery } from "./hooks";
import { BrowserRouter } from "react-router-dom";
import { AppRoute } from "./router";

export const App = () => {
  const largeScreen = useMediaQuery('(min-width: 640px)');
  return (
    <>
      <BrowserRouter>
        <Toaster toastOptions={
          {
            className: 'bg-light text-black text-xs md:text-sm xl:text-lg',
          }
        }

          position={
            largeScreen ? 'top-right' : 'bottom-center'
          } />
        <AppRoute />
      </BrowserRouter>
    </>
  )
}

export default App