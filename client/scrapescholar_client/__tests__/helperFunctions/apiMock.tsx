import itemsJson from "../mockData/ItemsTestJson";
import sourcesJson from "../mockData/DatabaseSourcesJson";
import pastSearchesTitle from "../mockData/pastSearchesTitle";
import pastSearchesArticles from "../mockData/pastSearchesArticles";

let simulateInsufficientStorage = false;
let deleteSearch = false;
const fetchMock = jest.fn((url) => {
  const academic_database_url = /^http:\/\/0.0.0.0:8000\/academic_data\?keywords\=/
  if (academic_database_url.test(url)) {
    if (simulateInsufficientStorage) {
      return Promise.resolve({
        ok: false,
        status: 507,
        json: jest.fn().mockResolvedValue({
          message: "Insufficient storage, you have 300 saved searches. Please delete some to continue"
        }),
        headers: new Headers(),
        redirected: false,
        statusText: 'Insufficient Storage',
      });
    }

    return Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(itemsJson),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',
    })
  }

  const academic_sources_url = /^http:\/\/0.0.0.0:8000\/academic_sources/
  if (academic_sources_url.test(url)) {
    return Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(sourcesJson),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',

    });
  }

  const past_search_title_url = /^http:\/\/0.0.0.0:8000\/search\/user\/search\/title\?search_id\=/
  const response = {
    "title": itemsJson.articles[0].title,
    "keywords": ["test input"]
  }
  if (past_search_title_url.test(url)) {
    return Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(response),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',

    });

  }

  const past_search_articles_url = /^http:\/\/0.0.0.0:8000\/search\/user\/articles\?search_id\=/

  if (past_search_articles_url.test(url)) {
    return Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(pastSearchesArticles),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',
    });
  }

  const past_searches_url = /^http:\/\/0.0.0.0:8000\/search\/user\/searches/

  if (past_searches_url.test(url)) {
    if (simulateInsufficientStorage) {
      let threehundredSearches = [];
      for (let i = 0; i <= 300; i++) {
        threehundredSearches.push({
          ...pastSearchesTitle[0],
          search_id: i + 1,
          title: `Test Title ${i}`
        })
      }
      if(deleteSearch){
        threehundredSearches.pop();
      }
      return Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve(threehundredSearches),
        headers: new Headers(),
        redirected: false,
        statusText: 'OK',
      });
    }
    return Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(pastSearchesTitle),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',
    });
  }
  return Promise.reject(new Error('Invalid URL'));
}) as jest.Mock;

export const setSimulateInsufficientStorage = (value:boolean) => {
  simulateInsufficientStorage = value;
};

export const setDeleteSearch = (value:boolean) => {
  deleteSearch = value;
};


export default fetchMock;