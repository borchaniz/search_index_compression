import json

from DiskIO import DiskIO

with open('index_one.json') as f:
    data = json.load(f)
disk_io = DiskIO()
disk_io.write(data, 'output')
print(data == disk_io.read_and_decompress('output'))
data = disk_io.read('output')
print(disk_io.decompress(data[list(data.keys())[0]]))
