# 产生式右部拆分
def LR1_RightSideProcess(s: str):
    # 拆分一条产生式的多个右部选项
    splitPoints = [-1]
    for i in range(len(s)):
        if s[i] == '$':
            splitPoints.append(i)
    splitPoints.append(len(s))
    all_parts = []
    for i in range(len(splitPoints) - 1):
        all_parts.append(s[splitPoints[i] + 1:splitPoints[i + 1]])

    # 返回一条产生式的所有右部选项
    return all_parts


# 读取产生式
def LR1_FormulaeResolution(l: str, whole_r: str):
    # 拆分多个右部
    r = LR1_RightSideProcess(whole_r)
    # 终结符集、非终结符集、产生式列表
    terminal, non_term, l_and_r_list = set(), set(), []

    # 左边
    # 是否为非终结符符号
    ntFlag = False
    lBuff = ""
    # 遍历每一个字符
    for ls in l:
        # 搜索非终结符开始符号
        if not ntFlag and ls == "<":
            ntFlag = True
        # 搜索非终结符结束符号
        elif ntFlag:
            # 结束
            if ls == ">":
                break
            # 在非终结符符号内的字符，即为非终结符名称
            else:
                lBuff += ls
    # 虽然2型文法规定产生式左部只能是一个非终结符，但上述算法可以增加程序鲁棒性，且可以泛化、为产生式有部分析提供启发
    non_term.add(lBuff)

    # 右边
    # 对于每一个右部
    for ir in r:
        # 每个右部有多个语法符号，如 S ==> aAbBcc
        rBfs = []
        # -1表示终结符，1表示非终结符，0表示不属于语法符号名称
        nt_or_t = 0
        # 单个语法符号名称
        rBuff = ""
        # 遍历一个右部的所有字符
        for rs in ir:
            # 搜索语法符号开始
            if not nt_or_t:
                if rs == "<":
                    nt_or_t = 1
                elif rs == "(":
                    nt_or_t = -1
            # 搜索语法符号结束
            else:
                if nt_or_t == 1:
                    if rs == ">":
                        # 初始化，存储当前符号名称，并更新相应集合
                        nt_or_t = 0
                        rBfs.append(rBuff)
                        non_term.add(rBuff)
                        rBuff = ""
                    else:
                        rBuff += rs
                elif nt_or_t == -1:
                    if rs == ")":
                        nt_or_t = 0
                        rBfs.append(rBuff)
                        terminal.add(rBuff)
                        rBuff = ""
                    else:
                        rBuff += rs
        # 每一个右部和其对应的左部形成一条产生式列表信息
        l_and_r_list.append((lBuff, rBfs))

    return terminal, non_term, l_and_r_list
