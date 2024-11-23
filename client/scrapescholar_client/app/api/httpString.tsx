const ENVIRONMENT = process.env.NEXT_PUBLIC_ENVIRONMENT;

const httpStringGen = ()=>{



  if (ENVIRONMENT=="PROD" || ENVIRONMENT=="prod"||ENVIRONMENT=="production"||ENVIRONMENT=="PRODUCTION"){
  return "https"
  }
  else{
    return "http"
  }
}

export default httpStringGen;