# Rasberry Pi 5 - NVMe hat with ASM1064 fix

This procedure modifies the Raspberry Pi 5 device tree to improve compatibility with NVMe HATs and ASM1064-based PCIe controllers. It starts by gaining root access and creating a backup of the original device tree blob (`bcm2712-rpi-5-b.dtb`). The device tree is then decompiled into a human-readable `.dts` format, where the `pcie@1..` node is renamed to `p1: pcie@1...`, and references to `<0x..>` are replaced with `<&p1>`. These modifications ensure that PCIe devices, such as NVMe adapters and ASM1064 SATA controllers, are properly detected and initialized by the firmware. After making the changes, the `.dts` file is recompiled back into a `.dtb` file and replaces the original firmware file. The system is then rebooted to apply the new configuration, potentially resolving issues related to PCIe lane assignment, device detection, and stability when using NVMe SSDs or SATA expansions on the Raspberry Pi 5.

```bash
sudo su
sudo cp /boot/firmware/bcm2712-rpi-5-b.dtb /boot/firmware/bcm2712-rpi-5-b.dtb.bak
dtc -I dtb -O dts /boot/firmware/bcm2712-rpi-5-b.dtb -o ~/fix.dts
nano ~/fix.dts
```

> - replace `pcie@1..` to `p1: pcie@1..`
> - replace `msi-parrent: <0x..>` to `msi-parrent: <&p1>`

```bash
dtc -I dts -O dtb ~/fix.dts -o ~/fix.dtb
sudo mv ~/fix.dtb /boot/firmware/bcm2712-rpi-5-b.dtb
rm ~/fix.dts
reboot
```

### Python script not yet tested!
