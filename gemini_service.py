import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY no encontrada")

client = genai.Client(api_key=api_key)


def analizar_documento(ruta_archivo):

    documento = client.files.upload(file=ruta_archivo)

    prompt = """
Analiza este documento de una IPS.

Extrae UNICAMENTE estos dos datos:

1. identificacion: numero de identificacion del paciente.
2. clasificacion: clasifica el documento usando SOLO una de estas opciones:

ORDEN_MEDICA
AUTORIZACION
FORMULA_MEDICA
REMISION
HISTORIA_CLINICA
OTRO

Si no encuentras la identificacion:
NO_IDENTIFICADA

Responde UNICAMENTE con JSON valido:

{
  "identificacion": "numero",
  "clasificacion": "CLASIFICACION"
}
"""

    for intento in range(1, 4):

        try:
            print(f"Intento Gemini: {intento}/3")

            response = client.models.generate_content(
                model=model,
                contents=[
                    documento,
                    prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            return json.loads(response.text)

        except errors.ServerError as e:

            print(f"Gemini devolvio error temporal: {e}")

            if intento < 3:
                print("Esperando 5 segundos antes de reintentar...")
                time.sleep(5)
            else:
                print("Gemini no estuvo disponible despues de 3 intentos.")
                raise