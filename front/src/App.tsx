import { useState, useEffect, SetStateAction } from 'react'
import './App.css'

const App = () => {
  const [search, setSearch] = useState<string>("")
  const [results, setResults] = useState<Array<any>>([])
  const [suggestions, setSuggestions] = useState<Array<any>>([])

  const searchLink : string = "http://127.0.0.1:5000/?search="
  const suggestionLink : string = "http://127.0.0.1:5000/sugg?id="

  const filterSearch = () => search.split(" ").filter((word) => word.length > 2).join(" ")

  const getData = () => {
    const headersOpt : object = {
      "content-type": "application/json",
    }

    const requestOptions : object = {
      method: 'GET',
      headers : headersOpt,
      redirect: 'follow'
    };
    
    fetch("http://127.0.0.1:5000/?search=" + filterSearch(), requestOptions)
      .then(response => response.json())
      .then(result => {console.log(result);setResults(result["results"])})
      .catch(error => console.log(error))
  }

  const getSuggestions = (id : number) => {
    const headersOpt : object = {
      "content-type": "application/json",
    }

    const requestOptions : object = {
      method: 'GET',
      headers : headersOpt,
      redirect: 'follow'
    };
    
    fetch("http://127.0.0.1:5000/sugg?id=" + id, requestOptions)
      .then(response => response.json())
      .then(result => setSuggestions(JSON.parse(result["results"])))
      .catch(error => console.log(error))
  }

  const resultView = (result : any) => {
    const title = result[1];
    const id = result[0];

    return(
      <div className="card" style={{marginTop: "10%"}}>
        <h3>{title}</h3>
        <img src={"https://www.gutenberg.org/cache/epub/"+id+"/pg"+id+".cover.medium.jpg"}/>
      </div>
    )
  }

  useEffect(() => {
    if(results) console.log(results);
    getSuggestions(4);
  }, [results])

  return (
    <div className="App">
      <div style={{display: "flex", justifyContent: "center"}}>
        <input onChange={(e) => setSearch(e.target.value)}/>
        <button onClick={() => getData()}>Search</button>
      </div>
      <div>
        {results.map(result => resultView(result))}
      </div>
      <div>
        <h1>Suggestions</h1>
        {Array.from(suggestions).map(suggestion => resultView([suggestion, "title"]))}
      </div>
    </div>
  )
}

export default App
