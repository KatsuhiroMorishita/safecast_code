# purpose: ダウンロードしたsafecastの観測データをcsv形式に変換する。
# author: Katsuhiro Morishita
# created: 2016-06-12
# license: MIT
import json
import glob
from datetime import datetime as dt

keys = ["captured_at", "channel_id", "device_id", "devicetype_id", "height", "id", "latitude", "location_name", "longitude", "original_id", "sensor_id", "station_id", "unit", "user_id", "value"]

files = glob.glob("*.json")
print(files)


data = []
for fpath in files:
	f = open(fpath, 'r')
	_json = json.load(f)
	f.close()
	for j in _json:
		mem = []
		for key in keys:
			if key == "captured_at":     # 時刻をExcelが処理できるフォーマットに変換する。
				t = j[key].split(".")[0] # "2016-08-13T11:51:21.000Z".split(".")[0]
				t = t.replace("Z", "")   # たまに、Zがついている。
				print(t)
				tdatetime = dt.strptime(t, '%Y-%m-%dT%H:%M:%S') # "2016-08-13T11:51:21"
				mem.append(tdatetime)
			else:
				mem.append(j[key])
		mem = [str(x) for x in mem]
		data.append(",".join(mem))

with open("save.csv", "w") as fw:
	fw.write(",".join(keys))
	fw.write("\n")
	fw.write("\n".join(data))

