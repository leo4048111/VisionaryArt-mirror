/*Upload huge file via file slice*/
import { http } from "./http.js";

class SliceUploader {
    progress = 0;
    #file = null;
    #file_cover = null;
    #query_url = null;
    #upload_url = null;
    #params = null;
    #fuid = null;
    #uploaded_bytes = 0;
    #chunks = new Array();  /**[{"index":index,"file":file,"size":chunk_size},{}...] */

    constructor(file/*a file object*/, file_cover/*a file object*/, query_url, upload_url, params) {
        this.#file = file;
        this.#file_cover = file_cover;
        this.#query_url = query_url;
        this.#upload_url = upload_url;
        this.#params = params;
    }

    BeginUpload(on_upload_success, on_upload_error) {
        const on_error = (error) => {
            on_upload_error(error);
        }

        /**Loop uploading chunks */
        const on_got_chunks = () => {
            var index = this.#FindUnUploadedChunk();
            //on_upload_progress(this.#uploaded_bytes, this.#file.size)
            this.#PostOneChunk(index, on_got_chunks, on_error)
            if (index == -1) {
                if (this.#uploaded_bytes == this.#file.size)
                    on_upload_success();
                else on_upload_error();
            }
        }

        this.#GetSliceFromServer(on_got_chunks, on_error);
    }

    GetProgress() {
        return this.progress.toFixed(1);
    }

    /*Get file slice chunks from server */
    #GetSliceFromServer(on_got_chunks, on_upload_error) {
        const on_response = (response) => {
            let data = response.data;
            let file_data = data.data;
            if (data.code == 0) {
                this.#fuid = file_data.fuid;                /**A fuid for file */
                this.#ParseSliceChunks(file_data.chunks);  /**Get all chunks */
                on_got_chunks();
            }
            else {
                on_upload_error(data.code);
            }
        }

        const on_error = (error) => {
            on_upload_error(error);
        }

        let formData = new FormData();
        formData.append("filename", this.#file.name);
        formData.append("filesize", this.#file.size);
        http.post(this.#query_url, formData, this.#params, on_response, on_error);
    }

    /**Parse response */
    #ParseSliceChunks(chunks_array) {
        let expected_byte_cnt = 0;
        for (let i = 0; i < chunks_array.length; i++) {
            let fr = -1;
            let to = -1;
            /* Check wether chunk has been transfered */
            if (chunks_array[i].chunk_size != chunks_array[i].uploaded_size)
                fr = expected_byte_cnt;

            expected_byte_cnt += chunks_array[i].chunk_size;
            to = expected_byte_cnt;

            this.#uploaded_bytes += chunks_array[i].uploaded_size;
            let chunk = { "index": i, "from": fr, "to": to };
            this.#chunks[i] = chunk;
        }
    }

    /**Upload one slice chunk to server */
    #PostOneChunk(index, on_got_chunks, on_upload_error) {
        const on_response = (response) => {
            //let data = response.data;
            this.#uploaded_bytes += (this.#chunks[index].to - this.#chunks[index].from);
            this.#chunks[index].from = -1;
            this.#chunks[index].to = -1;
            console.log("upload " + index + " is ok...")
            /**Upload next chunk */
            if (index != -1)
                on_got_chunks();
        }

        const on_error = (error) => {
            on_upload_error(error);
        }

        let formData = new FormData();
        formData.append("fuid", this.#fuid);
        formData.append("chunk_index", index);

        //formData.append("size", this.#chunks[index].to - this.#chunks[index].from);
        if (index != -1) {
            let fs = this.#file.slice(this.#chunks[index].from, this.#chunks[index].to);
            formData.append("file", fs);
            formData.append("pos", this.#chunks[index].from);
            formData.append("type", this.#params.type);
        }
        else
            formData.append("coverimage", this.#file_cover);

        if (index == -1)
            http.post(this.#upload_url, formData, this.#params, on_response, on_error);
        else
            http.post(this.#upload_url, formData, { uid: this.#params.uid, session_key: this.#params.session_key }, on_response, on_error);
    }

    /**Get an un-transfered chunk */
    #FindUnUploadedChunk() {
        let index = -1;
        for (var i = 0; i < this.#chunks.length; i++) {
            if (this.#chunks[i].from != -1 && this.#chunks[i].to != -1) {
                index = i;
                break;
            }
        }
        this.progress = this.#uploaded_bytes * 100.0 / this.#file.size;
        return index;
    }
}

export { SliceUploader }
