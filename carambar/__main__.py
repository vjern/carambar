import sys
import time
import argparse

from .itqdm import tqdm


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--total', '-t', help='Total number of lines', default=None, type=int)
    parser.add_argument('--color', default=None)
    parser.add_argument('--desc', '-d', default=None)

    args = parser.parse_args()
    print(args)

    for row in tqdm(sys.stdin, total=args.total, color=args.color, leave=True, desc=args.desc):
        sys.stdout.write(row)
        sys.stdout.flush()
    