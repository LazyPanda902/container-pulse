from pathlib import Path
from types import SimpleNamespace

from container_pulse import core


def test_parse_meminfo_converts_kb():
    data = core.parse_meminfo('MemTotal: 100 kB\nMemAvailable: 25 kB\n')
    assert data['MemTotal'] == 102400
    assert data['MemAvailable'] == 25600


def test_read_loadavg(tmp_path):
    path = tmp_path / 'loadavg'
    path.write_text('0.10 0.20 0.30 1/100 1\n')
    assert core.read_loadavg(str(path)) == (0.1, 0.2, 0.3)


def test_docker_parsing():
    def fake_runner(*args, **kwargs):
        return SimpleNamespace(returncode=0, stdout='web|Up 2 hours|nginx:latest\n', stderr='')
    rows, error = core.docker_containers(fake_runner)
    assert error is None
    assert rows == [{'name': 'web', 'status': 'Up 2 hours', 'image': 'nginx:latest'}]


def test_docker_failure_is_reported():
    def fake_runner(*args, **kwargs):
        return SimpleNamespace(returncode=1, stdout='', stderr='daemon unavailable')
    rows, error = core.docker_containers(fake_runner)
    assert rows == []
    assert error == 'daemon unavailable'
