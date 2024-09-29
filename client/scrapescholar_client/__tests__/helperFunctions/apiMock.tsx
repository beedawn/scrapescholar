import itemsJson from "../mockData/ItemsTestJson";
import sourcesJson from "../mockData/DatabaseSourcesJson";

const fetchMock = jest.fn((url) => {
    const academic_database_url = /^http:\/\/0.0.0.0:8000\/academic_data\?keywords\=/

    const academic_sources_url =/^http:\/\/0.0.0.0:8000\/academic_sources/
    if (academic_database_url.test(url)) {
      return Promise.resolve({
            ok: true,
            status: 200,
            json: () => Promise.resolve(itemsJson),
            headers: new Headers(),
            redirected: false,
            statusText: 'OK',
      
          })
    

}
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
    return Promise.reject(new Error('Invalid URL'));
}) as jest.Mock;


export default fetchMock;