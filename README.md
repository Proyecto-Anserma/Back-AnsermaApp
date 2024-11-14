# Back-AnsermaApp
Backend del Sistema Integral de Información y Georreferenciación para la Gestión Social y Territorial en Anserma, Caldas

Debe contar con versión de Python 3.13.0 instalada (con la ruta de path activa)

# Correr en la terminal o consola:

### 1. Instalar dependencias

En powershell:
```bash
python -m venv venv
```

### 2. Activar el etorno virtual

-----------------------------

En bash:
```bash
source venv/Scripts/activate
```

En cmd:
```cmd
.\venv\Scripts\activate
```

-----------------------------

### 3. Instalar la librería mesa

```bash
pip install mesa
```

### 4. Instalar la librerias / requerimientos necesarias

```bash
pip install -r "requirements.txt"
```

### 5. Correr el programa

```bash
uvicorn src.main:app --port 5000 --reload
```