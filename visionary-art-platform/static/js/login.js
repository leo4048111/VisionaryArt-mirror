import { common } from './utils/common.js'
import { http } from './utils/http.js'
import { store } from './utils/store.js'

const app = Vue.createApp({
    data() {
        return {
            isActive: false,
            name: '',
            password: '',
            reg_name: '',
            reg_password: '',
            status_msg: ''
        }
    },
    created() {
        common.validate_session((isValid) => {
            if (isValid) {
                window.location.href = '/templates/home.html';
            }
        });
    },
    methods:{
        login(event){
            event.preventDefault();
            const on_response = (response) => {
                let data = response.data;
                if (data.code == 0) {
                    store.set_user_data(data.data);
                }

                this.status_msg = data.msg;
                common.validate_session((isValid) => {
                    if (isValid) {
                        window.location.href = '/templates/home.html';
                    }
                });
            };

            const on_error = (error) => {
                console.log(error);
            };

            http.post('/user/login', {}, {
                name: this.name,
                password: this.password
            }, on_response, on_error);

        },

        register() {
            const on_response = (response) => {
                let data = response.data;
                this.status_msg = data.msg;
                if (this.status_msg == 'user registered successfully') {
                    this.isActive = false;
                }
            };

            const on_error = (error) => {
                alert(error.msg)
            };

            http.post('/user/register', {}, {
                name: this.reg_name,
                password: this.reg_password
            }, on_response, on_error);
        },

        onClickSignIn() {
            this.status_msg = '';
            this.isActive = false;
        },

        onClickSignUp() {
            this.status_msg = '';
            this.isActive = true;
        }
    }
});

app.mount('.container');

