#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# Find the meater address with hcitool lescan (label MEATER).
# run readMeater.py <address>
# python ./readMeater.py D0:D9:4F:83:E8:EB

import time
from bluepy import btle
import time
import click
import paho.mqtt.client as mqtt 

from meater import MeaterProbe

@click.command()
@click.option("--device", '-d', multiple=True, help="bluetooth id of Meater")
@click.option("--mosquitto-server", '-m', help="url of mosquitto server to send results to.")
def main(device, mosquitto_server):
   if mosquitto_server is not None:
      print(f"Connecting to mosquitto server: {mosquitto_server}...")
      client = mqtt.Client("Meater")
      client.connect(mosquitto_server)

   print("Connecting...")
   devs = [MeaterProbe(addr) for addr in device]
   print("Connected")


   while True:
      for dev in devs:
         dev.update()
         print(dev)
         if mosquitto_server is not None:
            client.publish("TEMPERATURE_C", dev.getTipC())
      time.sleep(1)

if __name__ == '__main__':
    main()