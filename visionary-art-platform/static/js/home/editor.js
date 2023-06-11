const editor = Vue.createApp({
    data() {
        return {
            converter: new showdown.Converter(),
            value: "#This is a description of the model\n",
            renderedHtml: null
        };
    },

    mounted() {
        this.renderedHtml = this.converter.makeHtml(this.value);
    },

    methods: {
        onchange(event) {
            this.value = event.target.value;
            this.renderedHtml = this.converter.makeHtml(this.value);
        }
    }
});

editor.mount(".container");