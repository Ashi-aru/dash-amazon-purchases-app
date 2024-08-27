# app.pyを実行する過程を自動化
# control + Cで中断するときちんとポートも閉じるみたい。
# control + Zで中断するとポートが開きっぱなしになり、python3 ./app.pyだとエラーを吐く

PORT=8050
PID=$(lsof -t -i:$PORT)
echo "$PID"
if [ ! -z "$PID" ]; then
    kill -9 $PID
    echo "Killed process $PID on port $PORT"
fi
# source venv_amazon/bin/activate
python3 ./app1.py
# deactivate