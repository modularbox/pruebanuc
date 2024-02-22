import time 
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Custom
from fixture_model import FixtureModel
dmx = OpenDMXController()
light_fixture_model = FixtureModel('RGBW') 

# Big square fixture model
bsq_fixture_model = FixtureModel("DRGBWSEP")

custom_fixture = dmx.add_fixture(Custom,name="CustomFixture", start_channel=1, channels=500)
bsq_fixture_model.setup_fixture(custom_fixture)

print("EncenderLuces")
custom_fixture.dim(255, 0, 1)
custom_fixture.dim(255, 0, 2)
custom_fixture.dim(255, 0, 3)
custom_fixture.dim(255, 0, 4)
custom_fixture.dim(255, 0, 7)
custom_fixture.dim(255, 0, 12)
custom_fixture.dim(255, 0, 17)
custom_fixture.dim(255, 0, 22)
custom_fixture.dim(255, 0, 29)

def encender():
    custom_fixture.dim(255, 0, 1)
    custom_fixture.dim(255, 0, 2)
    custom_fixture.dim(255, 0, 3)
    custom_fixture.dim(255, 0, 4)
    custom_fixture.dim(255, 0, 7)
    custom_fixture.dim(255, 0, 12)
    custom_fixture.dim(255, 0, 17)
    custom_fixture.dim(255, 0, 22)
    custom_fixture.dim(255, 0, 29)

encender()
while True:
    time.sleep(3)
print("LucesTermino")
"""
 FT232R USB UART:

                  Product ID: 0x6001
                  Vendor ID: 0x0403  (Future Technology Devices International Limited)
                  Version: 6.00
                  Serial Number: AL0409WG
                  Speed: Up to 12 Mb/s
                  Manufacturer: FTDI
                  Location ID: 0x00113000 / 6
                  Current Available (mA): 500
                  Current Required (mA): 90
                  Extra Operating Current (mA): 0
"""