import { cookie } from "./cookie.js";

class Store
{
    constructor() {

    }

    set_cookie(json, days) {
        cookie.setCookie(json, days);
    }

    get_cookie(name) {
        return cookie.getCookie(name);
    }

    clear_cookie(name) {
        cookie.clearCookie(name);
    }

    set_user_data(data) {
        this.set_cookie(data, 0.1);
    }

    get_session_data() {
        let data = {
            uid: this.get_cookie('uid'),
            session_key: this.get_cookie('session_key')
        };

        return data;
    }

    get_user_avatar() {
        return this.get_cookie('avatar');
    }
    
    get_user_name() {
        return this.get_cookie('name');
    }

    get_user_info(str) {
        return this.get_cookie(str);
    }
}

var store = new Store();

export { store };