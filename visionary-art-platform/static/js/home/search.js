import { store } from "../utils/store.js"
import { http } from "../utils/http.js"

const app = Vue.createApp({
    data() {
        return {
            isFocused: false,
            isSearching: false,
            hasSearched: false,
            isCheckingDetail: false,
            isModelCommentsLoading: false,
            searchType: 0,
            searchText: null,
            modelSearchResults: [],
            userSearchResults: [],
            totalPages: 1,
            curPage: 1,
            searchResultSliceIndex: [],
            curModelDetailIndex: 0,
            newUserCommentText: null,
            modelComments: [],
        }
    },

    mounted() {

    },

    methods: {
        handleFocus() {
            this.isFocused = true;
        },

        handleBlur() {
            this.isFocused = false;
        },

        handleEnter(event) {
            event.preventDefault();
            this.search(parseInt(this.searchType));
        },

        searchModel() {
            this.isSearching = true;
            let search_model_name = this.searchText;
            let data = store.get_session_data();
            data["modelname"] = search_model_name;
            const on_response = (response) => {
                this.isSearching = false;
                let data = response.data;
                this.modelSearchResults = data.data;
                for (let i = 0; i < this.modelSearchResults.length; i++)
                    this.updateModelLikedStatus(i);
            };

            const on_error = (error) => {
                console.log(error);
                this.isSearching = false;
            };

            http.post('/search/model', {}, data, on_response, on_error);
        },

        searchUser() {
            this.isSearching = true;
            let search_name = this.searchText;
            let data = store.get_session_data();
            data["search_name"] = search_name;
            const on_response = (response) => {
                let data = response.data;
                this.userSearchResults = data.data;
                this.isSearching = false;
            };

            const on_error = (error) => {
                console.log(error);
                this.isSearching = false;
            };

            http.post('/search/user', {}, data, on_response, on_error);
        },

        searchTrending() {
            this.isSearching = true;
            let data = store.get_session_data();
            data["trending"] = 10;
            const on_response = (response) => {
                this.isSearching = false;
                let data = response.data;
                this.modelSearchResults = data.data;
                for (let i = 0; i < this.modelSearchResults.length; i++)
                    this.updateModelLikedStatus(i);
            };

            const on_error = (error) => {
                console.log(error);
                this.isSearching = false;
            };

            http.post('/search/model', {}, data, on_response, on_error);
        },

        searchLiked() {
            this.isSearching = true;
            let data = store.get_session_data();
            data["liked"] = 1;
            const on_response = (response) => {
                this.isSearching = false;
                let data = response.data;
                this.modelSearchResults = data.data;
                for (let i = 0; i < this.modelSearchResults.length; i++)
                    this.updateModelLikedStatus(i);
            };

            const on_error = (error) => {
                console.log(error);
                this.isSearching = false;
            };

            http.post('/search/model', {}, data, on_response, on_error);
        },

        search(type) {
            this.hasSearched = true;

            switch (type) {
                case 0:
                    this.searchModel();
                    break;
                case 1:
                    this.searchUser();
                    break;
                case 2:
                    this.searchTrending();
                    break;
                case 3: 
                    this.searchLiked();
                    break;
            }
        },

        slide(offset) {
            let index = curPage[parseInt(searchType)];
            let total = totalPages[parseInt(searchType)];
            index = Math.min(Math.max(index + offset, 0), total - 1);
            var pr = document.querySelector('.paginate.left');
            var pl = document.querySelector('.paginate.right');
            pr.setAttribute('data-state', index === 0 ? 'disabled' : '');
            pl.setAttribute('data-state', index === total - 1 ? 'disabled' : '');

            curPage[parseInt(searchType)] = index;
            searchResultSliceIndex[parseInt(searchType)] = index * 10;
        },

        getModelDetails(index) {
            this.isCheckingDetail = true;
            this.isModelCommentsLoading = true;
            this.curModelDetailIndex = index;
            let model = this.modelSearchResults[index];
            let data = store.get_session_data();
            data["mid"] = model.id;
            this.curModelDisc = model.disc;
            const on_response = (response) => {
                let data = response.data;
                this.modelSearchResults[index]['comments'] = data.data;
                this.isModelCommentsLoading = false;
            };

            const on_error = (error) => {
                console.log(error);
            };

            http.post('/comment/search', {}, data, on_response, on_error);
        },

        updateModelLikedStatus(index) {
            let model = this.modelSearchResults[index];
            let data = store.get_session_data();
            data["mid"] = model.id;
            const on_response = (response) => {
                let data = response.data;
                this.modelSearchResults[index]['is_model_liked'] = data.data['is_model_liked'];
                this.modelSearchResults[index]['liked'] = data.data['liked'];
            };

            const on_error = (error) => {
                console.log(error);
            };

            http.post('/model/if_user_like_model', {}, data, on_response, on_error);
        },

        likeModel(index) {
            let model = this.modelSearchResults[index];
            let data = store.get_session_data();
            data["mid"] = model.id;
            const on_response = (response) => {
                this.updateModelLikedStatus(index);
                console.log(response);
            };

            const on_error = (error) => {
                console.log(error);
            };

            http.post('/model/like', {}, data, on_response, on_error);
        },

        downloadModel(index) {
            let model = this.modelSearchResults[index];
            let url = model.url;
            let extension = '.' + url.substring(url.lastIndexOf(".") + 1, url.length);
            const x = document.createElement('a');
            const body = document.querySelector('body');
            x.href = url
            x.download = model.modelname + extension;
            x.style.display = 'none';
            body.appendChild(x);
            x.click();
            body.removeChild(x);
        },

        addComment() {
            let model = this.modelSearchResults[this.curModelDetailIndex];
            let mid = model.id;
            let data = store.get_session_data();
            data["mid"] = mid;
            data["content"] = this.newUserCommentText;
            const on_response = (response) => {
                this.newUserCommentText = "";
                this.getModelDetails(this.curModelDetailIndex);
                console.log(response);
            };

            const on_error = (error) => {
                console.log(error);
            };

            http.post('/comment/add', {}, data, on_response, on_error);
        },
    },

    directives: {
        drag(el, bindings) {
            el.onmousedown = function (e) {
                var disx = e.clientX - el.offsetLeft;
                var disy = e.clientY - el.offsetTop;
                el.style.cursor = 'move';
                document.onmousemove = function (e) {
                    el.style.left = e.clientX - disx + 'px';
                    el.style.top = e.clientY - disy + 'px';
                }
                document.onmouseup = function () {
                    document.onmousemove = document.onmouseup = null;
                    el.style.cursor = 'default';
                }
            }
        }
    }
});

app.mount(".container");