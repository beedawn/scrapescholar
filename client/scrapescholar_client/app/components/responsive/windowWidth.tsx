// import React, { useState, useEffect } from "react";

// const WindowWidth = () => {
//   const [width, setWidth] = useState(window.innerWidth);

//   useEffect(() => {
//     const handleResize = () => setWidth(window.innerWidth);
//     window.addEventListener("resize", handleResize);
//     return () => window.removeEventListener("resize", handleResize);
//   }, []);

//   return (
//     <div>
//       {" "}
//       <p>The width of the screen is: {width}px</p>{" "}
//     </div>
//   );
// };

// export default WindowWidth;




const windowWidth = (setWidth:(item:number)=>void) => {

    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
};

export default windowWidth;