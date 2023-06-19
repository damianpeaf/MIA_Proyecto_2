# Obtener el ID del proceso asociado al puerto 8000
OLD_PID=$(lsof -t -i :8000)

# Matar el proceso anterior si existe
if [[ -n $OLD_PID ]]; then
    echo "Matando el proceso anterior en el puerto 8000: $OLD_PID"
    kill $OLD_PID
fi