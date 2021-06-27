sudo systemctl start brewferm-gui.service
sleep 20
sudo systemctl start brewferm-sensors.service
sleep 15
sudo systemctl start brewferm-controller.service
sleep 20
sudo systemctl start brewferm-relays.service
