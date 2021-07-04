sudo systemctl start brewferm-gui.service
sleep 30
sudo systemctl start brewferm-sensors.service
sleep 30
sudo systemctl start brewferm-controller.service
sleep 40
sudo systemctl start brewferm-relays.service
