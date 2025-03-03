# WIFID

This document provides an overview of the ` WIFID.py` script, which is designed to demonstrate various wireless network attack techniques such as MAC spoofing, deauthentication attacks
(WEP cracking), beacon flooding, and evil twin attacks. The tool operates under the hood of a legitimate wireless network but uses unethical methods to achieve its goals.

## Overview

The script provides commands for:
- Spoofing device MAC addresses.
- Generating deauth packets (for WEP cracking).
- Beacon flooding to find open SSIDs.
- Creating evil twins (cloning SSIDs and MACs).

Note: Use this tool responsibly. Security research should always comply with local laws.

## Quick Start Guide

```bash
python3 WIFID.py -h
```

## Configuration

The attacks are defined in a YAML config file (`config.yml`). Here's an example:

```yaml
airplane:
  mode: deauth
  target_ap: AP123456
  target_client: 192.168.1.100
  power: 75
  count: 200

beacon_flood:
  interface: wlan0
  num_aps: 20

evil_twin:
  real_ap_ssid: airplane
```

## Attacks

### Spoofing MAC Address

Run the script in monitor mode:

```bash
python3 wireless_attack_tool.py -i wlan0
```

### Deauth (WEP Cracking)

```python
python3 wireless_attack_tool.py -a deauth airplane AP123456 75 200
```

### Beacon Flooding

```python
python3 wireless_attack_tool.py -a beacon_flood airplane wlan0 20
```

### Evil Twin Attack

```python
python3 wireless_attack_tool.py -a evil_twin airplane
```

## Command List (config.yml)

```yaml
airplane:
  type: deauth
  target_ap: AP123456
  target_client: 192.168.1.100
  power: 75
  count: 200

beacon_flood:
  interface: wlan0
  num_aps: 20

evil_twin:
  real_ap_ssid: airplane

interface:
  type: str
  default: wlan0

attacks:
  - airplane
  - beacon_flood
  - evil_twin

log-level:
  level: debug | info | warning | error | critical
  default: warning
```

## Known Issues

- **AP Without WPS Support:** Evil twin attacks may fail if the AP doesn't support Wi-Fi Protected Setup (WPS).
- **AP Initialization Time:** Beacon flooding can be delayed by some APs, causing some SSIDs not to appear.
- **AP Reboots:** If an AP reboots after an evil twin attack is launched, the attack fails.

## Troubleshooting

1. **Connection refused:**
   ```bash
   ifconfig -a
   ```

2. **Cannot bind:**
   Adjust network interfaces in `airplane` config.

3. **Authentication failed:**
   Remove or comment out your AP credentials from the config file before running attacks.

## Ethical Considerations

• Security research should always comply with local laws.
• Tools should be used for legitimate security testing purposes only.
• Always ensure any modifications to network devices are done ethically and legally.
