
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

  const getAPIResults = async (userDatabaseList:string[], inputsAndLogicalOperators:string[],emptyString:string, setInputs:any, setResults:any, setError:any, filterBlankInputs:string[]) =>{let data: Response;
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
            data = await fetch(url, { method: "GET", credentials:"include"})
            jsonData = await data.json()
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
        setResults([]);
    }
}

return {getAPIDatabases, postAPILogin, getAPIResults};

}


export default apiCalls;