#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

import os, sys, time, subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def log(s):
    print('[Monitor] %s' % s)


class MyFileSystemEventHandler(FileSystemEventHandler):

	def __init__(self, func):
		super(MyFileSystemEventHandler, self).__init__()
		self.callback = func

	def on_any_event(self, event):
		print('---->')
		if event.src_path.endswith('.py'):
			log('Python source file changed: %s' % event.src_path)
			self.callback()

command = ['echo', 'ok']
process = None

def start_process():
	global command, process
	log('Start process %s...' % ' '.join(command))
	process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout,stderr=sys.stderr)

def kill_process():
	global process
	if process:
		log('Kill process [%s]...' % process.pid)
		process.kill()
		process.wait()
		log('Process ended with status %s.' % process.returncode)
		process = None

def restart_process():
	kill_process()
	start_process()


def start_watch(path, callback):
	observer = Observer()
	observer.schedule(MyFileSystemEventHandler(restart_process), path, recursive=True)
	observer.start()
	start_process()
	try:
		while(True):
			time.sleep(0.5)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

if __name__ == '__main__':
	argv = sys.argv[1:]
	if not argv:
		print('Usage: ./pymonitor.py your-script.py')
		exit(0)
	if argv[0] != 'python':
		argv.insert(0, 'python')
	command = argv
	path = os.path.abspath('.')
	start_watch(path, restart_process)


