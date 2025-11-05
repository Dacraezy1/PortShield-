import argparse
from . import core
from . import monitor
from . import utils

def main():
    """Main entry point for the PortShield CLI."""
    parser = argparse.ArgumentParser(description="PortShield - A real-time port monitoring tool.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for open ports.")

    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Monitor ports in real-time.")
    watch_parser.add_argument("--kill", action="store_true", help="Kill processes on unwhitelisted ports.")

    # Whitelist command
    whitelist_parser = subparsers.add_parser("whitelist", help="Manage the port whitelist.")
    whitelist_subparsers = whitelist_parser.add_subparsers(dest="whitelist_command", help="Whitelist commands")
    whitelist_add_parser = whitelist_subparsers.add_parser("add", help="Add a port to the whitelist.")
    whitelist_add_parser.add_argument("port", type=int, help="The port to add.")
    whitelist_remove_parser = whitelist_subparsers.add_parser("remove", help="Remove a port from the whitelist.")
    whitelist_remove_parser.add_argument("port", type=int, help="The port to remove.")

    # Logs command
    logs_parser = subparsers.add_parser("logs", help="View recent alerts.")

    args = parser.parse_args()

    utils.ensure_dirs()

    if args.command == "scan":
        core.scan()
    elif args.command == "watch":
        monitor.watch(kill_unwhitelisted=args.kill)
    elif args.command == "whitelist":
        if args.whitelist_command == "add":
            utils.add_to_whitelist(args.port)
        elif args.whitelist_command == "remove":
            utils.remove_from_whitelist(args.port)
        else:
            whitelist_parser.print_help()
    elif args.command == "logs":
        with open(utils.LOG_FILE, "r") as f:
            print(f.read())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
