# 封装控制台信息输出格式
def CONSOLE(e: str, infoType: str):
    if infoType == "ERROR":
        # 紫红色
        print("\033[1;35m", end="")
    elif infoType == "WARN":
        # 黄色
        print("\033[1;33m", end="")
    elif infoType == "INFO":
        # 蓝色
        print("\033[1;34m", end="")
    elif infoType == "NORMAL":
        # 绿色
        print("\033[1;32m", end="")

    print(e)
    print("\033[0m", end="")
