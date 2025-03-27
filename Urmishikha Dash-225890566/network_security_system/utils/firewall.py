import os
import logging

# Logging configuration
logging.basicConfig(filename='logs/firewall.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def block_ip(ip_address):
    """
    Block an IP address using macOS's pf firewall.
    """
    try:
        # Add the IP to the pf configuration file
        with open('/etc/pf.conf', 'a') as f:
            f.write(f'\nblock drop quick from {{ {ip_address} }} to any\n')
        
        # Reload the pf configuration
        os.system('sudo pfctl -f /etc/pf.conf')
        
        logging.info(f"Blocked IP: {ip_address}")
        print(f"Blocked IP: {ip_address}")
    except Exception as e:
        logging.error(f"Failed to block IP {ip_address}: {str(e)}")
        print(f"Failed to block IP {ip_address}: {str(e)}")