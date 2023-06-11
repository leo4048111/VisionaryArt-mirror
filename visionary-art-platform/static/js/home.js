import { common } from "./utils/common.js"
import { store } from "./utils/store.js"
import { http } from "./utils/http.js"
import { SliceUploader } from "./utils/sliceuploader.js";

const app = Vue.createApp({
  data() {
    return {
      main_area_frame_src: "/templates/home/browse.html",
      left_nav_isActive: [
        true, false, false, false, false, false
      ],
      user_avatar: store.get_user_avatar(),
      user_avatar_file: null,
      ai_service_port: 0,
      upload_tasks: [],
    }
  },

  created() {
    common.validate_session((isValid) => {
      if (!isValid) {
        window.location.href = '/templates/login.html';
      }
    });

    this.user_avatar = store.get_user_avatar();
  },

  mounted() {
    $('.main-area').scroll(function () {
      if ($('.main-area').scrollTop() >= 88) {
        $('div.main-area-header').addClass('fixed');
      }
      else {
        $('div.main-area-header').removeClass('fixed');
      }
    });

    this.$nextTick(() => {
      window.addEventListener('message', this.handleMessage)
    });

    this.timer = setInterval(this.updateAllProgress, 500);
  },

  methods: {
    main_frame_navigate_to(index, src) {
      this.main_area_frame_src = src;
      for (let i = 0; i < this.left_nav_isActive.length; i++) {
        this.left_nav_isActive[i] = false;
      }

      this.left_nav_isActive[index] = true;
    },

    logout() {
      const on_response = (response) => {
        let data = response.data;
        if (data.code == 0) {
          store.clear_cookie('uid');
          store.clear_cookie('session_key');
          common.redirect_to_login();
        } else common.validate_session((isValid) => {
          if (!isValid) common.redirect_to_login();
        });
      };

      const on_error = (error) => {
        console.log(error);
      };

      http.post('/user/logout', {}, store.get_session_data(), on_response, on_error);
    },

    onClickUserAvatar(event) {
      event.preventDefault();
      document.getElementById('user-avatar-uploader').click();
    },

    onUploadAvatarChange(event) {
      this.user_avatar_file = event.target.files[0];
      this.uploadUserAvatar();
    },

    uploadUserAvatar() {
      if (this.user_avatar_file == null) return;

      let formData = new FormData();
      formData.append("avatarFile", this.user_avatar_file);

      const on_response = (response) => {
        console.log(response);
        common.update_user_info(() => {
          this.user_avatar = store.get_user_avatar();
        })
      };

      const on_error = (error) => {
        console.log(error);
      };

      http.post('/user/update_user_avatar', formData, store.get_session_data(), on_response, on_error);
    },

    navigateToAiService() {
      const on_response = (response) => {
        let port = response.data.data.port;
        if (port == 0) this.main_frame_navigate_to(4, '/templates/404.html');
        else {
          let x = window.location.protocol + '//' + window.location.hostname + ':' + port;
          this.main_frame_navigate_to(4, x);
        }
      };

      const on_error = (error) => {
        console.log(error);
      };

      http.post('/get_ai_service_port', {}, store.get_session_data(), on_response, on_error);
    },

    upload_model(file, file_cover, query_url, upload_url, params) {
      const on_response = (response) => {
        let data = response.data;
        if (data.code == 0) {
          console.log("upload success");
        }
      };

      const on_error = (error) => {
        console.log("request error...");
      };

      const on_slice_upload_success = () => {
        console.log("slice upload success...");
      };

      if (file.size < 10 * 1024 * 1024) {
        // put bytes of file into form data
        let formData = new FormData();
        formData.append("modelfile", file);
        formData.append("coverimage", file_cover);
        http.post("/model/upload", formData, params, on_response, on_error);
        this.upload_tasks.push({ "params": params, "uploader": null, "progress": 100 })
      }
      else {
        let uploader = new SliceUploader(file, file_cover, query_url, upload_url, params);
        this.upload_tasks.push({ "params": params, "uploader": uploader, "progress": uploader.GetProgress() });
        uploader.BeginUpload(on_slice_upload_success, on_error);
      }
    },

    handleMessage(event) {
      const data = event.data;
      switch (data.cmd) {
        case 'upload-model':
          this.upload_model(data.file, data.file_cover, data.query_url, data.upload_url, data.params);
          break;
        case 'get-session-data':
          event.source.postMessage({
            cmd: 'session-data',
            data: store.get_session_data()
          }, event.origin);
          break;
        default: break;
      }
    },

    updateAllProgress() {
      for (let i = 0; i < this.upload_tasks.length; i++) {
        let task = this.upload_tasks[i];
        if (task.uploader != null) {
          let x = task.uploader.GetProgress();
          if (x == 100 && task.progress != 100) {
            const data = {
              cmd: 'upload-model-success',
            }
            document.getElementById('main-frame').contentWindow.postMessage(data, '*');
          }
          task.progress = x;
        }

      }
    }
  }
});

app.mount('.app-container');

