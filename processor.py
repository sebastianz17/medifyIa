import os
import shutil
from pathlib import Path

from PIL import Image

from gemini_service import analizar_documento
from logger import registrar_proceso


EXTENSIONES_PERMITIDAS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
}


# =========================
# CARPETAS
# =========================

DESCARGAS = Path.home() / "Downloads"

CARPETA_MEDIFY = DESCARGAS / "MEDIFY_AI"

CARPETA_SALIDA = CARPETA_MEDIFY / "PROCESADOS"

CARPETA_SALIDA.mkdir(
    parents=True,
    exist_ok=True
)


# =========================
# PROCESAR ARCHIVO
# =========================

def procesar_archivo(ruta_archivo):

    nombre_original = os.path.basename(ruta_archivo)

    print(f"\nProcesando: {nombre_original}")

    try:

        # =========================
        # ANALISIS CON GEMINI
        # =========================

        resultado = analizar_documento(ruta_archivo)

        identificacion = resultado["identificacion"]

        clasificacion = resultado["clasificacion"]


        # =========================
        # NOMBRE FINAL
        # =========================

        nuevo_nombre = (
            f"{identificacion}_"
            f"{clasificacion}.pdf"
        )


        ruta_salida = CARPETA_SALIDA / nuevo_nombre


        extension = Path(ruta_archivo).suffix.lower()


        # =========================
        # SI ES PDF
        # =========================

        if extension == ".pdf":

            shutil.move(
                ruta_archivo,
                ruta_salida
            )


        # =========================
        # SI ES IMAGEN
        # CONVERTIR A PDF
        # =========================

        else:

            imagen = Image.open(ruta_archivo)

            if imagen.mode != "RGB":

                imagen = imagen.convert("RGB")


            imagen.save(
                ruta_salida,
                "PDF",
                resolution=100.0
            )


            # Eliminar imagen original
            os.remove(ruta_archivo)


        # =========================
        # REGISTRAR LOG
        # =========================

        datos = {
            "archivo_original": nombre_original,
            "identificacion": identificacion,
            "clasificacion": clasificacion,
            "archivo_generado": nuevo_nombre,
            "estado": "OK",
            "detalle": "Documento procesado correctamente"
        }


        registrar_proceso(datos)


        print(
            f"Identificacion: {identificacion}"
        )

        print(
            f"Clasificacion: {clasificacion}"
        )

        print(
            f"Archivo generado: {nuevo_nombre}"
        )

        print(
            f"Guardado en: {ruta_salida}"
        )

        print("Estado: OK")


        return datos


    except Exception as e:

        datos = {
            "archivo_original": nombre_original,
            "identificacion": "",
            "clasificacion": "",
            "archivo_generado": "",
            "estado": "ERROR",
            "detalle": str(e)
        }


        registrar_proceso(datos)


        print(f"ERROR: {e}")


        return datos


# =========================
# PROCESAR ENTRADA
# =========================

def procesar_entrada():

    carpeta_entrada = "entrada"

    os.makedirs(
        carpeta_entrada,
        exist_ok=True
    )


    archivos = []


    for archivo in os.listdir(
        carpeta_entrada
    ):

        ruta = os.path.join(
            carpeta_entrada,
            archivo
        )


        if not os.path.isfile(ruta):

            continue


        extension = os.path.splitext(
            archivo
        )[1].lower()


        if extension in EXTENSIONES_PERMITIDAS:

            archivos.append(ruta)


    if not archivos:

        print(
            "No hay documentos para procesar en entrada."
        )

        return


    print(
        f"\nDocumentos encontrados: {len(archivos)}"
    )


    for archivo in archivos:

        procesar_archivo(archivo)


    print(
        "\nProcesamiento finalizado."
    )


if __name__ == "__main__":

    procesar_entrada()
