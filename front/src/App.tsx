import { useState, useEffect } from 'react'
import './App.css'

const App = () => {
  const [search, setSearch] = useState<string>("")
  const [results, setResults] = useState<Array<any>>([])

  const filterSearch = () => search.split(" ").filter((word) => word.length > 2).join(" ")

  const getData = () => {
    const headersOpt = {
      "content-type": "application/json",
    }

    const requestOptions = {
      method: 'GET',
      headers : headersOpt,
      redirect: 'follow'
    };
    
    fetch("http://127.0.0.1:5000/?search=" + filterSearch(), requestOptions)
      .then(response => response.json())
      .then(result => setResults(result["result"]))
      .catch(error => console.log(error))
  }

  const resultView = (result : any) => {
    const title = result[1];
    const id = result[0];

    return(
      <div>
        <img src={"https://www.gutenberg.org/cache/epub/"+id+"/pg"+id+".cover.medium.jpg"}/>
        <p>{title}</p>
      </div>
    )
  }

  useEffect(() => results ? console.log(results) : undefined, [results])

  return (
    <div className="App">
      <input onChange={(e) => setSearch(e.target.value)}/>
      <button onClick={() => getData()}>Go</button>
      <div>
        {results.map(result => resultView(result))}
      </div>
    </div>
  )
}

export default App
