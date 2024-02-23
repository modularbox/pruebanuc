Instalar PyDMXControl
Sustutuir VERSION la version que tengas de python
Despues ir a la carpeta /usr/local/lib/python[VERSION]/dist-packages/PyDMXControl/web/_routes.py
Y en el archivo ir a routes = Blueprint(''), __name__, url_prefix='/')
Y modificarlo por
Y en el archivo ir a routes = Blueprint('dmx'), __name__, url_prefix='/')
