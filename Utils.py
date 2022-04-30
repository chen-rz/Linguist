import datetime


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

    # 日志记录
    e = list(e.strip("\n"))
    for i in range(len(e) - 1):
        if e[i] == "\n":
            e.insert(i + 1, " " * 30)
    if e and e[-1] != "\n":
        e.append("\n")
    e = "".join(e)
    return str(datetime.datetime.now()) + " " * 4 + e


# 进度条
def ProgressBar(p: float):
    p *= 100
    pi = int(p)
    pd = int((p - pi) * 10)
    print("\033[1;34m", end="")
    pgb = "\r[" + "#" * (pi - 1)
    if pd == 0:
        pgb += "#"
    else:
        pgb += str(pd)
    pgb += " " * (100 - pi) + "] "
    pgb += str(pi) + "." + str(pd) + "%"
    print(pgb, end="")
    print("\033[0m", end="")
