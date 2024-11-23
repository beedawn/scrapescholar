function escapeRegExp(str:string|undefined) {
    if (str ===undefined){
      return
    }
    else
    return str.replace(/[.*+?^=!:${}()|\[\]\/\\]/g, '\\$&'); // Escape special characters
  }

  export default escapeRegExp;