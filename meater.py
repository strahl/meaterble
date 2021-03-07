from bluepy import btle
import time
__all__ = ['MeaterProbe']
 
class MeaterProbe:
   def __init__(self, addr):
      self._addr = addr
      self.connect()
      self.update()
       
   @staticmethod
   def bytesToInt(byte0, byte1):
      return byte1*256+byte0

   @staticmethod
   def convertAmbient(array): 
      tip = MeaterProbe.bytesToInt(array[0], array[1])
      ra  = MeaterProbe.bytesToInt(array[2], array[3])
      oa  = MeaterProbe.bytesToInt(array[4], array[5])
      return int(tip+(max(0,((((ra-min(48,oa))*16)*589))/1487)))
      
   @staticmethod
   def toCelsius(value):
      return (float(value)+8.0)/16.0

   @staticmethod
   def toFahrenheit(value):
      return ((MeaterProbe.toCelsius(value)*9)/5)+32.0

   def getTip(self):
      if hasattr(self, '_tip'):
         return self._tip
      return None

   def getTipF(self):
      if hasattr(self, '_tip'):
         return MeaterProbe.toFahrenheit(self._tip)
      return None

   def getTipC(self):
      if hasattr(self, '_tip'):
         return MeaterProbe.toCelsius(self._tip)
      return None

   def getAmbientF(self):
      if hasattr(self, '_ambient'):
         return MeaterProbe.toFahrenheit(self._ambient)
      return None

   def getAmbient(self):
      if hasattr(self, '_ambient'):
         return self._ambient
      return None

   def getAmbientC(self):
      if hasattr(self, '_ambient'):
         return MeaterProbe.toCelsius(self._ambient)
      return None

   def getBattery(self):
      if hasattr(self, '_ambient'):
         return self._battery
      return None

   def getAddress(self):
      if hasattr(self, '_addr'):
         return self._addr
      return None

   def getID(self):
      if hasattr(self, '_id'):
         return self._id
      return None

   def getFirmware(self):
      if hasattr(self, '_firmware'):
         return self._firmware
      return None

   def connect(self):
      self._dev = btle.Peripheral(self._addr)

   def readCharacteristic(self, c):
      return bytearray(self._dev.readCharacteristic(c))

   def update(self):
      tempBytes = self.readCharacteristic(31)
      batteryBytes = self.readCharacteristic(35)
      if len(tempBytes) > 0:
         self._tip = MeaterProbe.bytesToInt(tempBytes[0], tempBytes[1])
         self._ambient = MeaterProbe.convertAmbient(tempBytes)
         self._battery = MeaterProbe.bytesToInt(batteryBytes[0], batteryBytes[1])*10
         (self._firmware, self._id) = str(self.readCharacteristic(22)).split("_")
         self._lastUpdate = time.time()

   def __str__(self):
      if hasattr(self, '_lastUpdate'):
         return "%s %s probe: %s tip: %fF/%fC ambient: %fF/%fC battery: %d%% age: %ds" % (self.getAddress(), self.getFirmware(), self.getID(), self.getTipF(), self.getTipC(), self.getAmbientF(), self.getAmbientC(), self.getBattery(), time.time() - self._lastUpdate)
      return "No data yet."
