# purpose: safecastの観測データをダウンロードする。
# author: Katsuhiro Morishita
# created: 2016-06-12
# license: MIT
import urllib.request
import urllib
import json
import os

# ダウンロード設定
since = '"08/05/2016 23:12:17"'
until = '"15/08/2016 23:59:38"'
device = 100222 # 100221 and 100222 are sendai station. 100112 and 100111 are yatsushiro station.


def create_dir(path_list):
	""" 指定されたパスのディレクトリを作成する
	Argv:
	    path_list   <list<str>> 作成するディレクトリ
	                    階層を要素とする。
	"""
	#print(path_list)
	dir = ""
	for men in path_list:
		dir = os.path.join(dir, men)
		#print(dir)
		if not os.path.isdir(dir):
			os.mkdir(dir)
	return dir


# 保存用のディレクトリを作る
create_dir(["data", str(device)])


# ダウンロードする。
for page in range(1500):           # データは一度にダウンロードできない。ページごとに分割されている。
	print("page: ", page)
	query = [
		('device_id', device),
		('since', since),
		('until', until),
		('page', page),
	]
	url = "https://api.safecast.org/measurements.json?" + urllib.parse.urlencode(query)
	#print(url)
	data = urllib.request.urlopen(url)
	txt = data.read()
	_json = json.loads(txt.decode())
	if len(_json) == 0:
		break
	start = _json[0]['captured_at'].replace(":", "") # ファイル内から時刻を抜き出す
	end = _json[-1]['captured_at'].replace(":", "")
	print(start, end)
	with open('data/' + str(device) + '/did{2}_{0}_{1}.json'.format(start, end, device), 'w') as f: # save
		json.dump(_json, f, sort_keys=True, indent=4)
	#print(_json)

