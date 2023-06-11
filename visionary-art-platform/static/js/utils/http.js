class HTTPRequest
{
    async get(url, data, on_response, on_error)
    {
        await axios.get(url, {
            params: data
        }).then(on_response).catch(on_error);
    }

    async post(url, data, param_data, on_response, on_error) {
        await axios.post(url, data, {
            params: param_data,
        }).then(on_response).catch(on_error);
    }
}

var http = new HTTPRequest();

export {http}