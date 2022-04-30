import subprocess
import ipaddress
import datetime

class Network():
    def __init__(self,interface,hostname,address,netmask,gateway,dhcp,dns1,dns2):
        self.interface = interface
        self.hostname = hostname
        self.address = address
        self.netmask = netmask
        self.gateway = gateway
        self.dhcp = dhcp
        self.dns1 = dns1
        self.dns2 = dns2
        self.disabled = ''

    @classmethod
    def get_net(cls, interface):
        sub0 = subprocess.run('/bin/hostname', shell=True, capture_output=True, text=True)
        #Network.logerr(f'00code:{sub0.returncode}\nout:{sub0.stdout}\nerr:{sub0.stderr}\n')
        hostname = sub0.stdout.strip()
        sub1 = subprocess.run(f'/sbin/ip addr show {interface} | /bin/grep inet', shell=True, capture_output=True, text=True)
        #Network.logerr(f'01code:{sub1.returncode}\nout:{sub1.stdout}\nerr:{sub1.stderr}\n')
        buff = sub1.stdout.split()
        buff = ipaddress.ip_interface(buff[1].strip())
        buff = buff.with_netmask
        buff = buff.split('/')
        address = buff[0]
        netmask = buff[1]
        sub2 = subprocess.run(f'/sbin/ip route | /bin/grep default | /bin/grep {interface}', shell=True, capture_output=True, text=True)
        #Network.logerr(f'02code:{sub2.returncode}\nout:{sub2.stdout}\nerr:{sub2.stderr}\n')
        buff = sub2.stdout.split()
        gateway = buff[2]
        dhcp = buff[6]
        sub3 = subprocess.run(f'/usr/bin/nmcli dev show {interface} | /bin/grep DNS', shell=True, capture_output=True, text=True)
        #Network.logerr(f'03code:{sub3.returncode}\nout:{sub3.stdout}\nerr:{sub3.stderr}\n')
        buff = sub3.stdout.split()
        dns1 = buff[1]
        dns2 = buff[3]
        print(f'-{hostname},{address},{netmask},{dhcp},{gateway},{dns1},{dns2}-')
        net = Network(interface=interface,hostname=hostname,address=address,netmask=netmask,gateway=gateway,dhcp=dhcp,dns1=dns1,dns2=dns2)
        net.disabled = net.is_dhcp()
        return net

    def is_dhcp(self):
        if self.dhcp=='dhcp':
            return 'disabled'
        else:
            return ''

    @classmethod
    def upnet_dhcp(cls, interface):
        origen = "/etc/netplan/set-network.yaml"
        doc = f'# Let NetworkManager manage all devices on this system\nnetwork:\n  version: 2\n  renderer: NetworkManager\n  ethernets:\n    {interface}:\n      dhcp4: yes'
        try:
            archi=open(origen, mode='w+')
            archi.write(doc)
            archi.close()
            fin = 0
        except OSError as err:
            fin = f'Error {err.args}'
        print(fin)
        return fin

    @classmethod
    def upnet_static(cls, interface, address, netmask, gateway, dns1, dns2):
        origen = "/etc/netplan/set-network.yaml"
        buff = ipaddress.ip_interface(f'{address}/{netmask}')
        buff = buff.with_prefixlen
        buff = buff.split('/')
        address, netmask = buff[0], buff[1]
        doc = f'# Let NetworkManager manage all devices on this system\nnetwork:\n  version: 2\n  renderer: NetworkManager\n  ethernets:\n    {interface}:\n      dhcp4: no\n      addresses: [{address}/{netmask}]\n      gateway4: {gateway}\n      nameservers:\n        addresses: [{dns1},{dns2}]'
        try:
            archi=open(origen, mode='w+')
            archi.write(doc)
            archi.close()
            return 0
        except OSError as err:
            return f'Error {err.args}'

    @classmethod
    def del_netold(cls, interface, address, netmask):
        buff = ipaddress.ip_interface(f'{address}/{netmask}')
        buff = buff.with_prefixlen.strip()
        sub0 = subprocess.run(f'/sbin/ip addr del {buff} dev {interface}', shell=True, capture_output=True, text=True)
        Network.logerr(f'20code:{sub0.returncode}\nout:{sub0.stdout}\nerr:{sub0.stderr}\n')
        return sub0.returncode

    @classmethod
    def apply_netplan(cls):
        sub0 = subprocess.run('/bin/pwd', shell=True, capture_output=True, text=True)
        ruta = sub0.stdout.strip()+'/set_netplan.py'
        subX = subprocess.run(f'/bin/ls', shell=True, capture_output=True, text=True)
        Network.logerr(f'10code:{sub0.returncode}\nout:{sub0.stdout}-{ruta}-{subX.stdout}-\nerr:{sub0.stderr}\n')
        sub1 = subprocess.run(f'/usr/bin/python3.7 set_netplat.py', shell=True, capture_output=True, text=True)
        Network.logerr(f'11code:{sub1.returncode}\nout:{sub1.stdout}\nerr:{sub1.stderr}\n')
        if sub1.returncode == 0:
            return 'Netplan ejecutado con exito', 0
        else:
            return 'Netplan fallo la ejecucion', 1
    
    @classmethod
    def logerr(cls, msj):
        origen = '/home/alejandro/webapp/logerr.txt'
        try:
            archi=open(origen, mode='a+')
            archi.write(msj)
            archi.close()
            return 0
        except OSError as err:
            return f'Error {err.args}'

class Time_Local():
    def __init__(self, dt, zn, ntp):
        self.dt = dt
        self.zn = zn
        self.ntp = ntp

    @classmethod
    def get_timelocal(cls):
        dt = datetime.datetime.now()
        sub0 = subprocess.run('/usr/bin/timedatectl status | /bin/grep zone', shell=True, capture_output=True, text=True)
        buff = sub0.stdout.strip().split()
        zn = buff[2]
        sub1 = subprocess.run('/usr/bin/timedatectl status | /bin/grep timesyncd', shell=True, capture_output=True, text=True)
        buff = sub1.stdout.strip().split()
        ntp = buff[2]
        dtl = Time_Local(dt=dt, zn=zn, ntp=ntp)
        return dtl

    @classmethod
    def get_timezones(cls):
        sub0 = sub0 = subprocess.run('/usr/bin/timedatectl list-timezones', shell=True, capture_output=True, text=True)
        buff = sub0.stdout.strip().split()
        tup = []
        for zone in buff:
            tup.append((zone,zone))
        return tup