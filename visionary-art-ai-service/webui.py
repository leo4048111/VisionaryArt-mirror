import time

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import modules
from modules.ui import create_webui
from modules import shared

from initialize import initialize

def setup_middleware(app):
    # reset current middleware to allow modifying user provided list
    origins = [
        "*"
    ]

    app.middleware_stack = None
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    # app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=['*'], allow_headers=['*'])
    # app.add_middleware(CORSMiddleware, allow_origins=cmd_opts.cors_allow_origins.split(','), allow_methods=['*'], allow_credentials=True, allow_headers=['*'])
    # app.add_middleware(CORSMiddleware, allow_origin_regex=cmd_opts.cors_allow_origins_regex, allow_methods=['*'], allow_credentials=True, allow_headers=['*'])
    app.build_middleware_stack()  # rebuild middleware stack on-the-fly

def setup_routers(app):
    from utils.share_image import share_image, ImageShareResponse
    from utils.list_models import list_models, ModelListResponse
    app.add_api_route("/image/share", share_image, methods=["POST"], response_model=ImageShareResponse)
    app.add_api_route("/model/list", list_models, methods=["POST"], response_model=ModelListResponse)

def wait_on_server(webui=None):
    while 1:
        time.sleep(0.5)
        if shared.state.need_restart:
            shared.state.need_restart = False
            time.sleep(0.5)
            webui.close()
            time.sleep(0.5)
            break

def launch_webui():
    while True:
        webui = create_webui()
        app, local_url, share_url = webui.launch(
            share=False,
            show_api=False,
            server_name="0.0.0.0",
            server_port=8080,
            prevent_thread_lock=True
        )

        from utils.on_ai_service_loaded import on_ai_service_loaded
        import hashlib

        from threading import Thread

        def heart_beat_confirmation():
            while True:
                on_ai_service_loaded(local_url.split(':')[-1].split('/')[0], hashlib.sha1('visionary-art-ai-service'.encode('utf-8')).hexdigest())
                time.sleep(5)
            
        thread_heart_beat = Thread(target=heart_beat_confirmation, name="heart_beat_confirmation")
        thread_heart_beat.start()

        # app.user_middleware = [
        #     x for x in app.user_middleware if x.cls.__name__ != 'CORSMiddleware']
        setup_routers(app)
        setup_middleware(app)
        modules.progress.setup_progress_api(app)

        wait_on_server(webui)

def webui():
    initialize()
    launch_webui()

if __name__ == '__main__':
    webui()
