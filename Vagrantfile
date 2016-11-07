# -*- mode: ruby -*-
# vim: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provision "shell", path: "./script/provision.sh"

  # Enable USB access
  usb_devs = [
    # Required for programming new fraunchpad
    ['0x2047', '0x0013', 'MSP4305969 Launchpad programmer'],
    ['0x2047', '0x0203', 'MSP4305969 Launchpad FW updater'],
    # Other USB ids from TI's udev rules.
    ['0x2047', '0x0010', 'MSP430UIF'],
    ['0x2047', '0x0014', 'MSP430UIF'],
    ['0x2047', '0x0204', 'MSP430UIF'],
    # For older fraunchpads and launchpads
    ['0x0451', '0xf432', 'eZ430'],
    # Misc devices
    ['0x15ba', '0x0031', 'Olimex JTAG tiny'],

  ]

  config.vm.provider "virtualbox" do |vb|
    vb.customize ['modifyvm', :id, '--usb', 'on']
    usb_devs.each do |dev|
      vb.customize ['usbfilter', 'add', '0', '--target', :id, '--vendorid', dev[0], '--productid', dev[1], '--name', dev[2]]
    end
    # Don't boot with headless mode
    # vb.gui = true
    vb.customize ['modifyvm', :id, '--usbehci', 'on']
    vb.customize ['modifyvm', :id, '--usb', 'on']
  end
end
