import { NewUser } from "../components/UserManagement/modal/AddUserModal";
import httpStringGen from "@/app/api/httpString";
import _ from 'lodash';
import { APIKeyInterface } from "../components/SearchView/modal/APIKeyModal";
const apiCalls = () => {
  const host = _.escapeRegExp(process.env.NEXT_PUBLIC_HOST_IP);
  const http_string = httpStringGen();

  interface NewArticle {
    search_id: number,
    title: string,
    date: string,
    citedby: number,
    source_id: number,
    document_type: string,
    abstract: string,
    link: string
  }

  const getAPIDatabases = async () => {
    const url = `${http_string}://${host}:8000/academic_sources`;
    try {
      const response = await fetch(url, { method: "GET", credentials: "include" });
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const json = await response.json();
      return json;
    } catch (error) {
      return [];
    }
  }

  const getAPIDatabasesAndIDs = async () => {
    const url = `${http_string}://${host}:8000/academic_sources_id`;
    try {
      const response = await fetch(url, { method: "GET", credentials: "include" });
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
    const url = `${http_string}://${host}:8000/auth/login`;
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

  const getAPIResults = async (
    userDatabaseList: string[], inputsAndLogicalOperators: string[],
    emptyString: string, setInputs: any, setResults: any, setError: any,
    filterBlankInputs: string[], inputs: any, setDataFull: (item: boolean) => void,
    setCurrentSearchId: (item: number) => void, apiKey:APIKeyInterface
  ) => {
    let data: Response;
    let jsonData;
    let queryString = '';
    console.log(apiKey)
    for (let item of userDatabaseList) {
      queryString += `&academic_database=${item}`;
    }
    if (inputsAndLogicalOperators.length === 0)
      setInputs([emptyString])
    else {
      setInputs([...filterBlankInputs])
      const apiQuery = inputsAndLogicalOperators.join('%20')
      
      try {
        const url = `${http_string}://${host}:8000/academic_data?keywords=${apiQuery}${queryString}`
        
        data = await fetch(url, { 
          method: "POST", 
          credentials: "include", 
          headers:{"Content-Type":"application/json"},
        body:JSON.stringify(apiKey) })
        jsonData = await data.json()
        if (data.status === 507) {
          setDataFull(true);
        }
      }
      catch (error: any) {
        setError(error);
      }
    }
    if (jsonData !== undefined && jsonData.articles !== undefined && jsonData.articles.length > 0) {
      setResults(jsonData.articles)
      setCurrentSearchId(jsonData.search_id)
      return jsonData
    }
    else {
      setResults([]);
      return []
    }
  }

  const getAPISearches = async (setError: any) => {
    let data: Response;
    let jsonData;
    try {
      const url = `${http_string}://${host}:8000/search/user/searches`
      data = await fetch(url, { method: "GET", credentials: "include" })
      jsonData = await data.json()
    }
    catch (error: any) {
    }

    if (jsonData !== undefined && jsonData.length > 0) {
      return jsonData;
    }
    else {
      return [];
    }
  }

  const getAPIPastSearchResults = async (setResults: any, setError: any, search_id: number) => {
    let data: Response;
    let jsonData;
    try {
      const url = `${http_string}://${host}:8000/search/user/articles?search_id=${search_id}`
      data = await fetch(url, { method: "GET", credentials: "include" })
      jsonData = await data.json()
    }
    catch (error: any) {
      setError(error);
    }
    if (jsonData !== undefined && jsonData.length > 0) {
      setResults(jsonData)
      return jsonData
    }
    else {
      setResults([]);
      return []
    }
  }

  const getAPIPastSearchTitle = async (search_id: number, setSearchName: (item: string) => void, setDisplayInputs: (item: string[]) => void) => {
    let data: Response;
    let jsonData;
    if (search_id > 0) {
      try {
        const url = `${http_string}://${host}:8000/search/user/search/title?search_id=${search_id}`
        data = await fetch(url, { method: "GET", credentials: "include" })
        jsonData = await data.json()
      }
      catch (error: any) {
      }
      if (jsonData !== undefined && (jsonData.title !== undefined || jsonData.keywords !== undefined)) {
        setSearchName(jsonData.title);
        const joinedKeywords = jsonData.keywords.join(' ');
        setDisplayInputs(joinedKeywords);
      }
      else {
        return [];
      }
    }
  }

  const putSearchTitle = async (new_title: string, search_id: number,
    setSearchName: (item: string) => void,
    setLoading: (item: boolean) => void) => {
    let data: Response;
    let jsonData;
    setLoading(true);
    try {
      const url = `${http_string}://${host}:8000/search/user/search/title?search_id=${search_id}`
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
    }
    if (jsonData !== undefined && jsonData.title !== undefined) {
      setSearchName(jsonData.title);
    }
    setLoading(false)
  }

  const deleteSearch = async (search_id: number) => {
    let data: Response;
    let jsonData;
    try {
      const url = `${http_string}://${host}:8000/search/user/search/title?search_id=${search_id}`
      data = await fetch(url, {
        method: "DELETE", credentials: "include"
      })
      jsonData = await data.json()
    }
    catch (error: any) {
    }
  }


  const putUserData = async (new_data: {}) => {
    let data: Response;
    let jsonData;
    try {
      const url = `${http_string}://${host}:8000/user_data/update`
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
    }
  }

  const getCommentsByArticle = async (articleId: number) => {
    try {
      const url = `${http_string}://${host}:8000/comment/article/${articleId}/comments`;
      const response = await fetch(url, { method: "GET", credentials: "include" });
      if (!response.ok) {
        throw new Error(`Error fetching comments for article ${articleId}: ${response.statusText}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      return [];
    }
  }

  const addComment = async (articleId: number, commentText: string) => {
    try {
      const url = `${http_string}://${host}:8000/comment/article/${articleId}`;
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

  const editComment = async (commentId: number, updatedText: string) => {
    try {
      const url = `${http_string}://${host}:8000/comment/${commentId}`;
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

  const deleteComment = async (commentId: number) => {
    try {
      const url = `${http_string}://${host}:8000/comment/${commentId}`;
      const response = await fetch(url, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error(`Error deleting comment ${commentId}: ${response.statusText}`);
      }
      return true;
    } catch (error) {
      console.error("Error deleting comment:", error);
      return false;
    }
  };

  const getCookie = async () => {
    let data;
    let jsonData
    try {
      const url = `${http_string}://${host}:8000/auth/get_cookie`
      data = await fetch(url, { method: "GET", credentials: "include" })
      jsonData = await data.json()
      return jsonData;
    }
    catch (error: any) {
      return { detail: "Cookie not found" };
    }

  }

  const isAdmin = async () => {
    let data;
    let textData

    try {
      const url = `${http_string}://${host}:8000/auth/is_admin`
      data = await fetch(url, { method: "GET", credentials: "include" })
      textData = await data.text()
      return textData;
    }
    catch (error: any) {
      return { detail: "Admin request failed" };
    }

  }

  const deleteCookie = async () => {
    let data;
    let jsonData

    try {
      const url = `${http_string}://${host}:8000/auth/remove_cookie`
      data = await fetch(url, { method: "GET", credentials: "include" })
      jsonData = await data.json()
      return jsonData;
    }
    catch (error: any) {
      return [];
    }

  }

  const putSearchShare = async (shared_with_user: string, search_id: number) => {
    let data: Response;
    let jsonData;
    try {
      const url = `${http_string}://${host}:8000/search/share?search_id=${search_id}&share_user=${shared_with_user}`
      data = await fetch(url, {
        method: "PUT", credentials: "include", headers: {
          'Content-Type': 'application/json'
        },
      })
      if (data.status === 404) {
        return false;
      }
      jsonData = await data.json()
      return true
    }
    catch (error: any) {
      return false
    }
  }

  const downloadURL = `${http_string}://${host}:8000/download?search_id=`

  const addUser = async (userBody: NewUser) => {
    try {
      const url = `${http_string}://${host}:8000/users/create`;
      const response = await fetch(url, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(
          userBody
        ),
      });
      if (!response.ok) {
        throw new Error(`Error adding user: ${response.statusText}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      return null;
    }
  }

  const getUsers = async () => {
    const url = `${http_string}://${host}:8000/users/get`;
    try {
      const response = await fetch(url, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const json = await response.json();
      return json;
    } catch (error) {
      return [];
    }
  }


  const deleteUserAPI = async (user_id: number) => {
    let data: Response;
    let jsonData;
    try {
      const url = `${http_string}://${host}:8000/users/delete/${user_id}`
      data = await fetch(url, {
        method: "DELETE", credentials: "include"
      })
      jsonData = await data.json()
    }
    catch (error: any) {
    }
  }

  const updateUserRole = async (userId: number, newRole: string) => {
    const url = `${http_string}://${host}:8000/users/update-role/${userId}`;
    try {
      const response = await fetch(url, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ role_name: newRole }),  // Send role_name in the request body
      });
      if (!response.ok) {
        throw new Error(`Error updating user role: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error updating user role:", error);
      return null;
    }
  };

  const addArticle = async (articleBody: NewArticle) => {
    try {
      const url = `${http_string}://${host}:8000/article`;
      const response = await fetch(url, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(
          articleBody
        ),
      });
      if (!response.ok) {
        throw new Error(`Error adding user: ${response.statusText}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      return null;
    }
  }

  const deleteArticleAPI = async (article_id: number) => {
    let data: Response;
    let jsonData;
    try {
      const url = `${http_string}://${host}:8000/article/${article_id}`
      data = await fetch(url, {
        method: "DELETE", credentials: "include"
      })
      jsonData = await data.json()
    }
    catch (error: any) {
    }

  }


  const verifyAPIKey = async (APIKey: string, academicSource: string) => {
    let data: Response;
    let status;
    let academic_url;
    switch (academicSource) {
      case 'scopus':
        academic_url = "https://api.elsevier.com/content/search/scopus?query=all(gene)&apiKey="
        break;
      case 'sciencedirect':
        academic_url = "https://api.elsevier.com/content/search/sciencedirect?query=gene&apiKey=";
        break;
      default:
        return false
    }
    try {
      const url = `${academic_url}${APIKey}`
      data = await fetch(url, {
        method: "GET"
      })
      status = data.status;
      if (status == 200) {
        return true
      } else {
        return false
      }
    }
    catch (error: any) {
      return false
    }

  }

  return {
    getAPIDatabases, postAPILogin,
    getAPIResults, getAPISearches, getAPIPastSearchResults,
    getAPIPastSearchTitle, putSearchTitle,
    deleteSearch, putUserData, getCookie, deleteCookie,
    getCommentsByArticle,
    addComment,
    editComment,
    deleteComment, downloadURL, putSearchShare,
    isAdmin, addUser, getUsers, deleteUserAPI, updateUserRole,
    getAPIDatabasesAndIDs, addArticle, deleteArticleAPI, verifyAPIKey
  };
}

export default apiCalls;