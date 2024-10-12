const fs = require("fs")

const BASE_URL = "http://127.0.0.1:5000/api"

const url = (path=[],vars=[]) => {
    let url = BASE_URL
    if(path.length > 0)
        for(const elem in path)
            url += `/${elem}`
    if(vars.length > 0)
        for(let i=0;i<vars.length;i++)
            url += `${i == 0 ? "?" : "&"}${vars[i][0]}=${vars[i][1]}`
}

const post = async (url,body) => {
    try {
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(body)
        }).then(res=>res.status)
        if(response.status == 201)
            return `${new Date()}; ${url}; ${response}`
    } catch (err) {
        return `${new Date()}; ${url}; 400`
    }
} 

const get = async (url) => {
    try {
        const response = await fetch(url).then(res=>res.status)
        if(response.status == 201)
            return `${new Date()}; ${url}; ${response}`
    } catch (err) {
        return `${new Date()}; ${url}; 400`
    }
} 

const init = async () => {
    const result = ""
    const errors = []
    const requests = JSON.parse(fs.readFileSync("requests.json"))
    
    for(const req of requests){
        const this_url = url(req.path,req.vars)
        try {
            if(req.body)
                result += await post(this_url, req.body) + "\n"
            else
                result += await get(this_url) + "\n"
        } catch (err) {
            console.log(err)
            errors.push({
                url: this_url,
                err: err
            })
        }
    }

    fs.writeFileSync("result.csv",result)
    fs.writeFileSync("error.json",JSON.stringify(result))
}

init()