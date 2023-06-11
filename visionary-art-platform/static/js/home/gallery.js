import { store } from "../utils/store.js"
import { http } from "../utils/http.js"

const app = Vue.createApp({
    data() {
        return {
            imageInfos: []
        };
    },

    mounted() {
        this.getImages();
        window.onscroll = this.onScroll;
    },

    methods: {
        getImages(count = 9) {
            let data = store.get_session_data();
            data["count"] = count;
            const on_response = (response) => {
                this.imageInfos.push(...response.data.data);
            };

            const on_error = (error) => {
                console.log(error);
            };

            http.post('/image/get', {}, data, on_response, on_error);
        },

        onClickImage(imageInfo) {
            $(".modal-body").html("<img src='" + imageInfo.path + "' class='modal-img'>");
            $(".modal-info").html(imageInfo.generation_info_html);
            $("#myModal").modal();
        },

        onScroll() {
            const scrollHeight = document.documentElement.scrollHeight;
            const scrollTop = document.documentElement.scrollTop;
            const clientHeight = document.documentElement.clientHeight;
            if (scrollTop + clientHeight >= scrollHeight) {
                console.log("at bottom");
                this.getImages(9);
            }
        },
    },
});

app.mount(".container")

