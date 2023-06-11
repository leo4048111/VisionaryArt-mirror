from utils import common
import random
import string
import hashlib

db_redis = common.redis_handle()

# def genarate_access_token(string_token):
#     """生成token"""
#     access_token = hashlib.md5(string_token.encode("utf-8")).hexdigest()
#     return access_token

def genarate_session_key(length=64):
    """generate a random session key"""
    # 数字的个数随机产生
    num_of_numeric = random.randint(1, length - 1)
    # 剩下的都是字母
    num_of_letter = length - num_of_numeric
    # 随机生成数字
    numerics = [random.choice(string.digits) for _ in range(num_of_numeric)]
    # 随机生成字母
    letters = [random.choice(string.ascii_letters) for _ in range(num_of_letter)]
    # 结合两者
    all_chars = numerics + letters
    # 洗牌
    random.shuffle(all_chars)
    # 生成最终字符串
    session_key = ''.join([i for i in all_chars])
    return session_key

def find_user_session_key(uid):
    key = "session_key_{}".format(uid)
    session_key = db_redis.get(key)
    return session_key

def get_user_session_key(uid):
    """get session key"""
    session_key = common.my_str(find_user_session_key(uid))
    key = "session_key_{}".format(uid)
    if not session_key:
        session_key = genarate_session_key()
        db_redis.set(key, session_key, ex=5 * 24 * 60 * 60)
    ttl = db_redis.ttl(key)
    return session_key, ttl

def remove_user_session_key(uid):
    """remove session key"""
    key = "session_key_{}".format(uid)
    db_redis.delete(key)

def check_user_session_key(uid, session_key):
    """check session key"""
    if uid <= 0:
        return False
    check_session_key = common.my_str(find_user_session_key(uid))
    if not check_session_key:
        return False
    if session_key == check_session_key:
        return True
    return False

def generate_user_sid(uid):
    s = str(uid) + "salt:neverleakthisvalue"
    sid = hashlib.md5(s.encode("utf-8")).hexdigest()
    return sid

# # def get_user_sid(uid):
# #     """generate sid for user"""
# #     sid = find_user_sid(uid)
# #     if not sid:
# #         sid = generate_user_sid(uid)
# #     key = "user_{}".format(uid)
# #     db_redis.set(key, sid, ex=86400 * 30)
# #     return common.my_str(sid)

# # def find_user_sid(uid):
# #     key = "user_{}".format(uid)
# #     sid = db_redis.get(key)
# #     return sid

# # def check_user_sid(uid, sid):
# #     """check if user session sid is valid"""
# #     if uid <= 0:
# #         return False
# #     check_sid = common.my_str(find_user_sid(uid))
# #     if not check_sid:
# #         return False
# #     if sid == check_sid:
# #         return True
# #     return False

# def remove_user_sid(uid):
# #     key = "user_{}".format(uid)
# #     db_redis.delete(key)

def validate_user_session(uid, session_key):
    if uid <= 0:
        return False
    # result = check_user_sid(uid, sid)
    # if not result:
    #     return False
    
    result = check_user_session_key(uid, session_key)
    if not result:
        return False
    
    return True

# 