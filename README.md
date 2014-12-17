x2go
====

####################################################################################
# Instructions for Installing the EDX Platform on Cubietruck Using a Booting SD Card
####################################################################################

On a Linux or Ubuntu machine connected to the Internet which have access
to a SD card Slot (You can also access a SD card through a USB):

1)  Put the contents of these EDX Platform Installation files for Cubietruck on an empty folder.

2)  Change the current directory to this folder.

3)  Insert an empty SD card on the corresponding slot.

3)  Replacing ${card} with the SD card device you are using (eg. /dev/sdc, please be sure of this
    before proceeding, so not damage happens), run:
  
        python execute sd ${card}

4)  When finished, it will be safe to take out the SD card, and it will contain Lubuntu (as specified
    on the Cubietruck web site) and the EDX installation files for Cubietruck, on the folder
    "/home/linaro/EDX"

5)  Insert the created SD card on the Cubietruck SD card slot, turn on the Cubietruck,
    and Lubuntu will load.

6)  Change directory and run the first part of the script ("upgrade_trusty" file).
    Note: The initial installation of Lubuntu on Cubietruck has Python3
  
        cd /home/linaro/EDX
        python3 execute upgrade_trusty

7)  When finished Cubietruck will reboot, so change directory and run the second part of the script
    which is the "update" file.
  
        cd /home/linaro/EDX
        python3 execute update

8)  When finished Cubietruck will reboot again, so change directory and run the third part of the script
    which consists of the EDX installation previous steps ("edxPRE"), the specific fixes for this
    platform ("fixes"), and the main EDX installation step ("edx"). You can see the files: "edxPRE",
    "fixes", and "edx", for better understanding.
  
        cd /home/linaro/EDX
        python3 execute edxPRE fixes edx

9)  Now, the EDX Installation will complete successfully, but because of continous development, new
    issues may arise. In this case, the only thing left to do is for now: rebooting and trying
    to run "edx" again, as in step 8, but just running "edx". Similarly, you can do this after canceling
    the running of "edx", if it delays too long in a specific task (which normaly runs faster) as if it
    appears to never finish. That happened to me some times at different points, maybe because of a bad
    internet connection, not too sure.
