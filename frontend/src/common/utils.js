let lastPathElem = path => {
    
    const lastIndex = path.lastIndexOf('/')
    return path.substr(lastIndex+1)
};

export default {
    lastPathElem
}