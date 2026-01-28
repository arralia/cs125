import NavBar from './Components/NavBar'
import ClassCardCollection from './Components/ClassCardCollection'
import LoginPage from './Pages/LoginPage'
import { useState } from 'react'

function App() {

  const [loginPrompt, setLogin] = useState(true);

  return (
    <>
      <NavBar setLogin={setLogin} />
      {loginPrompt ? <LoginPage setLogin={setLogin} /> : <ClassCardCollection />}
    </>
  )
}

export default App
