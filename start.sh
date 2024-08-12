# app.pyを実行する過程を自動化

PORT = 8050
PID = $(lsof -t -i:$PORT)
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "Killed process $PID on port $PORT"
fi
python3 ./app.py