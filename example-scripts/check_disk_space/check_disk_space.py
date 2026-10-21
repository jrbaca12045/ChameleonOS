import shutil
import sys
import io
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def main():
    parser = argparse.ArgumentParser(description="Report disk usage for a drive or path.")
    parser.add_argument("path", nargs="?", default="C:/",
                        help="Drive or path to check (default: C:/)")
    args = parser.parse_args()

    try:
        total, used, free = shutil.disk_usage(args.path)
    except OSError as e:
        print("[FAIL] Cannot read path: " + args.path)
        print("       " + str(e))
        sys.exit(1)

    percent_used = (used / total) * 100
    print("----------")
    print("[OK] " + args.path + " Usage: " + f"{percent_used:.1f}%")
    print("     Free: " + f"{free / (1024**3):.1f} GB of {total / (1024**3):.1f} GB")
    if percent_used > 80:
        print("[WARN] Alert: " + args.path + " exceeds 80% capacity!")
    else:
        print("[OK] " + args.path + " is operating within normal parameters.")
    print("----------")
    sys.stdout.flush()

if __name__ == "__main__":
    main()