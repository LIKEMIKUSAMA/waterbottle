#!/bin/bash
#CPU使用情况
cpuUse() {
    use=$(vmstat | awk '{if(NR==3) print $13+$14}') #使用
    iowait=$(vmstat | awk '{if(NR==3) print $16}')  #磁盘等待
    echo "cpu使用率：$use %，等待IO时长占用：$iowait %"
}
#内存使用情况
memory() {
    total=$(free -h | awk '{if(NR==2) print $2}')      #总计
    used=$(free -h | awk '{if(NR==2) print $3}')       #已用
    avaliable=$(free -h | awk '{if(NR==2) print $NF}') #可用
    echo "内存 合计：$total，已使用：$used，可用：$avaliable"
}
#磁盘情况
disk() {
    list=$(df -h | awk '/^\/dev/ {print $1}') #获取列表
    #遍历输出
    for i in $list; do
        mount=$(df -h | awk -v i=$i '$1==i {print $NF}') #挂载点
        used=$(df -h | awk -v i=$i '$1==i {print $3}')   #已用
        size=$(df -h | awk -v i=$i '$1==i {print $2}')   #总计
        avali=$(df -h | awk -v i=$i '$1==i {print $4}')  #剩余
        use=$(df -h | awk -v i=$i '$1==i {print $5}')    #已用空间占比（%）
        echo "硬盘    挂载：$mount，总大小：$size，已用：$used，占比：$use，可用：$avali"
    done
}
#tcp连接状态
tcp_stat() {
    tcpstatcount=$(netstat -natp | awk '{a[$6]++}END {for(i in a) print i,a[i] }')
    echo "TCP连接状态：$tcpstatcount"
}
#CPU使用前5
topcpu(){
    cpu=$(ps -eo pid,pcpu,pmem,args --sort=-pcpu|head -n 10)
    echo "***************************"
    echo "******    CPUTOP5   *******"
    echo "***************************"
    $cpu
}
#内存使用前5
topmem() {
    mem=$(ps -eo pid,pcpu,pmem,args --sort=-pmem|head -n 10)
    echo "***************************"
    echo "******    MEMTOP5   *******"
    echo "***************************"
    $mem
}
cpuUse
memory
disk
tcp_stat
topcpu
topmem
