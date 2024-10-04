import { json } from "d3";

const apiCalls = () => {

  const host = "0.0.0.0"

  const getAPIDatabases = async () => {
    const url = `http://${host}:8000/academic_sources`;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }

      const json = await response.json();
      return json;
    } catch (error) {

      return [];
    }
  }

  const postAPILogin = async (username: string, password: string) => {
    const url = `http://${host}:8000/auth/login`;
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    try {
      const response = await fetch(url, {
        method: 'POST',
        credentials:"include",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
      });
      if (!response.ok) {
        const errorData = (response).json;
        return new Error('Network error:' + JSON.stringify(errorData))
      }
      const data = await response.json();
      return data.access_token;
    }
    catch (error) {
      // console.error('Error:', error);
      return error;
    }


  }

  const getAPIResults = async (userDatabaseList:string[], inputsAndLogicalOperators:string[],
    emptyString:string, setInputs:any, setResults:any, setError:any, filterBlankInputs:string[], inputs:any, setDataFull:(item:boolean)=>void) =>{
    let data: Response;
    let jsonData;
    let queryString ='';
  
    for (let item of userDatabaseList){
        queryString += `&academic_database=${item}`;
    }
    if (inputsAndLogicalOperators.length === 0)
        setInputs([emptyString])
    else {
        setInputs([...filterBlankInputs])
        const apiQuery = inputsAndLogicalOperators.join('+')
  
        try {
    
          const url = `http://${host}:8000/academic_data?keywords=${apiQuery}${queryString}`
          console.log(url)
            data = await fetch(url, { method: "GET", credentials:"include"})
            jsonData = await data.json()
        
            if (data.status === 507) {
              setDataFull(true);
  
          } 

        }
        catch (error: any) {
      
  
            // jsonData = [{ "title": error.message, link: '' }]
            setError(error);
        }
    }
    if (jsonData !== undefined && jsonData.length > 0) {
        setResults(jsonData)
    }
    else {
        //set better error message
        // setError(data)
        setResults([]);
    }
}



const getAPISearches = async ( setError:any) =>{
  let data: Response;
  let jsonData;

      try {
  
        const url = `http://${host}:8000/search/user/searches`
          data = await fetch(url, { method: "GET", credentials:"include"})
          jsonData = await data.json()

      }
      catch (error: any) {
    

          // jsonData = [{ "title": error.message, link: '' }]
          // setError(error);
      }
  
  if (jsonData !== undefined && jsonData.length > 0) {
      return jsonData;
  }
  else {
      //set better error message
      // setError(data)
      return [];
  }
}



const getAPIPastSearchResults = async ( setResults:any, setError:any, search_id:number) =>{
  let data: Response;
  let jsonData;
      try {
  
        const url = `http://${host}:8000/search/user/articles?search_id=${search_id}`
          data = await fetch(url, { method: "GET", credentials:"include"})
          jsonData = await data.json()
          

      }
      catch (error: any) {
    

          // jsonData = [{ "title": error.message, link: '' }]
          setError(error);
      }
  if (jsonData !== undefined && jsonData.length > 0) {
      setResults(jsonData)
  }
  else {
      //set better error message
      // setError(data)
      setResults([]);
  }
}

const getAPIPastSearchTitle = async (search_id:number, setSearchName, setDisplayInputs) =>{
  let data: Response;
  let jsonData;
      try {
  
        const url = `http://${host}:8000/search/user/search/title?search_id=${search_id}`
          data = await fetch(url, { method: "GET", credentials:"include"})
          jsonData = await data.json()
          console.log(jsonData)

      }
      catch (error: any) {
    

          // jsonData = [{ "title": error.message, link: '' }]
          // setError(error);
      }
      console.log(jsonData)

  if (jsonData !== undefined ) {
      setSearchName(jsonData.title); 
      setDisplayInputs(jsonData.keywords);
  }
  else {
      //set better error message
      // setError(data)
      console.log(search_id)
      console.log(jsonData)
      return [];
  }
}


return {getAPIDatabases, postAPILogin, getAPIResults, getAPISearches, getAPIPastSearchResults, getAPIPastSearchTitle};

}


export default apiCalls;