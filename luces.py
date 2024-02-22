import time 
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Custom
from fixture_model import FixtureModel
from leer_json import cargar_luces_desde_json
# Cargar luces desde JSON
luces = cargar_luces_desde_json()

# Ejemplo de uso
if luces is not None:
    print("Encender:", luces.encender)
    print("Apagar:", luces.apagar)
else:
    print("No se pudieron cargar las luces desde el JSON.")


dmx = OpenDMXController()
light_fixture_model = FixtureModel('RGBW') 
# Big square fixture model
bsq_fixture_model = FixtureModel("DRGBWSEP")
custom_fixture = dmx.add_fixture(Custom,name="CustomFixture", start_channel=1, channels=500)
bsq_fixture_model.setup_fixture(custom_fixture)

def encender_luz(channel):
    custom_fixture.dim(255, 0, channel - 1)
def apagar_luz(channel):
    custom_fixture.dim(0, 0, channel - 1)

for channel in luces.encender:
    encender_luz(channel)

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