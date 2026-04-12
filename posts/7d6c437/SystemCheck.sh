#!/bin/bash
#定义文件数量
function setNofile() {
cat << EOF >>/etc/security/limits.conf
* soft nofile 65535
* hard nofile 65535
EOF
}

#设置时间自动同步任务
if crontab -l | grep ntpdate; then
    echo "时间任务已设置，无需再次设置"
elif ! crontab -l | grep ntpdate; then
    (echo "* 1 * * * ntpdate time.windows.com >/dev/null 2>&1"; crontab -l)|crontab    
    echo "时间同步任务设置成功"#此处缺判断，运行失败时也会回成功，下方报失败实际无效
else 
    echo "时间任务设置失败"
fi

#设置文件打开数量
if grep "soft nofile 65535" /etc/security/limits.conf >/dev/null; then
    echo "文件数量已设置，无需再次设置"
elif !  grep "soft nofile 65535" /etc/security/limits.conf >/dev/null; then
    setNofile
    echo "文件数量设置成功"
else
    echo "文件数量设置失败"
fi
