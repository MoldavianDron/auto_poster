## How to get device ip?
1. Show connected devices
    ```shell
    adb devices 
    ```
2. Find the device IP address
    ```shell
    adb -s <DEVICE_SERIAL> shell ip addr show wlan0
    ```
   Get your device's ip address from output
