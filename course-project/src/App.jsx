import NavBar from './Components/NavBar'
import ClassCardCollection from './Components/ClassCardCollection'
import UserSettingsPage from './Pages/UserSettingsPage'
import LoginPage from './Pages/LoginPage'
import { useState } from 'react'

function App() {

  const [loginPrompt, setLogin] = useState(false);
  const [settingsPrompt, setSettings] = useState(false);

  return (
    <>
      <NavBar setLogin={setLogin} setSettings={setSettings} />
      {loginPrompt ? <LoginPage setLogin={setLogin} /> : <ClassCardCollection />}
      {settingsPrompt ? <UserSettingsPage setSettings={setSettings} /> : null}
    </>
  )
}

export default App
