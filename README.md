Note: This software is pre-Alpha!!! Not ready to test

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

Todo: add min and max on,off and between time limits to relays logic

