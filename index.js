const fs = require("fs")

const BASE_URL = "http://127.0.0.1:5000/api"

const url = (path,vars) => {
    let url = BASE_URL
    if(path.length > 0)
        for(const elem of path)
            url += `/${elem}`
    if(vars.length > 0)
        for(let i=0;i<vars.length;i++)
            url += `${i == 0 ? "?" : "&"}${vars[i][0]}=${vars[i][1]}`
    return url
}

const post = async (url,body) => {
    try {
        console.log(body)
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })
        return `${new Date()}; ${url}; ${response.status}`
    } catch (err) {
        return `${new Date()}; ${url}; 400`
    }
} 

const get = async (url) => {
    try {
        const response = await fetch(url)
        return `${new Date()}; ${url}; ${response.status}`
    } catch (err) {
        return `${new Date()}; ${url}; 400`
    }
} 

const init = async () => {
    let result = ""
    const errors = []
    const requests = JSON.parse(fs.readFileSync("requests.json"))

    for(const req of requests){
        const this_url = url(req.path,req.vars)
        console.log(this_url)
        try {
            if(req.body){
                const postReq = await post(this_url, req.body)
                result += postReq + "\n"
            } else {
                const getReq = await get(this_url)
                result += getReq + "\n"
            }
        } catch (err) {
            console.log(err)
            errors.push({
                url: this_url,
                err: err
            })
        }
    }

    fs.writeFileSync("result.csv",result)
    fs.writeFileSync("error.json",JSON.stringify(errors))
}

init()