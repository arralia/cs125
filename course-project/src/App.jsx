import NavBar from './Components/NavBar'
import Card from './Components/Card'
import useApiCall from './Components/useApiCall'


function App() {
  const classes = useApiCall({ api: "/api/classInfo" });
  

  return (
    <>
      <NavBar />
      <div className="flex justify-left p-4 gap-4">
        <Card 
          className={classes?.data?.[0]?.className} 
          description={classes?.data?.[0]?.description} 
        />
        <Card 
          className={classes?.data?.[1]?.className} 
          description={classes?.data?.[1]?.description} 
        />
        <Card 
          className={classes?.data?.[2]?.className} 
          description={classes?.data?.[2]?.description} 
        />
      </div>
    </>
  )
}

export default App
