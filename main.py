import argparse

from main_mt import (
    run_simple as mt_rs,
    run_detailed as mt_rd,
    run_wordmap as mt_rw,
    run_evaluate as mt_re,
)
from main_gc import (
    run_simple as gc_rs,
    run_detailed as gc_rd,
    run_wordmap as gc_rw,
    evaluate as gc_re,
)


def main() -> None:
    # Specify here for just `main.py`
    mt_rd()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run from main")
    parser.add_argument("-m", action="store_true", help="Select module mt")
    parser.add_argument("-g", action="store_true", help="Select module gc")
    parser.add_argument("-d", action="store_true", help="Enable detailed mode")
    parser.add_argument("-w", action="store_true", help="Enable wordmap mode")
    parser.add_argument("-e", action="store_true", help="Enable evaluation mode")
    parser.add_argument("--file", help="Input file path")
    parser.add_argument("--out", help="Output directory path")

    args = parser.parse_args()

    func = None
    if args.m:
        func = mt_rd if args.d else (mt_rw if args.w else (mt_re if args.e else mt_rs))
    elif args.g:
        func = gc_rd if args.d else (gc_rw if args.w else (gc_re if args.e else gc_rs))

    if func:
        func(args.file or "", args.out or "")
    else:
        main()
