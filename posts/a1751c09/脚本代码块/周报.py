import os
import sys
import subprocess
from datetime import datetime, timedelta
# import pandas as pd //check_libraries方法判断后导入。

# pip检查
pipUrl = "https://mirrors.aliyun.com/pypi/simple/"

def check_pip_version():
    try:
        output = subprocess.check_output(["pip", "--version"])
        version = output.decode("utf-8").split()[1]
        # pip install pip --index-url https://pypi.mirrors.ustc.edu.cn/simple
        if not version.startswith("23"):
            print("当前pip版本不是最新版，正在更新...")
            os.system(
                "pip install -i " + pipUrl + " --upgrade pip")
            print("pip已更新到最新版本。")
    except FileNotFoundError:
        print("pip未安装，正在安装...")
        os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        os.system("python get-pip.py --user")
        os.system(
            "pip install -i " + pipUrl + " pandas openpyxl")
        print("pip和相关库已安装。")
        sys.exit()

# 库检查
def check_libraries():
    try:
        import pandas as pd
        import openpyxl as opx
        print("pandas和openpyxl已安装。")
    except ImportError:
        print("pandas或openpyxl未安装，正在安装...")
        os.system(
            "pip install -i " + pipUrl + " pandas openpyxl")
        print("pandas和openpyxl已安装。")


check_pip_version()
check_libraries()

import pandas as pd
print("pandas和openpyxl库已导入。")

# 获取当前文件所在目录，生成的文件都会存在同级目录。
dir_path = os.path.dirname(os.path.abspath(__file__))

# Excel文件路径
# 需自行替换文件名称
# excel_file = os.path.join(dir_path, "问题列表（丁宣文）.xlsx")  //当前处理文件同目录下
excel_file = os.path.realpath(
    r'C:\Users\Administrator\Desktop\问题列表（丁宣文）.xlsx')  # 绝对路径请自行替换文件名
# 添加 r 标示原生字符，防止直接复制路径报错

# 检查文件路径是否有效
if not os.path.exists(excel_file):
    print("文件路径无效！")
    exit()

# 获取当前日期
current_date = datetime.now()

# 计算本周的周一和周五的日期
start_time = current_date - timedelta(days=current_date.weekday())
end_time = start_time + timedelta(days=4)

# 设置时间起止范围
start_time = pd.Timestamp(start_time).strftime('%Y-%m-%d')
end_time = pd.Timestamp(end_time).strftime('%Y-%m-%d')

# 设置时间范围（手动筛选，统计周期非周一至周五才启用）
# start_time = pd.Timestamp('2023-10-07')
# end_time = pd.Timestamp('2023-10-13')

# 读取Excel表格数据
dtypes = {"编号": str, "严重程度评估": str}  # 将数字列设置为字符串类型

try:
    excel_data = pd.read_excel(excel_file, dtype=dtypes)
except Exception as e:
    print("读取Excel文件时出错:", str(e))
    exit()

# 筛选符合时间范围的数据
excel_data_range = excel_data[(excel_data['提出日期'] >= start_time) & (excel_data['提出日期'] <= end_time)]

# 新建一个空的DataFrame用于存放处理后的数据
data_result = pd.DataFrame()

# 表格内容过滤生成
# data_result['本周主要工作'] = excel_data_range.apply(lambda row: str(excel_data_range.index.get_loc(row.name)+1) + '、' + (row['提出企业']) + "\n" + str(row['问题描述']).replace('\n', '') + str(row['处理措施']).replace('\n', ''), axis=1)
#print (excel_data_range)

data_result['本周主要工作'] = excel_data_range.apply(lambda row: 
                                     str( (row['提出企业']) )
                                     + "\n" + str(row['问题描述']).replace('\n', '') 
                                     + "：" + str(row['原因分析']).replace('无', '') 
                                     + "。" + str(row['处理措施']).replace('\n', ''),
                                     axis=1
                                     )

# 生成表格数据
output_file = os.path.join(dir_path, "周报.xlsx")
try:
    with pd.ExcelWriter(output_file) as writer:
        data_result.to_excel(writer, index=False)
except Exception as e:
    print("保存Excel文件时出错:", str(e))
    exit()

print("结果已保存为周报.xlsx")


# 生成邮件内容
output_file = os.path.join(dir_path, "周报.txt")
try:
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("本周主要工作\n")  # 写入第一行数据
        count = 1  # 计数变量
        for _, row in excel_data_range.iterrows():
            # line = f"{count}、{row['提出企业']}{row['问题描述']}{row['处理措施']}\n"
            line = f"{count}、{row['提出企业']}：{row['问题描述']}。\n"
            file.write(line)
            count += 1  # 计数递增
        
        # 开始写入第一行核对用数据
        file.write("\n\n本周表格数据（核对用）\n")  
        for _, row in excel_data_range.iterrows():
            line = f"{row['提出企业']}\n{row['问题描述']}:{str(row['原因分析']).replace('无','')},{row['处理措施']}。\n\n"
            file.write(line)
    file.close()
except Exception as e:
    print("保存txt文件时出错:", str(e))
    exit()

print("结果已保存为周报.txt")