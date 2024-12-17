# # Usa Ubuntu como imagen base
# FROM ubuntu:22.04

# # Configura las variables de entorno para evitar preguntas durante la instalación
# ENV DEBIAN_FRONTEND=noninteractive
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Instala dependencias del sistema
# RUN apt-get update && apt-get install -y \
#     python3-pip \
#     python3-dev \
#     python3-venv \
#     build-essential \
#     libpq-dev \
#     sqlite3 \
#     wget \
#     curl \
#     gnupg \
#     git \
#     chromium-browser \
#     chromium-chromedriver \
#     libgconf-2-4 \
#     libnss3 \
#     libx11-xcb1 \
#     libgbm1 \
#     libasound2 \
#     lsb-release \
#     && apt-get clean

# # Añadir el repositorio de Google Chrome
# RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update \
#     && apt-get install -y google-chrome-stable \
#     && apt-get clean

# # Establece el directorio de la aplicación
# WORKDIR /app

# # Copia el archivo de dependencias
# COPY requirements.txt .

# # Configura el entorno virtual e instala dependencias de Python
# RUN python3 -m venv venv \
#     && . venv/bin/activate \
#     && pip install --upgrade pip \
#     && pip install -r requirements.txt

# # Copia todo el código fuente al contenedor
# COPY . .

# # Instalar las librerías de Python necesarias (Selenium y BeautifulSoup)
# RUN . venv/bin/activate && pip install selenium beautifulsoup4

# # Establecer las variables de entorno para el navegador y el ChromeDriver
# ENV CHROME_BIN=/usr/bin/google-chrome
# ENV CHROMEDRIVER_PATH=/usr/lib/chromium-browser/chromedriver

# # Exponer el puerto 8000 para Django (si es necesario)
# EXPOSE 8000

# # Realizar migraciones, crear el superusuario y cargar los datos
# RUN . venv/bin/activate && python manage.py makemigrations
# RUN . venv/bin/activate && python manage.py migrate
# RUN . venv/bin/activate && python manage.py shell -c "from django.contrib.auth.models import User; \
#     User.objects.create_superuser(username='usuario', email='test@test.com', password='contrasenia') \
#     if not User.objects.filter(username='usuario').exists() else print('El superusuario ya existe.');"
# RUN . venv/bin/activate && python manage.py loaddata autenticacion/fixtures/carreras_cursos.json



# # Comando para ejecutar el servidor de desarrollo o ejecutar tu script Python
# CMD ["sh", "-c", ". venv/bin/activate && python manage.py runserver 0.0.0.0:8000"]

# Usa Ubuntu como imagen base
FROM ubuntu:22.04

# Configura las variables de entorno para evitar preguntas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    libpq-dev \
    sqlite3 \
    wget \
    curl \
    gnupg \
    git \
    chromium-browser \
    chromium-chromedriver \
    libgconf-2-4 \
    libnss3 \
    libx11-xcb1 \
    libgbm1 \
    libasound2 \
    lsb-release \
    tzdata \
    && apt-get clean

# Añadir el repositorio de Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean

# Establece el directorio de la aplicación
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt .

# Configura el entorno virtual e instala dependencias de Python
RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . .

# Instalar las librerías de Python necesarias (Selenium y BeautifulSoup)
RUN . venv/bin/activate && pip install selenium beautifulsoup4

# Establecer las variables de entorno para el navegador y el ChromeDriver
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/lib/chromium-browser/chromedriver

# Exponer el puerto 8000 para Django (si es necesario)
EXPOSE 8000

# Realizar migraciones, crear el superusuario y cargar los datos
RUN . venv/bin/activate && python manage.py makemigrations
RUN . venv/bin/activate && python manage.py migrate
RUN . venv/bin/activate && python manage.py shell -c "from django.contrib.auth.models import User; \
    User.objects.create_superuser(username='usuario', email='test@test.com', password='contrasenia') \
    if not User.objects.filter(username='usuario').exists() else print('El superusuario ya existe.');"
RUN . venv/bin/activate && python manage.py loaddata autenticacion/fixtures/carreras_cursos.json

# Comando para ejecutar el servidor de desarrollo o ejecutar tu script Python
CMD ["sh", "-c", ". venv/bin/activate && python manage.py runserver 0.0.0.0:8000"]
