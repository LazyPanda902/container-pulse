from __future__ import annotations

import argparse
import json

from .core import collect_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='container-pulse',
        description='Collect a read-only Linux host and Docker snapshot.',
    )
    parser.add_argument('--path', default='/', help='filesystem path to measure')
    parser.add_argument('--no-docker', action='store_true', help='skip docker ps')
    parser.add_argument('--json', action='store_true', help='emit JSON')
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    data = collect_snapshot(args.path, not args.no_docker)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"load={data['load']}")
        print(f"memory_available={data['memory']['available_bytes']}")
        print(f"disk_free={data['disk']['free_bytes']}")
        print(f"docker_running={data['docker']['running_count']}")
        if data['docker']['error']:
            print(f"docker_error={data['docker']['error']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
