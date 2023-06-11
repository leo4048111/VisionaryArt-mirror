import { store } from "../utils/store.js";
import { http } from "../utils/http.js";
import { SliceUploader } from "../utils/sliceuploader.js";
import { common } from "../utils/common.js";

const app = Vue.createApp({
  data() {
    return {
      fr: new FileReader(),
      hasSubmitted: false,
      cachedFile: null, // according to SRS, only one file is allowed to be uploaded at a time
      modelCoverImage: null,
      isPending: true,
      isUploading: false,
      isSuccess: false,
      isFailed: false,
      message: null,
      model_info: {
        modelname: null,
        type: 'Checkpoint',
        size: null,
        disc: null,
        version: null,
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

    this.fr.onload = function (event) {
      document.getElementById('cover-image').src = event.target.result;
    }
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
      this.model_info.disc = this.quill.getHTML();
    });

    this.$nextTick(() => {
      window.addEventListener('message', this.handleMessage)
    });
  },

  destroyed() {
    window.removeEventListener('message', this.handleMessage)
  },

  methods: {
    handleMessage(event) {
      const data = event.data;
      switch (data.cmd) {
        case 'upload-model-success':
          location.reload(true);
          break;
        default: break;
      }
    },

    getEditorContentAsHTMLString() {
      return this.quill.getHTML();
    },

    onClickModelFileBrowser(event) {
      event.preventDefault();
      document.getElementById('model-file-upload').click();
    },

    onClickCoverImageBrowser(event) {
      event.preventDefault();
      document.getElementById('cover-image-upload').click();
    },

    onDragEnter(event) {
      event.preventDefault();
    },

    onDragOver(event) {
      event.preventDefault();
    },

    resetModelFile(file) {
      this.cachedFile = file;
      if (file == null) return;
      this.isUploading = false;
      this.isSuccess = false;
      this.isFailed = false;
      this.isPending = true;
      this.model_info.size = this.cachedFile.size;
      this.model_info.modelname = common.getFileNameWithoutExt(this.cachedFile.name)
    },

    resetCoverImageFile(file) {
      this.modelCoverImage = file;
      if (file == null) return;
      this.fr.readAsDataURL(file);
    },

    onDropModelFile(event) {
      event.preventDefault();
      let file = event.dataTransfer.files[0];
      if (event.dataTransfer.files.length > 1) {
        this.message = "Multiple files dropped, ignored all but the first one.";
      }

      let extension = file.name.split('.').pop();

      if (extension !== 'safetensors' && extension !== 'ckpt') {
        this.message = "File extension not supported. Please upload a '.safetensors' or '.ckpt' file.";
        return;
      }

      this.resetModelFile(event.dataTransfer.files[0]);
    },

    onDropCoverImageFile(event) {
      event.preventDefault();
      this.resetCoverImageFile(event.dataTransfer.files[0]);
    },

    onModelFileUploadChange(event) {
      let file = event.target.files[0];
      let extension = file.name.split('.').pop();

      if (extension !== 'safetensors' && extension !== 'ckpt') {
        this.message = "File extension not supported. Please upload a '.safetensors' or '.ckpt' file.";
        return;
      }

      this.resetModelFile(event.target.files[0]);
    },

    onCoverImageUploadChange(event) {
      this.resetCoverImageFile(event.target.files[0]);
    },

    uploadModel() {
      // // put bytes of file into form data
      // let formData = new FormData();
      // formData.append("modelfile", this.cachedFile);
      // formData.append("coverimage", this.modelCoverImage);

      // put other data into post request params
      let data = store.get_session_data();
      data['modelname'] = this.model_info.modelname;
      data['type'] = this.model_info.type;
      data['size'] = this.model_info.size;
      data['disc'] = this.model_info.disc;
      data['version'] = this.model_info.version;
      this.isSuccess = false;
      this.isFailed = false;
      this.isPending = false;
      this.isUploading = true;

      if (this.cachedFile == null || this.modelCoverImage == null || this.model_info.disc == null || this.model_info.version == null) {
        alert("Please fill in all the fields!");
        return
      }

      // post message to parent window
      const x = {
        cmd: 'upload-model',
        file: this.cachedFile,
        file_cover: this.modelCoverImage,
        query_url: "/model/getchunks",
        upload_url: "/model/uploadchunks",
        params: data,
      };

      window.parent.postMessage(x, '*');
      this.hasSubmitted = true;
    },
  }
});

app.mount(".container");