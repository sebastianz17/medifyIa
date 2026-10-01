const fileInput = document.getElementById("fileInput");
const selectButton = document.getElementById("selectButton");
const fileList = document.getElementById("fileList");
const fileCount = document.getElementById("fileCount");
const processButton = document.getElementById("processButton");
const message = document.getElementById("message");

let archivosSeleccionados = [];

selectButton.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", async () => {

    archivosSeleccionados = Array.from(fileInput.files);

    mostrarArchivos();

    if (archivosSeleccionados.length === 0) {
        return;
    }

    const formData = new FormData();

    archivosSeleccionados.forEach(file => {
        formData.append("files", file);
    });

    message.textContent = "Cargando documentos...";

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const resultado = await response.json();

        if (resultado.estado === "OK") {

            message.textContent =
                "OK - " +
                resultado.cantidad +
                " documento(s) cargado(s).";

        } else {

            message.textContent =
                "ERROR - No se pudieron cargar los documentos.";

        }

    } catch (error) {

        console.error(error);

        message.textContent =
            "ERROR - No se pudo conectar con el servidor.";

    }

});


function mostrarArchivos() {

    fileList.innerHTML = "";

    fileCount.textContent =
        archivosSeleccionados.length;

    archivosSeleccionados.forEach(file => {

        const item =
            document.createElement("div");

        item.className =
            "file-item";

        item.textContent =
            "PDF/IMG - " + file.name;

        fileList.appendChild(item);

    });

}


processButton.addEventListener("click", async () => {

    if (archivosSeleccionados.length === 0) {

        message.textContent =
            "Selecciona documentos para comenzar.";

        return;
    }

    processButton.disabled = true;

    processButton.textContent =
        "Procesando con IA...";

    message.textContent =
        "MEDIFY AI esta analizando los documentos...";

    try {

        const response =
            await fetch("/procesar", {
                method: "POST"
            });

        const resultado =
            await response.json();

        if (!response.ok ||
            resultado.estado !== "OK") {

            throw new Error(
                resultado.mensaje ||
                "No se pudieron procesar los documentos."
            );

        }

        message.textContent =
            "OK - " +
            resultado.cantidad +
            " documento(s) procesado(s).";

        const enlace =
            document.createElement("a");

        enlace.href =
            resultado.descarga;

        enlace.download =
            "MEDIFY_AI_PROCESADOS.zip";

        document.body.appendChild(enlace);

        enlace.click();

        enlace.remove();

        fileList.innerHTML = "";

        archivosSeleccionados = [];

        fileInput.value = "";

        fileCount.textContent = "0";

    } catch (error) {

        console.error(
            "ERROR PROCESANDO:",
            error
        );

        message.textContent =
            "ERROR - " + error.message;

    } finally {

        processButton.disabled = false;

        processButton.textContent =
            "Procesar documentos";

    }

});


