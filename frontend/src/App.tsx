import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
      <div className="h-screen flex items-center justify-center bg-cyber-blue text-white">
      <h1 className="text-4xl font-bold">Tailwind is working!</h1>
    </div>
      </div>
      <h1>Vite + React</h1>

    </>
  )
}

export default App
