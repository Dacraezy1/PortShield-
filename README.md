                                   
   ____            _   ____  _     _      _     _ 
 |  _ \ ___  _ __| |_/ ___|| |__ (_) ___| | __| |
 | |_) / _ \| '__| __\___ \| '_ \| |/ _ \ |/ _` |
 |  __/ (_) | |  | |_ ___) | | | | |  __/ | (_| |
 |_|   \___/|_|   \__|____/|_| |_|_|\___|_|\__,_|
                                                                                                                                                   
                                                                                                    
# PortShield

PortShield is a lightweight, real-time port monitoring tool for Linux. It helps you keep an eye on open ports, alerts you to unexpected network activity, and can even take action to protect your system.

## Features

-   **Real-time Monitoring**: Continuously watches for new or closed ports.
-   **Process Identification**: Shows which process is listening on each port.
-   **Whitelist**: Define a list of allowed ports to prevent unauthorized services.
-   **Automatic Actions**: Optionally kill processes that listen on non-whitelisted ports.
-   **Logging**: Keeps a record of all port-related events.
-   **IPv4/IPv6 Support**: Monitors both IPv4 and IPv6 connections.
-   **Clean Output**: Uses rich for a clear and colorized terminal interface.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Dacraezy1/portshield.git
    cd portshield
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Install PortShield:
    ```bash
    pip install .
    ```

## Usage

### Scan for open ports

To see a list of all currently open ports and the processes using them:

```bash
portshield scan
```

### Monitor ports in real-time

To start monitoring for any changes in open ports:

```bash
portshield watch
```

### Manage the whitelist

Add a port to the whitelist:

```bash
portshield whitelist add 8080
```

Remove a port from the whitelist:

```bash
portshield whitelist remove 8080
```

### View logs

To see the latest events from the log file:

```bash
portshield logs
```

## Screenshot

![Screenshot Placeholder](https://via.placeholder.com/800x400.png?text=PortShield+Screenshot)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
