
const apiCalls = () => {

  const host = process.env.NEXT_PUBLIC_HOST_IP;

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
        credentials: "include",
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

  const getAPIResults = async (userDatabaseList: string[], inputsAndLogicalOperators: string[],
    emptyString: string, setInputs: any, setResults: any, setError: any,
    filterBlankInputs: string[], inputs: any, setDataFull: (item: boolean) => void,
    setCurrentSearchId: (item: number) => void) => {
    let data: Response;
    let jsonData;
    let queryString = '';
    for (let item of userDatabaseList) {
      queryString += `&academic_database=${item}`;
    }
    if (inputsAndLogicalOperators.length === 0)
      setInputs([emptyString])
    else {
      setInputs([...filterBlankInputs])
      const apiQuery = inputsAndLogicalOperators.join('%20')
      try {
        const url = `http://${host}:8000/academic_data?keywords=${apiQuery}${queryString}`
        data = await fetch(url, { method: "GET", credentials: "include" })
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
    if (jsonData !== undefined && jsonData.articles !== undefined && jsonData.articles.length > 0) {
      //maybe should have this get searchname and keywords too?

      setResults(jsonData.articles)
      setCurrentSearchId(jsonData.search_id)
    }
    else {
      //set better error message
      // setError(data)
      setResults([]);
    }
  }

  const getAPISearches = async (setError: any) => {
    let data: Response;
    let jsonData;
    try {
      const url = `http://${host}:8000/search/user/searches`
      data = await fetch(url, { method: "GET", credentials: "include" })
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

  const getAPIPastSearchResults = async (setResults: any, setError: any, search_id: number) => {
    let data: Response;
    let jsonData;
    try {
      const url = `http://${host}:8000/search/user/articles?search_id=${search_id}`
      data = await fetch(url, { method: "GET", credentials: "include" })
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

  const getAPIPastSearchTitle = async (search_id: number, setSearchName: (item: string) => void, setDisplayInputs: (item: string[]) => void) => {
    let data: Response;
    let jsonData;
    if (search_id > 0) {
      try {
        const url = `http://${host}:8000/search/user/search/title?search_id=${search_id}`
        data = await fetch(url, { method: "GET", credentials: "include" })
        jsonData = await data.json()
      }
      catch (error: any) {
        // jsonData = [{ "title": error.message, link: '' }]
        // setError(error);
      }

      if (jsonData !== undefined && (jsonData.title !== undefined || jsonData.keywords !== undefined)) {
        setSearchName(jsonData.title);
        const joinedKeywords = jsonData.keywords.join(' ');
        setDisplayInputs(joinedKeywords);
      }
      else {
        //set better error message
        // setError(data)
        return [];
      }
    }
  }

  const putSearchTitle = async (new_title: string, search_id: number,
    setSearchName: (item: string) => void,
    setLoading: (item: boolean) => void) => {
    let data: Response;
    let jsonData;
    /* responds with 
    {
      "user_id": 1,
      "search_keywords": [
          "abcdefghijkl,mop",
          "AND",
          "123456789"
      ],
      "title": "new title new",
      "search_date": null,
      "search_id": 17,
      "status": "active"
  } 
      */
    setLoading(true);
    try {

      const url = `http://${host}:8000/search/user/search/title?search_id=${search_id}`
      data = await fetch(url, {
        method: "PUT", credentials: "include", headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          { "title": new_title }
        )
      })
      jsonData = await data.json()
    }
    catch (error: any) {
      // jsonData = [{ "title": error.message, link: '' }]
      // setError(error);
    }

    if (jsonData !== undefined && jsonData.title !== undefined) {
      setSearchName(jsonData.title);

    }
    else {
      // console.log(jsonData)
    }
    setLoading(false)
  }

  const deleteSearch = async (search_id: number) => {
    let data: Response;
    let jsonData;
    try {
      const url = `http://${host}:8000/search/user/search/title?search_id=${search_id}`
      data = await fetch(url, {
        method: "DELETE", credentials: "include"
      })
      jsonData = await data.json()
    }
    catch (error: any) {
      // jsonData = [{ "title": error.message, link: '' }]
      // setError(error);
    }
    if (jsonData !== undefined) {
      // console.log("Search deleted")
    }
    else {
      // console.log(jsonData)
      console.log("failure to delete search")
    }
  }


  const putUserData = async (new_data: {}) => {
    let data: Response;
    let jsonData;

    try {

      const url = `http://${host}:8000/user_data/update`
      data = await fetch(url, {
        method: "PUT", credentials: "include", headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
           new_data 
        )
      })
      jsonData = await data.json()
    }
    catch (error: any) {
      // jsonData = [{ "title": error.message, link: '' }]
      // setError(error);
    }

    if (jsonData !== undefined && jsonData.title !== undefined) {
      //hapy path

    }
    else {
      //something went wrong!
      // console.log(jsonData)
    }

  }

  const getCommentsByArticle = async (articleId: number) => {
    try {
      const url = `http://${host}:8000/comment/article/${articleId}/comments`;
      const response = await fetch(url, { method: "GET", credentials: "include" });
      if (!response.ok) {
        throw new Error(`Error fetching comments for article ${articleId}: ${response.statusText}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching comments:", error);
      return [];
    }
  }

  // Add a new comment
  const addComment = async (articleId: number, commentText: string) => {
    try {
        const url = `http://${host}:8000/comment/article/${articleId}`;
        const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                comment_text: commentText
            }),
        });

        if (!response.ok) {
            throw new Error(`Error adding comment for article ${articleId}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error adding comment:", error);
        return null;
    }
  }

  // Edit an existing comment
  const editComment = async (commentId: number, updatedText: string) => {
    try {
      const url = `http://${host}:8000/comment/${commentId}`;
      const response = await fetch(url, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          comment_text: updatedText, 
        }),
      });

      if (!response.ok) {
        throw new Error(`Error editing comment ${commentId}: ${response.statusText}`);
      }

      const data = await response.json();
      return data;  // Return the updated comment data
    } catch (error) {
      console.error("Error editing comment:", error);
      return null;
    }
  };

  // Delete an existing comment
  const deleteComment = async (commentId: number) => {
    try {
      const url = `http://${host}:8000/comment/${commentId}`;
      const response = await fetch(url, {
        method: 'DELETE',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`Error deleting comment ${commentId}: ${response.statusText}`);
      }

      return true;  // Return true on successful deletion
    } catch (error) {
      console.error("Error deleting comment:", error);
      return false;
    }
  };



  const getCookie= async ()=>{
    let data;
    let jsonData

    try {
      const url = `http://${host}:8000/auth/get_cookie`
      data = await fetch(url, { method: "GET", credentials: "include" })
      jsonData = await data.json()
      console.log(jsonData)
      return jsonData;
    }
    catch (error: any) {
      // jsonData = [{ "title": error.message, link: '' }]
      // setError(error);
      return {detail:"Cookie not found"};
    }

  }


  const isAdmin= async ()=>{
    let data;
    let textData

    try {
      const url = `http://${host}:8000/auth/is_admin`
      data = await fetch(url, { method: "GET", credentials: "include" })
      textData = await data.text()
      console.log(textData)
      return textData;
    }
    catch (error: any) {
      // jsonData = [{ "title": error.message, link: '' }]
      // setError(error);
      return {detail:"Admin request failed"};
    }

  }

  const deleteCookie= async ()=>{
    let data;
    let jsonData

    try {
      const url = `http://${host}:8000/auth/remove_cookie`
      data = await fetch(url, { method: "GET", credentials: "include" })
      jsonData = await data.json()
      console.log(jsonData)
      return jsonData;
    }
    catch (error: any) {
      // jsonData = [{ "title": error.message, link: '' }]
      // setError(error);
      return [];
    }

  }
  
  const putSearchShare = async (shared_with_user: string, search_id: number,
  
    // setLoading: (item: boolean) => void
  ) => {
    let data: Response;
    let jsonData;
    /* responds with 
    {
      "user_id": 1,
      "search_keywords": [
          "abcdefghijkl,mop",
          "AND",
          "123456789"
      ],
      "title": "new title new",
      "search_date": null,
      "search_id": 17,
      "status": "active"
  } 
      */
     //maybe different loading?
    // setLoading(true);
    try {
      const url = `http://${host}:8000/search/share?search_id=${search_id}&share_user=${shared_with_user}`
      data = await fetch(url, {
        method: "PUT", credentials: "include", headers: {
          'Content-Type': 'application/json'
        },
      })

      if (data.status === 404) {
        // Handle 404 error specifically by returning false
        return false;
      }
      jsonData = await data.json()
      return true
    }
    catch (error: any) {
      // jsonData = [{ "title": error.message, link: '' }]
      // setError(error);
      return false
    }

    // setLoading(false)
  }

  const downloadURL= `http://${host}:8000/download?search_id=`

  return { getAPIDatabases, postAPILogin, 
    getAPIResults, getAPISearches, getAPIPastSearchResults, 
    getAPIPastSearchTitle, putSearchTitle, 
    deleteSearch, putUserData, getCookie, deleteCookie, 
    getCommentsByArticle,
    addComment,
    editComment,
    deleteComment, downloadURL, putSearchShare, isAdmin   };

}

export default apiCalls;