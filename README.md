# Proyecto: Gestión Docente

## Descripción

Este README detalla los pasos necesarios para configurar y ejecutar el proyecto de Django **Gestión Docente**. Asegúrese de seguir cada paso cuidadosamente para garantizar una configuración correcta.

---

## Requisitos Previos

### Editor de Código
Tener instalado un editor de código. Se recomienda **Visual Studio Code (VSC)**.

### Git
Tener instalado Git. [Descargar Git](https://git-scm.com/).

### Python
Tener instalado Python 3.11 o superior. [Descargar Python](https://www.python.org/).

### Instalación de SQLiteDatabaseBrowserPortable en Windows

1. Descargar **SQLiteDatabaseBrowserPortable** desde el siguiente enlace:
   - [Página oficial de descargas de SQLiteDatabaseBrowserPortable](https://github.com/sqlitebrowser/sqlitebrowser/releases).

2. Extraer el archivo descargado:
   - Si el archivo descargado es un archivo `.zip`, haz clic derecho sobre él y selecciona **Extraer todo** para descomprimirlo.

3. Navegar a la carpeta extraída.

4. Ejecutar el programa:
   - Dentro de la carpeta extraída, busca el archivo ejecutable **SQLiteDatabaseBrowserPortable.exe** y haz doble clic para ejecutar el programa.

### Entorno Ubuntu
Tener un entorno Ubuntu, ya sea:
- Como sistema operativo principal.
- Usando WSL (Windows Subsystem for Linux). [Configurar WSL](https://learn.microsoft.com/es-es/windows/wsl/install).

### Guía de Instalación de Dependencias para Automatización Web en WSL
**Instalar Python y pip**  
Si no tienes Python y pip instalados en tu entorno WSL, instálalos con los siguientes comandos:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Instalar Google Chrome y Chromium en WSL**  
Para comenzar, debes instalar Google Chrome o Chromium en tu entorno WSL.
1. Instalar Chromium  
```bash
sudo apt update
sudo apt install chromium-browser
```

2. Instalar Google Chrome
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```
3. Instalar Chromedriver en WSL
Una vez que tengas instalado Chromium o Google Chrome, debes instalar Chromedriver, que es necesario para controlar el navegador con Selenium.
```bash
sudo apt install chromium-chromedriver
```

4. Verificar las instalaciones
Para asegurarte de que todo esté instalado correctamente, verifica las versiones de Chromium y ChromeDriver:
```bash
chromium-browser --version
chromedriver --version
google-chrome --version
```

5. Verificar la instalación del navegador y Chromedriver
Para asegurarte de que Google Chrome o Chromium y Chromedriver estén correctamente instalados, puedes ejecutar los siguientes comandos:
```bash
which chromedriver
```
Pega la ruta que obtengas al ejecutar este comando en tu código, para asegurarte de que Selenium pueda localizar el ejecutable de Chromedriver.

---

## Configuración Inicial

### Clonar el Repositorio
Clone el repositorio y acceda a la carpeta creada:
```bash
git clone https://github.com/g93624829/gestion_docente.git
cd gestion_docente
```

### Abrir Carpeta en VSC
Abra la carpeta con **Visual Studio Code**.

### Configurar Terminal en Ubuntu
Si está utilizando WSL, abra una nueva terminal en VSC y elija **Ubuntu (WSL)** como entorno.

---

## Configuración del Entorno Virtual

### Crear un Entorno Virtual
En la carpeta raíz del proyecto, ejecute:
```bash
python -m venv venv
```

### Activar el Entorno Virtual
Active el entorno virtual:
```bash
source venv/bin/activate
```

### Verificar Versiones
Compruebe la versión de Python dentro del entorno virtual:
```bash
python --version
```

Compruebe la versión de pip:
```bash
pip --version
```

### Instalar Dependencias
Instale las dependencias del proyecto:
```bash
pip install -r requirements.txt
```

---

## Configuración y Ejecución del Proyecto

### Iniciar el Servidor de Desarrollo
Inicie el servidor de Django:
```bash
python manage.py runserver
```

Acceda al enlace que genera (generalmente [http://127.0.0.1:8000/](http://127.0.0.1:8000/)) en su navegador.

### Preparar la Base de Datos
1. Vuelva a la terminal y cancele el servidor con `CTRL + C`.
2. Ejecute las migraciones necesarias:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Crear un Superusuario
1. **Crea el Superusuario y llenar las tablas en Django**  
   Ejecuta el siguiente comando en la terminal del servidor:
   ```bash
   python manage.py createsuperuser
   ```
   Proporcione:
   - **Username:** usuario
   - **Email:** test@test.com
   - **Password:** contrasenia

   Ejecute el siguiente comando en la terminal del servidor:
   ```bash
   python manage.py loaddata autenticacion/fixtures/carreras_cursos.json
   ```
   Ese comando hace lo siguiente:
   - Agregar el superusuario a la tabla miperfil, permitiéndole acceder a la plataforma.
   - Registrar las carreras de los alumnos.
   - Asignar los cursos que enseñan los profesores."
   Proporcione:

2. **Confirmación en Django**  
   Ejecuta el servidor para verificar que ya no recibes el error 404:
   ```bash
   python manage.py runserver
   ```

3. **Vista de tablas**  
   Usando el programa **SQLiteDatabaseBrowserPortable**, abre el archivo `db.sqlite3` que se creó en la carpeta raíz. Luego, haz clic en **Browse Data** y seleccione una tabla, deben verse de forma similar a esto: 
   
**Tabla `auth_user`** estos datos fueron creados por el `python manage.py createsuperuser` en el paso 1 **Crea el Superusuario en Django**:

|id|password                                                                                |last_login                |is_superuser|username|last_name|email        |is_staff|is_active|date_joined|first_name|
|--|----------------------------------------------------------------------------------------|--------------------------|------------|--------|---------|-------------|--------|---------|-----------|----------|
|1 |pbkdf2_sha256$870000$HPUOMBUALaZ2mG4g6l4Zj5$AFRisklmhRrlljsAOuIExLiy5xgkP/qQLIi6jxYq6U8=|2024-12-13 14:37:16.613512|1           |usuario |         |test@test.com|1       |1        |2024-11-21 20:08:36.580194||

**Tabla `autenticacion_miperfil`** estos datos fueron creados por el codigo de `sql` en el paso 4 **Inserta el Registro en MiPerfil**:

|id|dni     |tipo_usuario |nombre_usuario|correo_electronico|descripcion                       |numero_telefono|user_id|
|--|--------|-------------|--------------|------------------|----------------------------------|---------------|-------|
| 1|87654321|supervisor(a)|usuario       |test@test.com     |Este es el perfil del superusuario|987654321      |1      |

### Iniciar sesión
1. Ingresa a la página a través del `http://127.0.0.1:8000/`
2. Hace click en el boton de Iniciar Sesión
3. Ingresa sus credenciales creados: **USUARIO**: test@test.com, **CONTRASEÑA**: contrasenia

---

## Notas

- Recuerde activar siempre el entorno virtual antes de ejecutar cualquier comando relacionado con el proyecto.
- Si experimenta problemas con dependencias, asegúrese de que todas estén instaladas correctamente desde el archivo `requirements.txt`.
