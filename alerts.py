import os
import time
import subprocess
import requests

interface = "eth0"  # your network interface Here!
dumpdir = "/tmp/"

while True:
    with open("/proc/net/dev") as f:
        data = f.readlines()

    for line in data:
        if interface in line:
            pkt_new = int(line.split()[1])
            break

    time.sleep(1)

    with open("/proc/net/dev") as f:
        data = f.readlines()

    for line in data:
        if interface in line:
            pkt_old = int(line.split()[1])
            break

    pkt = pkt_new - pkt_old
    print(f"\r{pkt} packets/s", end="")
    time.sleep(0.5)
    os.system("clear")

    if pkt > 15000:  # If over 15000 packets
        print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} Under attack, dumping packets.")

     
        pkt_t = pkt / 1460
        msg_content = f"Dumping {pkt_t:.2f} Megabytes"
        
        # Put Your Discord webhook Here!
        webhook_url = "PUT YOUR WEBHOOK URL HERE"
        payload = {"content": msg_content}
        requests.post(webhook_url, json=payload)

    
        dump_file = f"{dumpdir}/dump.{time.strftime('%Y%m%d-%H%M%S')}.cap"
        subprocess.run(["tcpdump", "-n", "-s0", "-c", "2000", "-w", dump_file])
        
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Just got hit [Sleeping for 5 min].")
        time.sleep(300)
