urls = [
    ('/', 'handlers.static.home_page.Handle'),
    ('/user/logout', 'handlers.user.logout_user.Handle'),
    ('/user/validate_user_session', 'handlers.user.validate_user_session.Handle'),
    ('/user/register', 'handlers.user.register_user.Handle'),
    ('/user/get_user_info', 'handlers.user.get_user_info.Handle'),
    ('/user/login', 'handlers.user.login_user.Handle'),
    ('/user/modify_user', 'handlers.user.modify_user.Handle'),
    ('/user/update_user_avatar', 'handlers.user.update_user_avatar.Handle'),
    ('/model/remove','handlers.model.remove_model.Handle'),
    ('/model/upload', 'handlers.model.model_upload.Handle'),
    ('/search/user', 'handlers.search.search_user.Handle'),
    ('/search/model', 'handlers.search.search_model.Handle'),
    # ('/api/text2image', 'handlers.api.text2image.Handle'),
    #cx_test
    ('/model/like', 'handlers.model.model_like.Handle'),
    ('/model/if_user_like_model', 'handlers.model.if_user_like_model.Handle'),
    ('/comment/add', 'handlers.comment.comment_add.Handle'),
    ('/comment/remove', 'handlers.comment.comment_remove.Handle'),
    ('/comment/search', 'handlers.comment.comment_search.Handle'),
    ('/image/share', 'handlers.image.image_share.Handle'),
    ('/image/get', 'handlers.image.image_get.Handle'),
    #For chunk uploading handler
    ('/model/getchunks', 'handlers.model.model_getchunks.Handle'),
    ('/model/uploadchunks', 'handlers.model.model_uploadchunks.Handle'),
    ('/model/list', 'handlers.model.model_list.Handle'),
    # on ai service loaded, get service port
    ('/on_ai_service_loaded', 'handlers.auth.on_ai_service_loaded.Handle'),
    ('/get_ai_service_port', 'handlers.auth.get_ai_service_port.Handle'),
    ('/feedback/add', 'handlers.feedback.feedback_add.Handle'),
]
#lyt
#lyr-bygui
#lqt-测试
#zsr-IAM账号测试
#jjj