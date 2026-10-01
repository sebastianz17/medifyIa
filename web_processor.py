import os
from pathlib import Path

from PIL import Image

from gemini_service import analizar_documento


def procesar_archivo_web(ruta_archivo):

    ruta_archivo = Path(ruta_archivo)

    nombre_original = ruta_archivo.name

    resultado = analizar_documento(
        str(ruta_archivo)
    )

    identificacion = resultado["identificacion"]

    clasificacion = resultado["clasificacion"]

    nuevo_nombre = (
        f"{identificacion}_"
        f"{clasificacion}.pdf"
    )

    carpeta_temporal = Path(
        os.getenv(
            "TMPDIR",
            os.getenv(
                "TEMP",
                "/tmp"
            )
        )
    )

    carpeta_temporal.mkdir(
        parents=True,
        exist_ok=True
    )

    ruta_salida = (
        carpeta_temporal
        / nuevo_nombre
    )

    extension = ruta_archivo.suffix.lower()

    if extension == ".pdf":

        with open(
            ruta_archivo,
            "rb"
        ) as archivo_entrada:

            with open(
                ruta_salida,
                "wb"
            ) as archivo_salida:

                archivo_salida.write(
                    archivo_entrada.read()
                )

    else:

        imagen = Image.open(
            ruta_archivo
        )

        if imagen.mode != "RGB":

            imagen = imagen.convert("RGB")

        imagen.save(
            ruta_salida,
            "PDF",
            resolution=100.0
        )

    return {
        "archivo_original": nombre_original,
        "identificacion": identificacion,
        "clasificacion": clasificacion,
        "archivo_generado": nuevo_nombre,
        "ruta_salida": str(ruta_salida),
        "estado": "OK"
    }
