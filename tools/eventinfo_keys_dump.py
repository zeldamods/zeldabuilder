import byml
import wszst_yaz0
from collections import defaultdict
import typing
import yaml
import sys

data = byml.Byml(wszst_yaz0.decompress_file(sys.argv[1])).parse()

keys: typing.List[str] = list()
keys_per_mode: typing.DefaultDict[str, typing.List[str]] = defaultdict(list)

assert isinstance(data, dict)
for event in data.values():
    for key in event.keys():
        keys.append(key)
        keys_per_mode[event["mode"]].append(key)

print(yaml.dump({
    "keys": sorted(set(keys)),
    "keys_per_mode": {k: sorted(set(v)) for k, v in keys_per_mode.items()},
}, default_flow_style=False))
