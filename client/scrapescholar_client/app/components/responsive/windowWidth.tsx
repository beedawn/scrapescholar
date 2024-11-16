const windowWidth = (setWidth:(item:number)=>void) => {

    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
};

export default windowWidth;