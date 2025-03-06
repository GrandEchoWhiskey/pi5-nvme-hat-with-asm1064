import os

def check_privileges() -> None:
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        raise PermissionError("You need to run this script with sudo or as root.")

def fix_pointers(data: str) -> str:
    data1, data2 = data.split('pcie@1', 1)
    data2, data3 = data2.split('msi-parent = <', 1)
    data3, data4 = data3.split('>', 1)
    if data4.find('pcie@1'):
        data5, data6 = data4.split('pcie@1', 1)
        data7, data8 = data6.split('msi-parent = <', 1)
        data8, data9 = data8.split('>', 1)
        data4 = data5 + 'p2: pcie@1' + data7 + 'msi-parent = <&p2>' + data9

    data = data1 + 'p1: pcie@1' + data2 + 'msi-parent = <&p1>' + data4

    return data

def __main__():
    check_privileges()
    os.system('sudo cp /boot/firmware/bcm2712-rpi-5-b.dtb /boot/firmware/bcm2712-rpi-5-b.dtb.bak')
    os.system('dtc -I dtb -O dts /boot/firmware/bcm2712-rpi-5-b.dtb -o ~/fix.dts')

    with open('~/fix.dts', 'r') as file:
        data = file.read()

    data = fix_pointers(data)

    with open('~/fix.dts', 'w') as file:
        file.write(data)

    os.system('dtc -I dts -O dtb ~/fix.dts -o ~/fix.dtb')
    os.system('sudo mv ~/fix.dtb /boot/firmware/bcm2712-rpi-5-b.dtb')
    os.system('rm ~/fix.dts')
    os.system('reboot')