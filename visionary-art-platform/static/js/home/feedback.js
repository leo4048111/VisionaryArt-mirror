import { store } from "../utils/store.js";
import { http } from "../utils/http.js";
import { common } from "../utils/common.js";

const app = Vue.createApp({
    data() {
        return {
            message: null,
            hasSubmitted: false,
            feedback_info: {
                title: null,
                tag: 'Bug report',
                contact: null,
                detail: null,
            }
        };
    },

    created() {
        Quill.prototype.getHTML = function () {
            return this.container.querySelector(".ql-editor").innerHTML;
        };

        Quill.prototype.setHTML = function (html) {
            this.container.querySelector(".ql-editor").innerHTML = html;
        };
    },

    mounted() {
        this.quill = new Quill("#editor-container", {
            modules: {
                toolbar: [
                    [{ header: [1, 2, 3, 4, false] }],
                    ["bold", "italic", "underline"],
                    ["image", "code-block", "video", "link"]
                ]
            },

            theme: "snow" // or 'bubble'
        });

        this.quill.on("text-change", () => {
            this.feedback_info.detail = this.quill.getHTML();
        });
    },

    methods: {
        getEditorContentAsHTMLString() {
            return this.quill.getHTML();
        },

        sendFeedback() {
            // // put bytes of file into form data
            // let formData = new FormData();
            // formData.append("modelfile", this.cachedFile);
            // formData.append("coverimage", this.modelCoverImage);

            // put other data into post request params
            let data = store.get_session_data();
            data['title'] = this.feedback_info.title;
            data['tag'] = this.feedback_info.tag;
            data['contact'] = this.feedback_info.contact;

            if (this.feedback_info.detail == null || this.feedback_info.detail == '') {
                alert('Please fill in the detail of your feedback.');
                return;
            }

            if (this.feedback_info.title == null || this.feedback_info.title == '') {
                alert('Please fill in the title of your feedback.');
                return;
            }

            const on_response = (response) => {
                this.hasSubmitted = true;
                console.log(response);
            }

            const on_error = (error) => {
                console.log(error);
            }

            http.post('/feedback/add', { "detail": this.feedback_info.detail }, data, on_response, on_error);
        }
    }
});

app.mount(".container");