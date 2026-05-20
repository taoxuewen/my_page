#!/bin/bash

# 配置
APP_DIR="/usr/mypage"
APP_PY="app.py"
LOG_FILE="$APP_DIR/monitor.log"
CHECK_URL="http://127.0.0.1/"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查网站是否正常
check_website() {
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "$CHECK_URL")
    if [ "$HTTP_CODE" = "200" ]; then
        return 0  # 正常
    else
        return 1  # 异常
    fi
}

# 重启应用
restart_app() {
    log "网站异常，正在重启..."
    
    # 杀死所有运行中的python3 app.py进程
    pkill -f "python3.*$APP_PY" 2>/dev/null
    sleep 2
    
    # 确保进程已停止
    pkill -9 -f "python3.*$APP_PY" 2>/dev/null
    sleep 1
    
    # 进入应用目录并重启
    cd "$APP_DIR" || {
        log "无法进入目录 $APP_DIR"
        return 1
    }
    
    # 后台启动应用
    nohup python3 "$APP_PY" > /dev/null 2>&1 &
    sleep 3
    
    # 验证是否启动成功
    if check_website; then
        log "网站重启成功！"
        return 0
    else
        log "网站重启失败！"
        return 1
    fi
}

# 主逻辑
log "开始监控检查..."

if check_website; then
    log "网站运行正常"
else
    log "网站异常，HTTP状态码非200"
    restart_app
fi
