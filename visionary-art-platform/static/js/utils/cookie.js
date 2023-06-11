class Cookie {
    setCookie(json, days) {
        let data = new Date(
            new Date().getTime() + days * 24 * 60 * 60 * 1000
        ).toUTCString();

        for (var key in json) {
            document.cookie = key + "=" + json[key] + "; expires=" + data;
        }
    }

    getCookie(name) {
        var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
        if (arr != null) {
            return unescape(arr[2])
        } else {
            return null
        }
    }

    clearCookie(name) {
        let json = {};
        json[name] = '';
        this.setCookie(json, -1)
    }
};

var cookie = new Cookie();

export { cookie }
