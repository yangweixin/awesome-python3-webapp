#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Weixin Yang'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import User

@get('/')
async def index(request):
	users = await User.findAll()
	return {
		'__template__': 'test.html',
		'users': users
	}