sudo pip3 install pillow
sudo pip3 install mariadb

sudo cp brewferm-sensors.service /lib/systemd/system/
sudo cp brewferm-relays.service /lib/systemd/system/
sudo cp brewferm-gui.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable brewferm-sensors.service
sudo systemctl enable brewferm-relays.service
sudo systemctl enable brewferm-gui.service
sudo systemctl start brewferm-sensors.service
sudo systemctl start brewferm-relays.service
sudo systemctl start brewferm-gui.service
sudo systemctl status brewferm-sensors.service
sudo systemctl status brewferm-relays.service
sudo systemctl status brewferm-gui.service
cat /home/pi/brewferm/*.log

Todo: split into 
1) a headless python service that does the sensor readings and logs them to history table
2) a headless python service that turns relays on and off based on parameters in changes table and current values in history table. It should check for current readings and turn off all relays if the last reading is too old.
3) a gui that reads and displays the history table and sends parameter changes to the changes table

4) change table `changes` to `pid_settings`
5) change table `history` to `sensor_readings`
6) add table `system_settings` for pause state, sensor polling interval, gui update interval
7) add default values for `pid_settings` and `system_settings`