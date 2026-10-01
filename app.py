import customtkinter as ctk


# =========================
# CONFIGURACIÓN
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================
# VENTANA PRINCIPAL
# =========================

app = ctk.CTk()

app.title("MEDIFY AI")
app.geometry("900x600")
app.minsize(800, 550)


# =========================
# COLORES
# =========================

FONDO = "#0B1120"
PANEL = "#111827"
AZUL = "#2563EB"
AZUL_HOVER = "#1D4ED8"
TEXTO = "#F8FAFC"
SECUNDARIO = "#94A3B8"
VERDE = "#22C55E"


app.configure(fg_color=FONDO)


# =========================
# CONTENEDOR PRINCIPAL
# =========================

contenedor = ctk.CTkFrame(
    app,
    fg_color=FONDO
)

contenedor.pack(
    fill="both",
    expand=True,
    padx=50,
    pady=40
)


# =========================
# ENCABEZADO
# =========================

titulo = ctk.CTkLabel(
    contenedor,
    text="MEDIFY AI",
    font=ctk.CTkFont(
        family="Arial",
        size=34,
        weight="bold"
    ),
    text_color=TEXTO
)

titulo.pack(pady=(10, 5))


subtitulo = ctk.CTkLabel(
    contenedor,
    text="Clasificación y organización inteligente de documentos",
    font=ctk.CTkFont(
        family="Arial",
        size=16
    ),
    text_color=SECUNDARIO
)

subtitulo.pack(pady=(0, 30))


# =========================
# PANEL CENTRAL
# =========================

panel = ctk.CTkFrame(
    contenedor,
    fg_color=PANEL,
    corner_radius=18
)

panel.pack(
    fill="both",
    expand=True
)


# =========================
# ICONO / ÁREA VISUAL
# =========================

icono = ctk.CTkLabel(
    panel,
    text="📄",
    font=ctk.CTkFont(size=55)
)

icono.pack(pady=(35, 10))


texto_principal = ctk.CTkLabel(
    panel,
    text="Organiza tus documentos automáticamente",
    font=ctk.CTkFont(
        family="Arial",
        size=21,
        weight="bold"
    ),
    text_color=TEXTO
)

texto_principal.pack()


descripcion = ctk.CTkLabel(
    panel,
    text="Selecciona documentos PDF o imágenes y MEDIFY AI\n"
         "identificará y clasificará cada archivo automáticamente.",
    font=ctk.CTkFont(
        family="Arial",
        size=14
    ),
    text_color=SECUNDARIO,
    justify="center"
)

descripcion.pack(pady=(8, 25))


# =========================
# BOTÓN SELECCIONAR
# =========================

boton_seleccionar = ctk.CTkButton(
    panel,
    text="📁  Seleccionar documentos",
    width=260,
    height=45,
    corner_radius=10,
    fg_color=AZUL,
    hover_color=AZUL_HOVER,
    font=ctk.CTkFont(
        size=15,
        weight="bold"
    )
)

boton_seleccionar.pack(pady=8)


# =========================
# CONTADOR
# =========================

contador = ctk.CTkLabel(
    panel,
    text="Documentos seleccionados: 0",
    font=ctk.CTkFont(size=14),
    text_color=SECUNDARIO
)

contador.pack(pady=(8, 20))


# =========================
# BOTÓN PROCESAR
# =========================

boton_procesar = ctk.CTkButton(
    panel,
    text="🚀  Procesar documentos",
    width=260,
    height=45,
    corner_radius=10,
    fg_color=VERDE,
    hover_color="#16A34A",
    text_color="#FFFFFF",
    font=ctk.CTkFont(
        size=15,
        weight="bold"
    )
)

boton_procesar.pack(pady=8)


# =========================
# ESTADO
# =========================

estado = ctk.CTkLabel(
    panel,
    text="●  Sistema listo",
    font=ctk.CTkFont(size=14),
    text_color=VERDE
)

estado.pack(pady=(25, 10))


# =========================
# PIE
# =========================

pie = ctk.CTkLabel(
    contenedor,
    text="MEDIFY AI  •  Intelligent Document Processing",
    font=ctk.CTkFont(size=12),
    text_color="#64748B"
)

pie.pack(pady=(15, 0))


# =========================
# INICIAR
# =========================

app.mainloop()
