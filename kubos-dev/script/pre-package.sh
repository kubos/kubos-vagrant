#!/bin/bash
set -x

#Cleaning up before distribution
#Clear out the cache
rm -rf /var/cache/*

#Making all empty storage zeros allows the final box to be better compressed
dd if=/dev/zero of=/EMPTY bs=1M
rm -f /EMPTY
sync


#Change the ssh key to the default vagrant insecure key so others can ssh in when they start this box locally
echo " Changing SSH keys"
echo "AuthorizedKeysFile %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > /home/vagrant/.ssh/authorized_keysmod 0600 /home/vagrant/.ssh/authorized_keys

chmod 0600 /home/vagrant/.ssh/authorized_keys
chmod 0700 /home/vagrant/.ssh
chown -R vagrant  /home/vagrant/.ssh

#clear terminal history
history -cw

