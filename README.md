x2go
====

####################################################################################
# Instructions for Installing the EDX Platform on Cubietruck Using a Booting SD Card
####################################################################################

On a Linux (tested on Ubuntu) machine connected to the Internet which have access
to a SD card Slot (You can also access a SD card through a USB):

1. Clone this repo and change to its directory
1. Insert, but do not mount, the SD card, and note the device name (e.g. `/dev/sdb`)
1. Run `python execute sd /dev/sd_device` 

This should download an ARM Ubuntu image with edX pre-installed. For further services and configuration, use the scripts and Ansible playbooks in the [provision ](https://github.com/tunapanda/provision) repo. 

**NOTE:** The base install does not currently include openssh, so you will need to install that yourself (`apt-get install openssh-server)`. Inclusion of this service will be built into the base image and/or the provision repo soon. 
