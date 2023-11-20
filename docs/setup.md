# Jetson Nano
I originally (and slightly regrettably) started developing the "nest" code on a Jetson Nano. 

I've worked with them before, and prefer to use them in headless mode. So here's a link to a forum post I used as reference to setup my Nano with nomachine
[nvidia developer forums](https://forums.developer.nvidia.com/t/has-anyone-had-success-installing-nomachine-on-their-nano/75535/5)

Personally, I perfer using xorg as my X server, but I found it was a little easier to get headless mode working with xfce. 

## Python
With a fresh image on a Jetson Nano, I had to install a more recent version of python, since the system default version is 2.7

`sudo apt install python3.8`
`sudo apt install python3-pip, python3.8-venv, python3-venv`

## Bluetooth
The current user needs to be in the Bluetooth group to be able to connect to any of the eggs. This can be done with,
`sudo usermod -a -G bluetooth <your username>`

I found this post helpful in setting up Bluetooth, 
[Github GDBUS Errors](https://github.com/sputnikdev/eclipse-smarthome-bluetooth-binding/issues/9)

The policy shown in the link above was already in `bluetooth.conf` for me, but adding the policy, then adding the user to the bluetooth group and reloading the bluetooth service (`sudo systemctl restart bluetooth.service`) seemed to fix some of the issues I had been having.


Hopefully some information here helps if theres any issues setting up Bluetooth!