#!/usr/bin/env python3
"""Entry point for TOSTL — Tesla Order Status Tracker Lite."""

import sys
import traceback


def main() -> None:
    from tostl.utils.migration import main as run_all_migrations
    from tostl.utils.auth import main as run_tesla_auth
    from tostl.utils.orders import main as run_orders

    run_all_migrations()
    access_token = run_tesla_auth()
    run_orders(access_token)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 - catch-all for user guidance
        print(f"\n[ERROR] {e}\n")
        traceback.print_exc()
        print("\nIf the problem persists, please create an issue including the complete output of tostl.py")
        print("GitHub Issues: https://github.com/gokeeper/tesla-order-status/issues")
        sys.exit(1)
