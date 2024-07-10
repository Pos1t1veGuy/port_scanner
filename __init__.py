from typing import *

from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime as dt
from tqdm import tqdm

import socket
import traceback
import sys


class Scanner:
    ...


class PortScanner(Scanner):
    def __init__(self, ip: str):
        self.ip = ip
        self.openned_ports = []
        self.refused_ports = []
        self.closed_ports = []

    def scan(self, port_range: list,
        max_workers: int = 50, timeout: float = 0.7,
        show_time: bool = False, show_progress_bar: bool = False
        ) -> Dict[str, List[int]]:

        start_time = dt.now()
        openned_ports = []
        refused_ports = []
        closed_ports = []

        try:
            try:
                sorted_port_range = sorted(port_range)
                if sorted_port_range[-1] > 25565 or sorted_port_range[0] < 1:
                    raise ValueError(f'port_range must contain ports in range 1 -> 25565')
            except MemoryError:
                raise ValueError(f'port_range must contain ports in range 1 -> 25565')

            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.scan_port, port, timeout): port for port in port_range}
                if show_progress_bar:
                    progress_bar = tqdm(total=len(port_range), desc="Scanning")

                for future in as_completed(futures):
                    match future.result():
                        case 1:
                            openned_ports.append(futures[future])
                        case 2:
                            refused_ports.append(futures[future])
                        case 3:
                            closed_ports.append(futures[future])

                    if show_progress_bar:
                        progress_bar.update(1)

                if show_progress_bar:
                    progress_bar.close()

            end_time = dt.now()

            self.openned_ports = sorted(openned_ports)
            self.refused_ports = sorted(refused_ports)
            self.closed_ports = sorted(closed_ports)
            res = {
                'openned_ports': self.openned_ports,
                'refused_ports': self.refused_ports,
                'closed_ports': self.closed_ports,
            }
            if show_time:
                res['time'] = end_time - start_time

            return res
        except KeyboardInterrupt:
            print('aborted by user')

    def scan_port(self, port: int, timeout: float) -> int:
        try:
            with socket.socket() as sock:
                sock.settimeout(timeout)
                sock.connect((str(self.ip), port))
            return 1
        except socket.timeout:
            return 3
        except ConnectionRefusedError:
            return 2
        except WindowsError as we:
            if we.winerror != 10013:
                traceback.format_exc()
                print(e, port)
                return 3
        except Exception as e:
            traceback.format_exc()
            print(e, port)
            return 3

def ScannerGUI(ip: str, port_range: list):
    try:
        scanner = PortScanner(ip)
        result = scanner.scan(port_range, show_time=True, show_progress_bar=True)
        print(f"Openned ports: {', '.join([ str(port) for port in result['openned_ports']]) }" if result['openned_ports'] else 'No one openned port')
        print(f"Closed ports: {', '.join([ str(port) for port in result['closed_ports']]) }" if result['closed_ports'] else 'No one closed port')
        print(f"Refused ports: {', '.join([ str(port) for port in result['refused_ports']]) }" if result['refused_ports'] else 'No one refused port')
        print(f"\nExecuting time {result['time']}")
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    ScannerGUI( sys.argv[1], range(int(sys.argv[2]), int(sys.argv[3])) )
    " __init__.py host start_port end_port "