import subprocess

def set_netplat():
    sub=subprocess.run(["/usr/sbin/netplan apply"], shell=True, capture_output=True, text=True)
    if sub.returncode != 0:
        print(f"Fallo Netplan: {sub.stderr}")

if __name__ == '__main__':
    set_netplat()

# python3.7 -c ['import subprocess','sub=subprocess.run(["/usr/sbin/netplan apply"], shell=True, capture_output=True, text=True)','if sub.returncode != 0:','    print(f"Fallo Netplan: {sub.stderr}")']