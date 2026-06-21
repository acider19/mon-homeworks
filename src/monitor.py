#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime


def read_loadavg():
    with open('/proc/loadavg') as f:
        parts = f.read().strip().split()
        return {
            'load_1min': float(parts[0]),
            'load_5min': float(parts[1]),
            'load_15min': float(parts[2]),
            'running': parts[3].split('/')[0],
            'total_processes': parts[3].split('/')[1],
        }


def read_meminfo():
    data = {}
    with open('/proc/meminfo') as f:
        for line in f:
            parts = line.split(':')
            if len(parts) == 2 and parts[1].strip().endswith(' kB'):
                data[parts[0].strip()] = int(parts[1].strip().split()[0])
    mem_total = data.get('MemTotal', 1)
    mem_available = data.get('MemAvailable', 0)
    return {
        'mem_used_percent': round((mem_total - mem_available) / mem_total * 100, 1),
        'mem_available_kb': mem_available,
    }


def read_disk_usage(path='/'):
    s = os.statvfs(path)
    total = s.f_frsize * s.f_blocks
    free = s.f_frsize * s.f_bfree
    used = total - free
    return {
        'disk_used_percent': round(used / total * 100, 1) if total > 0 else 0,
        'disk_total_bytes': total,
    }


def main():
    loadavg = read_loadavg()
    mem = read_meminfo()
    disk = read_disk_usage()

    log_entry = {
        'timestamp': int(time.time()),
        'load_1min': loadavg['load_1min'],
        'load_5min': loadavg['load_5min'],
        'load_15min': loadavg['load_15min'],
        'mem_used_percent': mem['mem_used_percent'],
        'disk_used_percent': disk['disk_used_percent'],
    }

    log_path = os.path.join(
        '/var/log',
        f"{datetime.now().strftime('%y-%m-%d')}-awesome-monitoring.log",
    )

    with open(log_path, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


if __name__ == '__main__':
    main()
