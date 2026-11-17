from concurrent.futures import ProcessPoolExecutor
from collections import Counter
from multiprocessing import get_context
import os


def map_partition(rows):
    counts = Counter()
    minutes = Counter()
    for faculty, room, start, end in rows:
        key = (faculty, room)
        counts[key] += 1
        minutes[key] += end - start
    return counts, minutes, os.getpid()


def report(rows):
    if not rows:
        return {"particiones": 0, "procesos": [], "grupos": []}
    size = min(2, len(rows))
    # Separate single-process pools guarantee distinct OS processes for the partitions.
    pools = []
    try:
        jobs = []
        for i in range(size):
            pool = ProcessPoolExecutor(1, mp_context=get_context("spawn"))
            pools.append(pool)
            jobs.append(pool.submit(map_partition, rows[i::size]))
        counts, minutes, pids = Counter(), Counter(), []
        for job in jobs:
            c, m, pid = job.result()
            counts.update(c)
            minutes.update(m)
            pids.append(pid)
        groups = [{"facultad": f, "sala": s, "reservas": n,
                   "minutos": minutes[f, s]} for (f, s), n in sorted(counts.items())]
        return {"particiones": size, "procesos": pids, "grupos": groups}
    finally:
        for pool in pools:
            pool.shutdown()
