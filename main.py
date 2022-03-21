import redis
from redis import Redis
from fastapi import FastAPI

import datetime
import logging

from typing import Optional

from request_models.models import PostRequestBodyModel

app = FastAPI()
redis_client: Optional[Redis] = None
logger = logging.getLogger(__name__)


@app.on_event('startup')
async def startup_event():
    global redis_client
    logger.info("Initializing redis")
    redis_client = Redis(host='localhost', port=6379, db=0)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post('/visited_links')
async def visited_links_post(links: PostRequestBodyModel):
    current_unix_time = datetime.datetime.now().timestamp()
    redis_client.hset('links', str(int(current_unix_time)), '^'.join(links.links))
    return {'status': 'ok'}


@app.get('/visited_domains')
async def visited_domains_get(from_timestamp: int | None, to: int | None):
    from_timestamp = from_timestamp if from_timestamp is not None else 0
    to = to if to is not None else datetime.datetime(year=3000, day=1, month=1).timestamp()

    all_timestamps = redis_client.hkeys('links')
    filtered_timestamps = list(filter(lambda x: from_timestamp < int(x) < to, all_timestamps))

    links = [redis_client.hget('links', timestamp) for timestamp in filtered_timestamps]


    return {'domains': str(links).split('^'),
            'status': 'ok'}
