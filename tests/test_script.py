import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('exit_code', type=int)
    args = parser.parse_args()
    sys.exit(args.exit_code)
