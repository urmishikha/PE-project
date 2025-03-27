from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
import threading
import time
from utils.threat_intelligence import check_threat_intelligence
from utils.firewall import block_ip

class NetworkMonitor:
    def __init__(self, callback_function, window_size=60):
        self.callback = callback_function
        self.window_size = window_size
        self.traffic_stats = defaultdict(lambda: defaultdict(int))
        self.lock = threading.Lock()
        self.is_running = True

    def start_monitoring(self):
        self.capture_thread = threading.Thread(target=self._capture_packets)
        self.capture_thread.daemon = True
        self.capture_thread.start()

        self.analysis_thread = threading.Thread(target=self._analyze_traffic)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()

    def _capture_packets(self):
        sniff(prn=self._process_packet, store=False)

    def _process_packet(self, packet):
        if IP in packet:
            with self.lock:
                src_ip = packet[IP].src
                self.traffic_stats[src_ip]['packet_count'] += 1
                self.traffic_stats[src_ip]['total_bytes'] += len(packet)
                if TCP in packet:
                    self.traffic_stats[src_ip]['tcp_count'] += 1
                elif UDP in packet:
                    self.traffic_stats[src_ip]['udp_count'] += 1

    def _analyze_traffic(self):
        while self.is_running:
            time.sleep(self.window_size)
            with self.lock:
                for ip, stats in self.traffic_stats.items():
                    features = self._extract_features(stats)
                    self.callback(ip, features)
                self.traffic_stats.clear()

    def _extract_features(self, stats):
        return [
            stats['packet_count'],
            stats['total_bytes'] / max(stats['packet_count'], 1),
            stats['tcp_count'] / max(stats['packet_count'], 1),
            stats['udp_count'] / max(stats['packet_count'], 1)
        ]