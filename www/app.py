#!/usr/bin/python3

__author__='Yang Weixin'

import logging
logging.basicConfig(level=logging.INFO)
import asnycio,os,json,time
from datetime import datetime

from aiohttp import web

def index(request):
	return web.Response(body=b'<h1>Awesome</h1>')

async def init(loop):
	app = web.Application(loop=loop)
	app.router.add_route('GET','/',index)
	srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
	loggin.info('server started at http://127.0.0.1:9000')
	return srv

loop = asycio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

