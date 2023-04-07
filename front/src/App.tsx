import { useState, useEffect, SetStateAction } from 'react'
import './App.css'

const App = () => {
  const [search, setSearch] = useState<string>("")
  const [results, setResults] = useState<Array<any>>([])
  const [suggestions, setSuggestions] = useState<Array<any>>([])
  const [recommendations, setRecommendations] = useState<Array<any>>([])
  const [switchResult, setSwitchResult] = useState<boolean>(false)

  const searchLink : string = "http://127.0.0.1:5000/?search="
  const suggestionLink : string = "http://127.0.0.1:5000/sugg?id="
  const recommmendLink : string = "http://127.0.0.1:5000/recommend"

  const filterSearch = () => search.split(" ").filter((word) => word.length > 2).join(" ")

  const getData = (input : number | string | undefined, link : string) => {
    const headersOpt : object = {
      "content-type": "application/json",
    }

    const requestOptions : object = {
      method: 'GET',
      headers : headersOpt,
      redirect: 'follow'
    };

    console.log(input)
    
    fetch(link + (input === undefined ? "" : input), requestOptions)
      .then(response => response.json())
      .then(result => {
        switch(typeof(input)){
          case "number" : { setSuggestions(result["results"]); break; }
          case "string" : { setResults(result["results"]); break; }
          case "undefined" : { setRecommendations(result["results"]); break; }
        }
      })
      .catch(error => console.log(error))
  }

  const resultView = (result : any) => {
    const id : number = result[0];
    const title : string = result[1];

    return(
      <div className="card" style={{marginTop: "10%"}}>
        <h3>{title}</h3>
        <img src={"https://www.gutenberg.org/cache/epub/"+id+"/pg"+id+".cover.medium.jpg"}/>
      </div>
    )
  }

  useEffect(() => {
    getData(undefined, recommmendLink);
  }, [])

  useEffect(() => {
    if(results) console.log(results);
    if(results.length > 0) { getData(results[0][0], suggestionLink); console.log(suggestions)}
  }, [results])

  return (
    <div className="App">
      <div style={{display: "flex", justifyContent: "center"}}>
        <input onChange={(e) => setSearch(e.target.value)}/>
        <button onClick={() => {getData(filterSearch(), searchLink); setSwitchResult(true)}}>Search</button>
      </div>
      <div>
        { switchResult ? <h1>Results</h1> : "" }
        { switchResult ? results.map(result => resultView(result)) : "" }
      </div>
      <div>
        { switchResult ? <h1>Suggestions</h1> : "" }
        { suggestions.map(suggestion => resultView(suggestion)) }
      </div>
      <div>
        { !switchResult ? <h1>Most recommended books</h1> : "" }
        { !switchResult ? recommendations.map(recommendation => resultView(recommendation)) : "" }
      </div>
    </div>
  )
}

export default App
