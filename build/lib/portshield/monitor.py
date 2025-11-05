import time
import datetime
from . import core
from . import utils

def watch(kill_unwhitelisted=False):
    """Monitors open ports in real-time and alerts on changes."""
    utils.print_info("Starting real-time port monitoring...")
    known_ports = core.get_open_ports()
    whitelist = utils.get_whitelist()

    while True:
        try:
            current_ports = core.get_open_ports()
            new_ports = set(current_ports.keys()) - set(known_ports.keys())
            closed_ports = set(known_ports.keys()) - set(current_ports.keys())

            for port in new_ports:
                info = current_ports[port]
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"[{timestamp}] Port opened: {port} ({info['process']}, PID: {info['pid']})"
                utils.log_event(message)

                if port not in whitelist:
                    utils.print_danger(message)
                    if kill_unwhitelisted:
                        try:
                            proc = psutil.Process(info['pid'])
                            proc.kill()
                            kill_message = f"[{timestamp}] Killed process {info['process']} (PID: {info['pid']}) on unwhitelisted port {port}"
                            utils.log_event(kill_message)
                            utils.print_danger(kill_message)
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            error_message = f"[{timestamp}] Failed to kill process {info['process']} (PID: {info['pid']}): {e}"
                            utils.log_event(error_message)
                            utils.print_warning(error_message)
                else:
                    utils.print_success(message)


            for port in closed_ports:
                info = known_ports[port]
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"[{timestamp}] Port closed: {port} ({info['process']}, PID: {info['pid']})"
                utils.log_event(message)
                utils.print_info(message)

            known_ports = current_ports
            time.sleep(5)  # Update every 5 seconds
        except KeyboardInterrupt:
            utils.print_info("\nStopping port monitoring.")
            break
