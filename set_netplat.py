import subprocess

def set_netplat():
    #sub0=subprocess.run(["/usr/sbin/netplan apply"], shell=True, capture_output=True, text=True)
    sub0=subprocess.run(["/usr/sbin/netplan apply"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if sub0.returncode != 0:
        print(f"Fallo Netplan: {sub0.stdout.decode('UTF-8')} {sub0.stderr.decode('UTF-8')}")
    else:
        #sub1=subprocess.run(["/bin/systemctl restart networking.service"], shell=True, capture_output=True, text=True)
        sub1=subprocess.run(["/bin/systemctl restart networking.service"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Fallo Netplan: {sub0.stdout.decode('UTF-8')} {sub0.stderr.decode('UTF-8')} {sub1.stdout.decode('UTF-8')} {sub1.stderr.decode('UTF-8')}")



if __name__ == '__main__':
    set_netplat()

# python3.7 -c ['import subprocess','sub=subprocess.run(["/usr/sbin/netplan apply"], shell=True, capture_output=True, text=True)','if sub.returncode != 0:','    print(f"Fallo Netplan: {sub.stderr}")']