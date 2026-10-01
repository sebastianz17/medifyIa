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


    message.textContent =
        "Cargando documentos...";


    try {

        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );


        const resultado = await response.json();


        if (resultado.estado === "OK") {

            message.textContent =
                `✅ ${resultado.cantidad} documento(s) cargado(s).`;

        } else {

            message.textContent =
                "❌ No se pudieron cargar los documentos.";

        }


    } catch (error) {

        console.error(error);

        message.textContent =
            "❌ Error al conectar con el servidor.";

    }

});


function mostrarArchivos() {

    fileList.innerHTML = "";

    fileCount.textContent =
        archivosSeleccionados.length;


    archivosSeleccionados.forEach(file => {

        const item = document.createElement("div");

        item.className = "file-item";

        item.textContent =
            "📄 " + file.name;

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
        "MEDIFY AI está analizando los documentos...";


    try {

        const response = await fetch(
            "/procesar",
            {
                method: "POST"
            }
        );


        const resultado = await response.json();


        if (resultado.estado === "OK") {

            const exitosos =
                resultado.resultados.filter(
                    item => item.estado === "OK"
                ).length;


            message.textContent =
                `✅ Procesamiento terminado. ${exitosos} documento(s) procesado(s) correctamente.`;


            fileList.innerHTML = "";


            archivosSeleccionados = [];

            fileCount.textContent = "0";


        } else {

            message.textContent =
                `❌ ${resultado.mensaje}`;

        }


    } catch (error) {

        console.error(error);

        message.textContent =
            "❌ Error al procesar los documentos.";

    }


    processButton.disabled = false;

    processButton.textContent =
        "Procesar documentos";

});
