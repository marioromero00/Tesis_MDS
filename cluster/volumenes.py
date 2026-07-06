import ray
import os

ray.init("ray://localhost:10001")

@ray.remote
def ver_datos():
    ruta = "/Volumes/Externo4T/GoogleDrive/Tesistas Neurodatos/Datos  Crudos/EEG/EEG por Estímulo/Estímulos Emocionales"


    return {
        "existe": os.path.exists(ruta),
        "contenido": os.listdir(ruta)[:30] if os.path.exists(ruta) else None
    }

print(ray.get(ver_datos.remote()))
#['.DS_Store', 'Eye Tracker Data - Limpio', 'Datos GSR', 'Camara - Limpio', 'Proyecto Tobii - Limpio', 'obs de limpieza de data.gdoc', 'EEG']