from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="registros",
    user="postgres",
    password="sanny",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id SERIAL PRIMARY KEY,
        personaje VARCHAR(50),
        evento VARCHAR(50),
        descripcion TEXT,
        timestamp TIMESTAMP
    )
''')
conn.commit()

API_KEY = os.getenv("API_KEY")


@app.route('/registros', methods=['POST'])
def recibir_registro():
    api_key = request.headers.get('API-Key')
    if api_key != API_KEY:
        return jsonify({'error': 'Clave API no válida'}), 403

    data = request.json
    personaje = data['personaje']
    evento = data['evento']
    descripcion = data['descripcion']
    timestamp = data['timestamp']

    cur.execute('''
        INSERT INTO registros (personaje, evento, descripcion, timestamp)
        VALUES (%s, %s, %s, %s)
    ''', (personaje, evento, descripcion, timestamp))
    conn.commit()

    return jsonify({'mensaje': 'Registro recibido'}), 201


@app.route('/registros', methods=['GET'])
def obtener_registros():
    tipo_evento = request.args.get('evento')
    timestamp = request.args.get('timestamp')

    query = 'SELECT * FROM registros WHERE 1=1'
    params = []

    if tipo_evento:
        query += ' AND evento=%s'
        params.append(tipo_evento)
    if timestamp:
        query += ' AND timestamp=%s'
        params.append(timestamp)

    cur.execute(query, tuple(params))
    registros = cur.fetchall()

    return jsonify(registros), 200


if __name__ == '__main__':
    app.run(debug=True)
