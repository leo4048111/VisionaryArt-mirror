import { store } from "../utils/store.js";
import { http } from "../utils/http.js";

const app = Vue.createApp({
  data() {
    return {
      user_name: "testuser",
      user_files: []
    }
  },

  created() {
    let name = store.get_user_name();
    if (name != null)
      this.user_name = name;
    else this.user_name = "testuser";
  },

  mounted() {
    $(document).ready(function () {
      $("a#pageLink").click(function () {
        $("a#pageLink").removeClass("active");
        $(this).addClass("active");
      });
    });

    $('.main-area').scroll(function () {
      if ($('.main-area').scrollTop() >= 88) {
        $('div.main-area-header').addClass('fixed');
      }
      else {
        $('div.main-area-header').removeClass('fixed');
      }
    });

    this.get_user_files();
  },

  methods: {
    get_user_files() {
      let uploader_uid = store.get_user_info('uid');
      let data = store.get_session_data();
      data["uploader_uid"] = uploader_uid;
      const on_response = (response) => {
        let data = response.data;
        this.user_files = data.data;
      };

      const on_error = (error) => {
        console.log(error);
      };

      http.post('/search/model', {}, data, on_response, on_error);
    },

    deleteUserFile(index) {
      let data = store.get_session_data();
      data["mid"] = this.user_files[index]["id"];

      const on_response = (response) => {
        console.log(response);
        this.get_user_files();
      };

      const on_error = (error) => {
        console.log(error);
      };

      http.post('/model/remove', {}, data, on_response, on_error);
    }
  }
});

app.mount('.app-container');

