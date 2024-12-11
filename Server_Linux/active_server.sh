#!/bin/bash

# 起始端口号
START_PORT=4000
# 需要开放的端口数量
PORT_COUNT=65

# 循环从起始端口号开始，增加PORT_COUNT次
for (( i=0; i<PORT_COUNT; i++ ))
do
    # 计算当前端口号
    PORT=$((START_PORT - i))
    # 使用ufw允许当前端口
    sudo ufw allow $PORT/tcp
    echo "Port $PORT/tcp has been allowed."

    # 运行Python脚本并指定端口
    nohup python file_transfer_server.py $PORT > /dev/null 2>&1 &
    echo "file_transfer_server.py is running on port $PORT"
done

echo "All ports from $START_PORT to $((START_PORT - PORT_COUNT + 1)) have been allowed and file_transfer_server.py is running on each port."

