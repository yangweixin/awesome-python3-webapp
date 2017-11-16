#!/usr/bin/python3
import asyncio
import orm
from models import User

async def test(loop):
	loop = asyncio.get_event_loop()
	await orm.create_pool(loop=loop,user='root', password='yang123456', database='awesome')

	u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

	await u.save()


loop = asyncio.get_event_loop()
loop.run_until_complete( asyncio.wait([test( loop )]) )  
loop.close()