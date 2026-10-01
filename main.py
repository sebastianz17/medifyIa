from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import shutil

from processor import procesar_archivo


app = FastAPI(
    title="MEDIFY AI",
    description="Sistema inteligente para clasificación y organización documental",
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent

ENTRADA_DIR = BASE_DIR / "entrada"
PROCESADOS_DIR = BASE_DIR / "PROCESADOS"

ENTRADA_DIR.mkdir(exist_ok=True)
PROCESADOS_DIR.mkdir(exist_ok=True)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def inicio():

    archivo_html = BASE_DIR / "templates" / "index.html"

    return archivo_html.read_text(encoding="utf-8")


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

    resultados = []

    archivos = []

    extensiones_permitidas = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    }

    for archivo in ENTRADA_DIR.iterdir():

        if not archivo.is_file():
            continue

        if archivo.suffix.lower() in extensiones_permitidas:

            archivos.append(archivo)


    if not archivos:

        return {
            "estado": "ERROR",
            "mensaje": "No hay documentos para procesar."
        }


    for archivo in archivos:

        nombre_original = archivo.name

        try:

            procesar_archivo(str(archivo))

            resultados.append({
                "archivo": nombre_original,
                "estado": "OK"
            })

        except Exception as e:

            resultados.append({
                "archivo": nombre_original,
                "estado": "ERROR",
                "detalle": str(e)
            })


    return {
        "estado": "OK",
        "cantidad": len(resultados),
        "resultados": resultados
    }
