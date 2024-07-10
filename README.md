# port_scanner

## PortScanner class
Create scanner for your IP:
```py
from port_scanner import PortScanner
scanner = PortScanner('localhost')
```
Start scan process and save result:
```py
result = scanner.scan(port_range, show_time=True, show_progress_bar=True)
```
result will be dictionary with keys:<br>
-  '***openned_ports***': List[int];<br>
-  '***closed_ports***': List[int];<br>
-  '***refused_ports***': List[int] (These ports is open but refuse scanner connection);<br>

Arguments:<br>
-  '***port_range***' must be list or range object and not contain numbers less than 1 or more than 25565 (minimum and maximum port). Ports not in range will be ignored;<br>
-  '***show_time***' if is True it will return 'time' key in result with datetime.timedelta, it is scanning time;<br>
-  '***show_progress_bar***' if is True it will show TQDM progress bar in console;<br>

## ScannerGUI function
It will show in console scan result by arguments:<br>
'***IP***': str, '***port_range***': list or range
```py
from port_scanner import ScannerGUI
ScannerGUI( sys.argv[1], range(int(sys.argv[2]), int(sys.argv[3])) )
```
It will make console util, you can use it to call " ***port_scanner/__init__.py*** *host* start_port end_port " from console
