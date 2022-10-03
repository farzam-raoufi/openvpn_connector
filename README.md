create new file named login.conf in "/etc/openvpn" path and then add your clients username and password.

you can use this command to create login.conf (replace username and password by your username and password. don't remove "\n"):

    sudo echo -e "username\npass" > /etc/openvpn/login.conf

after create login.conf, move all your ".opvpn" files to "./openvpn_row_files" path and use follwing command to connect connect openvpn

    sudo python3 openvpn_connector.py

good luck