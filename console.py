#!/usr/bin/env python3
__author__ = 'Fabian'
import argparse
from multiprocessing import cpu_count, freeze_support

if __name__ == "__main__":
    freeze_support()
    parser = argparse.ArgumentParser(description='Stress CPU over a time, in the form of a rectangle function.')
    parser.add_argument('-f', '--frequency', type=int, dest="freq", default=10,
                       help='CPU stress frequency.')
    parser.add_argument('time', type=int, default=60,
                       help='Total test time in seconds.')
    parser.add_argument('-w', '--worker_count', type=int, default=cpu_count(),
                        dest="workers",
                       help='Amount of workers to run, to target a cpu core each.')
    import sys
    if len(sys.argv) <2:
        parser.print_help()
        print()
    args = parser.parse_args()


    import ticker
    from shared import Settings
    settings = Settings(args.time, 1.0/args.freq, args.workers)
    ticker.test(settings, lambda data:1)
