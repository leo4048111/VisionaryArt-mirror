import { http } from "./http.js";
import { store } from "./store.js"

class Common {
    upload_file = null;
    upload_file_cover = null;

    redirect_to_login() {
        window.location.href = '/templates/login.html';
    }

    validate_session(callback) {
        let data = store.get_session_data();
        let isValid = true;

        if (data.uid == null || data.session_key == null) {
            isValid = false;
        }

        http.post('/user/validate_user_session', {}, data, (response) => {
            let data = response.data;

            if (data.code != 0) {
                isValid = false;
            }
        }, (error) => {
            console.log(error);
            isValid = false;
        }).then(() => {
            callback(isValid);
        });
    }

    update_user_info(callback = null) {
        let data = store.get_session_data();
        http.post('/user/get_user_info', {}, data, (response) => {
            let data = response.data;
            if (data.code == 0) {
                store.set_user_data(data.data);
            }
        }, (error) => {
            console.log(error);
        }).then(() => {
            if (callback != null)
                callback();
        });
    }

    getFileName(filePath) {
        let match = filePath.match(/[^\\/]+$/);
        return match ? match[0] : "";
    }

    getFileNameWithoutExt(filePath) {
        let fileName = this.getFileName(filePath);
        let replacedName = fileName.replace(/[\\/]/g, "_");
        let match = replacedName.match(/^[^.]+/);
        return match ? match[0] : "";
    }

    fileToBlob(file) {
        let reader = new FileReader();
        reader.addEventListener('load', (e) => {
            let base64 = e.target.result;
            let blob = new Blob([base64], { type: file.type });
        })
        reader.readAsDataURL(file)
    }
}

var common = new Common();

export { common }