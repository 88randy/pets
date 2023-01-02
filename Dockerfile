FROM python:3.11.1-bullseye

# Crea un directorio para la aplicación
RUN mkdir /app

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Actualiza pip
RUN python -m pip install --upgrade pip

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt --no-color

# Copia el código de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Vincula el directorio de tu computadora con el directorio de datos del contenedor

#VOLUME . /app/data

# Ejecuta la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Para hacer migraciones ejecutar docker exec -it myapp /bin/bash y a continuacion ejecutar migraciones

# Para construir la imagen  docker build -t pets .
# docker run -p 8000:8000 -d --name pets-django pets