import os
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "portshield"
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "portshield"
WHITELIST_FILE = CONFIG_DIR / "whitelist.txt"
LOG_FILE = DATA_DIR / "logs.txt"

def ensure_dirs():
    """Ensure that the config and data directories exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WHITELIST_FILE.touch(exist_ok=True)
    LOG_FILE.touch(exist_ok=True)

def get_whitelist():
    """Reads the whitelist of allowed ports."""
    ensure_dirs()
    with open(WHITELIST_FILE, "r") as f:
        return {int(line.strip()) for line in f if line.strip().isdigit()}

def add_to_whitelist(port):
    """Adds a port to the whitelist."""
    ensure_dirs()
    whitelist = get_whitelist()
    if port in whitelist:
        print_info(f"Port {port} is already in the whitelist.")
        return
    with open(WHITELIST_FILE, "a") as f:
        f.write(f"{port}\n")
    print_success(f"Port {port} added to the whitelist.")

def remove_from_whitelist(port):
    """Removes a port from the whitelist."""
    ensure_dirs()
    whitelist = get_whitelist()
    if port not in whitelist:
        print_warning(f"Port {port} is not in the whitelist.")
        return
    whitelist.remove(port)
    with open(WHITELIST_FILE, "w") as f:
        for p in sorted(list(whitelist)):
            f.write(f"{p}\n")
    print_success(f"Port {port} removed from the whitelist.")

def log_event(message):
    """Logs an event to the log file."""
    ensure_dirs()
    with open(LOG_FILE, "a") as f:
        f.write(f"{message}\n")

def print_success(message):
    """Prints a success message."""
    if RICH_AVAILABLE:
        console.print(f"[bold green]✔ {message}[/bold green]")
    else:
        print(f"✔ {message}")

def print_info(message):
    """Prints an info message."""
    if RICH_AVAILABLE:
        console.print(f"[bold blue]ℹ {message}[/bold blue]")
    else:
        print(f"ℹ {message}")

def print_warning(message):
    """Prints a warning message."""
    if RICH_AVAILABLE:
        console.print(f"[bold yellow]⚠ {message}[/bold yellow]")
    else:
        print(f"⚠ {message}")

def print_danger(message):
    """Prints a danger message."""
    if RICH_AVAILABLE:
        console.print(f"[bold red]✖ {message}[/bold red]")
    else:
        print(f"✖ {message}")

def print_table(headers, rows):
    """Prints a table of data."""
    if RICH_AVAILABLE:
        table = Table(show_header=True, header_style="bold magenta")
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*[str(item) for item in row])
        console.print(table)
    else:
        # Simple text fallback
        header_str = " | ".join(headers)
        print(header_str)
        print("-" * len(header_str))
        for row in rows:
            print(" | ".join([str(item) for item in row]))
