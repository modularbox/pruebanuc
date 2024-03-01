#!/bin/bash

# Verifica que se haya proporcionado un parámetro
if [ $# -eq 0 ]; then
    echo "Usage: $0 <commit_message>"
    exit 1
fi

# Agrega todos los cambios en el repositorio de Git
git add .

# Realiza un commit con el mensaje proporcionado como parámetro
git commit -m "$1"

# Sube los cambios al repositorio remoto
git push