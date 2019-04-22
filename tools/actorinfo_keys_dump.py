import byml
import wszst_yaz0
from collections import defaultdict
import typing
import yaml
import sys

data = byml.Byml(wszst_yaz0.decompress_file(sys.argv[1])).parse()

keys: typing.List[str] = list()
keys_per_profile: typing.DefaultDict[str, typing.List[str]] = defaultdict(list)

assert isinstance(data, dict)
for actor in data["Actors"]:
    for key in actor.keys():
        keys.append(key)
        keys_per_profile[actor["profile"]].append(key)

profiles_per_key: typing.DefaultDict[str, typing.Set[str]] = defaultdict(set)
for profile, profile_keys in keys_per_profile.items():
    for key in profile_keys:
        profiles_per_key[key].add(profile)

print(yaml.dump({
    "keys": sorted(set(keys)),
    "keys_per_profile": {k: sorted(set(v)) for k, v in keys_per_profile.items()},
    "profiles_per_key": {k: sorted(profiles_per_key[k]) for k in sorted(profiles_per_key.keys())},
}, default_flow_style=False))
