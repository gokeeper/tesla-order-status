import argparse
import os
import time

from tostl.config import ORDERS_FILE

parser = argparse.ArgumentParser(description="Retrieve Tesla order status.")
group = parser.add_mutually_exclusive_group()
group.add_argument("--status", action="store_true",
                   help="report exit code only: 0 unchanged, 1 changes, 2 pending, -1 error")
group.add_argument("--details", action="store_true",
                   help="show extra fields (financing, registration, etc.)")
group.add_argument("--all", action="store_true",
                   help="dump every available field (verbose)")
parser.add_argument("--cached", action="store_true",
                    help="reuse locally cached orders without calling the API")
parser.add_argument("--order", metavar="REFERENCE",
                    help="print only the order with the given reference number")

_args, _ = parser.parse_known_args()

if not _args.cached and os.path.exists(ORDERS_FILE):
    last_api_call = os.path.getmtime(ORDERS_FILE)
    if time.time() - last_api_call < 60:
        _args.cached = True

DETAILS_MODE = _args.details
STATUS_MODE = _args.status
CACHED_MODE = _args.cached
ALL_KEYS_MODE = _args.all
ORDER_FILTER = _args.order.strip().upper() if isinstance(_args.order, str) and _args.order.strip() else None
