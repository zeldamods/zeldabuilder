# Copyright 2019 leoetlino <leo@leolam.fr>
# Licensed under GPLv2+

import argparse
from pathlib import Path

from zeldabuilder.build import build
from zeldabuilder.unbuild import unbuild

def main() -> None:
    parser = argparse.ArgumentParser("zeldabuilder")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    subparsers.required = True

    build_parser = subparsers.add_parser("build", description="")
    build_parser.set_defaults(func=build)

    unbuild_parser = subparsers.add_parser("unbuild", description="")
    unbuild_parser.add_argument("src_rom_dir", help="ROM directory")
    unbuild_parser.add_argument("dest_dir", help="Destination directory")
    unbuild_parser.add_argument("--platform", help="ROM platform", choices=["cafe", "nx"], required=True)
    unbuild_parser.add_argument("--aoc-dir", help="DLC/AoC directory (romfs for Switch or 0010 for Wii U)")
    unbuild_parser.set_defaults(func=lambda a:
        unbuild(src_rom_dir=Path(a.src_rom_dir),
                dest_dir=Path(a.dest_dir),
                platform=a.platform,
                aoc_dir=Path(a.aoc_dir) if a.aoc_dir else None,
                ))

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
