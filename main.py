from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
import shutil
import os
import zipfile

from logger import registrar_proceso, ARCHIVO_LOG


app = FastAPI(
    title="MEDIFY AI",
    description="Sistema inteligente para clasificación y organización documental",
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent

if os.getenv("VERCEL"):
    ENTRADA_DIR = Path("/tmp/medify_entrada")
    PROCESADOS_DIR = Path("/tmp/medify_procesados")
    ZIP_DIR = Path("/tmp/medify_zip")
else:
    ENTRADA_DIR = BASE_DIR / "entrada"
    PROCESADOS_DIR = BASE_DIR / "PROCESADOS"
    ZIP_DIR = BASE_DIR / "PROCESADOS"


ENTRADA_DIR.mkdir(parents=True, exist_ok=True)
PROCESADOS_DIR.mkdir(parents=True, exist_ok=True)
ZIP_DIR.mkdir(parents=True, exist_ok=True)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def inicio():

    archivo_html = BASE_DIR / "templates" / "index.html"

    return archivo_html.read_text(encoding="utf-8")


@app.get("/health")
def health():

    return {
        "estado": "OK",
        "sistema": "MEDIFY AI"
    }


@app.post("/upload")
async def subir_archivos(
    files: list[UploadFile] = File(...)
):

    archivos_guardados = []

    extensiones_permitidas = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    }

    for archivo in files:

        extension = Path(archivo.filename).suffix.lower()

        if extension not in extensiones_permitidas:
            continue

        ruta = ENTRADA_DIR / archivo.filename

        with open(ruta, "wb") as buffer:

            shutil.copyfileobj(
                archivo.file,
                buffer
            )

        archivos_guardados.append(archivo.filename)

    return {
        "estado": "OK",
        "archivos": archivos_guardados,
        "cantidad": len(archivos_guardados)
    }


@app.post("/procesar")
def procesar_documentos():

    from web_processor import procesar_archivo_web

    extensiones_permitidas = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    }

    archivos = [
        archivo
        for archivo in ENTRADA_DIR.iterdir()
        if archivo.is_file()
        and archivo.suffix.lower() in extensiones_permitidas
    ]

    if not archivos:

        return {
            "estado": "ERROR",
            "mensaje": "No hay documentos para procesar."
        }

    resultados = []

    for archivo in archivos:

        try:

            resultado = procesar_archivo_web(
                str(archivo)
            )

            resultados.append(resultado)

        except Exception as e:

            print(
                f"ERROR PROCESANDO {archivo.name}: {e}"
            )

            resultados.append({
                "archivo_original": archivo.name,
                "estado": "ERROR",
                "detalle": str(e)
            })

    exitosos = [
        resultado
        for resultado in resultados
        if resultado.get("estado") == "OK"
    ]

    if not exitosos:

        return {
            "estado": "ERROR",
            "mensaje": "No se pudo procesar ningún documento.",
            "resultados": resultados
        }

    archivos_procesados = []

    for resultado in exitosos:

        origen = Path(resultado["ruta_salida"])

        destino = (
            PROCESADOS_DIR /
            resultado["archivo_generado"]
        )

        shutil.copy2(
            origen,
            destino
        )

        registrar_proceso({
            "archivo_original": resultado["archivo_original"],
            "identificacion": resultado["identificacion"],
            "clasificacion": resultado["clasificacion"],
            "archivo_generado": resultado["archivo_generado"],
            "estado": "OK",
            "detalle": "Documento procesado correctamente"
        })

        archivos_procesados.append(
            destino
        )

    # Copiar el LOG al directorio PROCESADOS
    log_destino = PROCESADOS_DIR / "LOG.xlsx"

    if ARCHIVO_LOG.exists():
        shutil.copy2(
            ARCHIVO_LOG,
            log_destino
        )

    nombre_zip = "MEDIFY_AI_PROCESADOS.zip"

    ruta_zip = ZIP_DIR / nombre_zip

    if ruta_zip.exists():
        ruta_zip.unlink()

    with zipfile.ZipFile(
        ruta_zip,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_archivo:

        for archivo in archivos_procesados:

            zip_archivo.write(
                archivo,
                arcname=archivo.name
            )

        if log_destino.exists():

            zip_archivo.write(
                log_destino,
                arcname="LOG.xlsx"
            )

    return {
        "estado": "OK",
        "cantidad": len(archivos_procesados),
        "archivos": [
            archivo.name
            for archivo in archivos_procesados
        ],
        "log": "LOG.xlsx",
        "descarga": f"/descargar-zip/{nombre_zip}"
    }


@app.get("/descargar-zip/{nombre_archivo}")
def descargar_zip(nombre_archivo: str):

    archivo = ZIP_DIR / Path(nombre_archivo).name

    if not archivo.exists():

        return {
            "estado": "ERROR",
            "mensaje": "Archivo ZIP no encontrado."
        }

    return FileResponse(
        archivo,
        media_type="application/zip",
        filename=archivo.name
    )
