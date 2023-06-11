const app = Vue.createApp({
    data() {
        return {
            message: 'Oops! It seems that Visionary Art backend drawing service is currently down.'
        }
    },
    methods: {
        onClick() {
            window.location.href = "/templates/login.html";
        }
    }
});

app.mount('.container');