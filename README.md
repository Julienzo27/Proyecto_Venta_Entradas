# Proyecto Venta de Entradas

Este repositorio contiene un prototipo de sistema de ventas de entradas (Flask + SQLite) organizado en tres capas: dominio, repositorios y servicios. El proyecto ya está preparado para desplegar en Replit.

Este README explica exactamente los comandos (PowerShell) para ejecutar localmente, publicar en GitHub y luego importar el proyecto en Replit.

---

## Requisitos locales
- Python 3.11+ (se probó con 3.13 en el entorno de desarrollo)
- Git (para subir a GitHub)
- (Opcional) GitHub CLI `gh` para crear el repo desde la terminal

## Estructura principal
- `app.py` — aplicación Flask (rutas web)
- `create_db.py` — crea `db.sqlite3` y aplica seed; exporta `init_db()`
- `repositorios/sqlite_repos.py` — implementación SQLite de los repositorios
- `servicios/servicio_entradas.py` — lógica del dominio y validaciones
- `templates/` — vistas Jinja2 (extienden `base.html`)
- `css/estilos.css` — estilos usados por las plantillas
- `requirements.txt` — dependencias para Replit / despliegue
- `.replit` — comando de ejecución (opcional, usado por Replit)

---

## Ejecutar localmente (PowerShell)
1. Abrir PowerShell en la carpeta del proyecto:
```powershell
cd C:\Users\maria\Documents\Proyecto_Venta_Entradas
```

2. Activar el entorno virtual del proyecto (si existe):
```powershell
# Si usas el entorno creado en este repo
.\.venv\Scripts\Activate.ps1
# Si prefieres crear uno nuevo:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Crear / inicializar la base de datos (solo la primera vez o para reset):
```powershell
python create_db.py
# deberías ver: "db.sqlite3 creada/actualizada y semilla aplicada"
```

4. Ejecutar la aplicación (entorno de desarrollo):
```powershell
python app.py
```
Abre en el navegador `http://127.0.0.1:5000`.

Rutas principales a probar:
- `/` -> menú
- `/eventos` -> listar/crear/editar/eliminar eventos
- `/clientes` -> listar/crear/editar/eliminar clientes
- `/entradas` -> emitir entradas

---

## Tests rápidos (cliente de prueba Flask)
Hay tests de humo que utilizan `app.test_client()`:
```powershell
python test_app.py
python test_pages.py
python test_events.py
python test_delete_client.py
python test_delete_event.py
```

---

## Preparar repo y subir a GitHub (PowerShell)
A continuación los comandos exactos para crear un repo localmente y subirlo a GitHub (sin usar la UI). Sustituí `TU_USUARIO` y `NOMBRE_REPO` por los tuyos.

### Opción A — usar GitHub Web (más simple)
1. Crear repo nuevo en GitHub (https://github.com/new). No marques README ni .gitignore (ya existen localmente).
2. Luego, desde PowerShell en la carpeta del proyecto:
```powershell
git init
git add .
git commit -m "Inicial: preparar despliegue a Replit"
# Reemplaza la URL por la del repo que creaste en GitHub
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git
git branch -M main
git push -u origin main
```

### Opción B — usar GitHub CLI (`gh`) para crear y pushear en un solo paso
(Si no tienes `gh`, instálalo desde https://cli.github.com/)
```powershell
git init
git add .
git commit -m "Inicial: preparar despliegue a Replit"
# Crea repo en GitHub y pushea el código
gh repo create TU_USUARIO/NOMBRE_REPO --public --source=. --remote=origin --push
```

---

## Importar el proyecto en Replit (desde GitHub)
1. Ve a https://replit.com y logueate.
2. Haz clic en "Create" / "New Repl".
3. Elige "Import from GitHub" y pega la URL del repo (o busca tu repo si conectaste tu cuenta de GitHub).
4. Replit detectará `requirements.txt` e instalará dependencias.
5. En `Secrets` (Environment variables) agrega:
   - `SECRET_KEY` = (una cadena larga aleatoria)
   - Opcional: `FLASK_DEBUG` = 0
6. Si la importación no crea automáticamente un Run command correcto, en la pestaña `Tools` -> `Replit` -> `Run` configura el comando de ejecución como:
```text
python create_db.py && python app.py
```
7. Pulsa Run y abre la URL pública que Replit provee. Las rutas y UI estarán disponibles tal como en local.

---

## Importar el proyecto en Replit (subiendo archivos manualmente)
Si prefieres no usar GitHub, crea un Repl Python vacío y sube los archivos (Upload) desde la interfaz. Luego instala dependencias en el Shell:
```bash
pip install -r requirements.txt
```
Y configura el comando Run como arriba.

---

## Variables de entorno y seguridad
- Usa Replit Secrets para `SECRET_KEY` (no lo pongas en el código en producción).
- Si necesitas otras credenciales, guárdalas en Secrets.

---

## Notas finales y recomendaciones
- SQLite es suficiente para prototipos. Si vas a recibir tráfico concurrente o quieres datos compartidos entre instancias, considera migrar a PostgreSQL u otro servicio gestionado.
- Para producción considera usar SQLAlchemy y gestionar migraciones con Alembic.
- Si querés, puedo prepararte un `README` más corto para presentar el proyecto o puedo crear el repo en GitHub por vos si me das el nombre del repo y confirmás que vas a subir desde tu cuenta (yo te daré los comandos; no puedo usar tus credenciales).

---

Si querés que haga la importación por ti, dame la URL de tu repo en GitHub (si ya lo subiste) o confírmame que querés que te guíe paso a paso en la consola (puedo darte los comandos y validar la salida). No puedo interactuar con la interfaz web de Replit desde aquí, pero puedo ejecutar y validar todo lo necesario dentro de este workspace y prepararte los pasos exactos para pegar en Replit.
