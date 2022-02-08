Note: This software is Alpha!!! 

This should, but hasn't been tested, to work with HDMI out on the rpi. I've developed against a touch-screen LCD with dimension 640x480.

```
sudo pip3 install mariadb
sudo pip3 install simple-pid

sudo cp services/brewferm-sensors.service /lib/systemd/system/
sudo cp services/brewferm-relays.service /lib/systemd/system/
sudo cp services/brewferm-gui.service /lib/systemd/system/
sudo cp services/brewferm-controller.service /lib/systemd/system

sudo systemctl daemon-reload

sudo systemctl enable brewferm-sensors.service
sudo systemctl enable brewferm-relays.service
sudo systemctl enable brewferm-gui.service
sudo systemctl enable brewferm-controller.service

sudo systemctl start brewferm-sensors.service
sudo systemctl start brewferm-relays.service
sudo systemctl start brewferm-gui.service
sudo systemctl start brewferm-controller.service

sudo systemctl status brewferm-sensors.service
sudo systemctl status brewferm-relays.service
sudo systemctl status brewferm-gui.service
sudo systemctl status brewferm-controller.service

cat /home/pi/brewferm/logs/*.log
```

I'll be adding diagrams but for now:
  * If you're not qualified to work with high voltages, hire someone qualified
  * Hook up a Solid-State Relay (SSR) of at least 25amps to pins defined in relays.py statement ' myrelays = BrewfermRelays(cool_pin, heat_pin)'
  * Hook up one-wire sensors
  * Use 'Settings'->'Assign Sensors' screen to assign a sensor to a function. Clicking the button next to the sensor id will cycle through available functions. 
