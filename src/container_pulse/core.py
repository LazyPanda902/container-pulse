from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable


def parse_meminfo(text: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for line in text.splitlines():
        if ':' not in line:
            continue
        key, raw = line.split(':', 1)
        parts = raw.strip().split()
        if not parts:
            continue
        try:
            value = int(parts[0])
        except ValueError:
            continue
        if len(parts) > 1 and parts[1].lower() == 'kb':
            value *= 1024
        result[key] = value
    return result


def read_loadavg(path: str = '/proc/loadavg') -> tuple[float, float, float]:
    first = Path(path).read_text(encoding='utf-8').split()[:3]
    if len(first) != 3:
        raise ValueError('loadavg does not contain three load values')
    return tuple(float(v) for v in first)  # type: ignore[return-value]


def docker_containers(runner: Callable[..., Any] = subprocess.run) -> tuple[list[dict[str, str]], str | None]:
    try:
        result = runner(
            ['docker', 'ps', '--format', '{{.Names}}|{{.Status}}|{{.Image}}'],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [], str(exc)

    if result.returncode != 0:
        return [], (result.stderr or result.stdout or 'docker ps failed').strip()

    rows: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split('|', 2)
        if len(parts) == 3:
            rows.append({'name': parts[0], 'status': parts[1], 'image': parts[2]})
    return rows, None


def collect_snapshot(path: str = '/', include_docker: bool = True) -> dict[str, Any]:
    mem = parse_meminfo(Path('/proc/meminfo').read_text(encoding='utf-8'))
    disk = shutil.disk_usage(path)
    containers, docker_error = docker_containers() if include_docker else ([], None)
    return {
        'load': read_loadavg(),
        'memory': {
            'total_bytes': mem.get('MemTotal'),
            'available_bytes': mem.get('MemAvailable'),
        },
        'disk': {
            'path': path,
            'total_bytes': disk.total,
            'used_bytes': disk.used,
            'free_bytes': disk.free,
        },
        'docker': {
            'checked': include_docker,
            'running_count': len(containers),
            'containers': containers,
            'error': docker_error,
        },
    }
