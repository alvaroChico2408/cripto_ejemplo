# Guía para Desplegar una Aplicación Flask

Este documento describe los pasos necesarios para configurar y desplegar una aplicación Flask en tu entorno local.

## Requisitos previos

- Python 3.7 o superior instalado.

---

## Pasos para el despliegue

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local:

### 2. Crear un entorno virtual
Crea un entorno virtual para aislar las dependencias del proyecto:

```bash
python -m venv venv
```

### 3. Activar el entorno virtual
Activa el entorno virtual que acabas de crear:

- En Windows:
  ```bash
  venv\Scripts\activate
  ```
  
Cuando el entorno virtual esté activo, verás el prefijo `(venv)` en tu terminal.

### 4. Instalar dependencias
Instala las dependencias necesarias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación Flask
Inicia el servidor Flask ejecutando el archivo principal de la aplicación. 

```bash
flask run
```

---
