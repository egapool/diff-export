#!/usr/local/bin/python3

# http://d.hatena.ne.jp/mrgoofy33/20101214/1292339820

import subprocess
from datetime import datetime
import os
import sys
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ver1", 
					nargs='?',
					default="head",
                    help="Branch Name,Commit Id or ...",
                    type=str)
parser.add_argument("ver2", 
					nargs='?',
                    default=argparse.SUPPRESS,
                    help="Branch Name,Commit Id or ...",
                    type=str)
parser.add_argument("-d",
					help="Directory path where you want to create date folder",
					nargs='?',
					type=str
					)
arguments = parser.parse_args()

base_dir = os.path.dirname(os.path.abspath(__file__))

# make dist dir
dist_dir = base_dir+'/export/'+datetime.now().strftime('%Y%m%d_%H%M%S')

if not arguments.d == None:
	dist_dir += '/'+arguments.d

os.makedirs(dist_dir)

cmd = ['git','diff','--name-only',arguments.ver1]
if 'ver2' in arguments:
	cmd.append(arguments.ver2)

out = subprocess.run(cmd, stdout=subprocess.PIPE)
files = out.stdout.decode().split("\n")
for f in files:

	if f == '':
		continue

	d = os.path.dirname(f)

	src = base_dir+'/'+f
	dist = dist_dir+'/'+f

	# fileが存在しない、現行バージョンで消えているので不要
	if not os.path.exists(src):
		continue

	# distの各ディレクトリ作成
	if not os.path.exists(dist_dir+'/'+d):
		os.makedirs(dist_dir+'/'+d)

	shutil.copyfile(src,dist)

print("[SUCCESS] Created \""+dist_dir+"\"")
