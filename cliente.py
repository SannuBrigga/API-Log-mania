import requests
import random
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
posibles_personajes = ['Goku', 'Vegeta', 'Gohan']
NOMBRE_PERSONAJE = random.choice(posibles_personajes)


def generar_registro():
    eventos = ['debug', 'info', 'error']
    descripciones = {
        'debug': ['Saiyajin alcanzó un nuevo nivel', 'Exploración del espacio'],
        'info': ['Batalla ganada', 'Entrenamiento completado'],
        'error': ['Transformación fallida', 'Error en la cápsula espacial']
    }
    evento = random.choice(eventos)
    descripcion = random.choice(descripciones[evento])
    timestamp = datetime.datetime.now().isoformat()
    personaje = NOMBRE_PERSONAJE

    registro = {
        'evento': evento,
        'descripcion': descripcion,
        'timestamp': timestamp,
        'personaje': personaje
    }
    return registro


registro = generar_registro()
response = requests.post('http://localhost:5000/registros',
                        json=registro, headers={'API-Key': API_KEY})

print(response.json())
