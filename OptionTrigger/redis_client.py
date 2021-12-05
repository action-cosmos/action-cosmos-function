import os
import redis

def redis_client():
    r = redis.Redis(host=os.getenv('redis_host'), socket_timeout=3,
                    port=os.getenv('redis_port'), db=0,password=os.getenv('redis_password'), ssl=True)

    return r
