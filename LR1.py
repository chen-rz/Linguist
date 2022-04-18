import Lexicon


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
# 返回的产生式的数据结构：tuple(0 - 左边, 1 - list[右边按顺序排列])
def LR1_FormulaeResolution(l: str, whole_r: str):
    # 拆分多个右部
    r = LR1_RightSideProcess(whole_r)
    # 终结符集、非终结符集、产生式列表
    terminal, non_term, producer_list = set(), set(), []

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

                        # 存储终结符代号
                        if rBuff:
                            rBuff = Lexicon.getTerminalCode(rBuff)

                        rBfs.append(rBuff)
                        terminal.add(rBuff)
                        rBuff = ""
                    else:
                        rBuff += rs
        # 每一个右部和其对应的左部形成一条产生式列表信息
        producer_list.append((lBuff, rBfs))

    return terminal, non_term, producer_list


# 查询产生式的编号
def ProducerIdNo(p: tuple, producer_list: list):
    for i in range(len(producer_list)):
        if producer_list[i] == p:
            return i
    return -1


# FIRST集
def FIRST(symbol_list: list, terminal: set, non_term: set, producers: list):
    FIRST_set = set()

    # for s in symbol_list:
    #     # 找到第一个终结符
    #     if s in terminal:
    #         FIRST_set.add(s)
    #     # 非终结符
    #     elif s in non_term:
    #         # 查找以其为左部的产生式
    #         for prd in producers:
    #             if prd[0] == s:
    #                 # 递归调用
    #                 FIRST_set = FIRST_set.union(
    #                     FIRST(prd[1], terminal, non_term, producers))
    #     # 若找到终结符，则结束
    #     if FIRST_set:
    #         return FIRST_set

    # 采用迭代算法
    pstack = [symbol_list]
    while pstack:
        # 首符号
        s = pstack[-1][0]
        pstack.pop(-1)
        # 找到第一个终结符
        if s in terminal:
            FIRST_set.add(s)
        # 非终结符
        elif s in non_term:
            # 查找以其为左部的产生式
            for prd in producers:
                if prd[0] == s:
                    pstack.append(prd[1])

    return FIRST_set


# 构造LR(1)项目集族
# 项目的数据结构：list[0 - left: str, 1 - beforeDot: list, 2 - afterDot: list, 3 - searchSymbol: str]
IT_LEFT, IT_BEFORE_DOT, IT_AFTER_DOT, IT_SEARCH = range(4)


# 项目集是一个存储项目的list
def ItemSetClosure(I: list, terminals: set, non_terminals: set, producers: list):
    clo = I.copy()

    converged = False
    i = 0
    while not converged:
        converged = True
        # for i in clo:
        #     # 处理空产生式的情况
        #     while "" in i[IT_BEFORE_DOT]:
        #         i[IT_BEFORE_DOT].remove("")
        #     while "" in i[IT_AFTER_DOT]:
        #         i[IT_AFTER_DOT].remove("")
        #     # 若有项目A→α·Bβ,a属于CLOSURE(I)，
        #     if i[IT_AFTER_DOT] and i[IT_AFTER_DOT][0] in non_terminals:
        #         # B→γ是文法中的产生式，
        #         nextAfterDot = i[IT_AFTER_DOT][0]
        #         for p in producers:
        #             if p[0] == nextAfterDot:
        #                 # βa
        #                 bAfterDot = i[IT_AFTER_DOT].copy()  # 一定要以拷贝的形式！
        #                 bAfterDot.pop(0)
        #                 bAfterDot.append(i[IT_SEARCH])
        #                 # FIRST集
        #                 firstBetas = FIRST(bAfterDot, terminals, non_terminals, producers)
        #                 # b∈FIRST(βa)，
        #                 for sfs in firstBetas:
        #                     # 则B→·γ,b也属于CLOSURE(I)
        #                     it = [nextAfterDot, [], p[1], sfs]
        #                     # 直到CLOSURE(I)不再增大为止
        #                     if it not in clo:
        #                         clo.append(it)
        #                         converged = False
        #     # CLOSURE(I)改变，重新开始循环
        #     if not converged:
        #         break

        while i in range(len(clo)):
            # 处理空产生式的情况
            while "" in clo[i][IT_BEFORE_DOT]:
                clo[i][IT_BEFORE_DOT].remove("")
            while "" in clo[i][IT_AFTER_DOT]:
                clo[i][IT_AFTER_DOT].remove("")
            # 若有项目A→α·Bβ,a属于CLOSURE(I)，
            if clo[i][IT_AFTER_DOT] and clo[i][IT_AFTER_DOT][0] in non_terminals:
                # B→γ是文法中的产生式，
                nextAfterDot = clo[i][IT_AFTER_DOT][0]
                for p in producers:
                    if p[0] == nextAfterDot:
                        # βa
                        bAfterDot = clo[i][IT_AFTER_DOT].copy()  # 一定要以拷贝的形式！
                        bAfterDot.pop(0)
                        bAfterDot.append(clo[i][IT_SEARCH])
                        # FIRST集
                        firstBetas = FIRST(bAfterDot, terminals, non_terminals, producers)
                        # b∈FIRST(βa)，
                        for sfs in firstBetas:
                            # 则B→·γ,b也属于CLOSURE(I)
                            it = [nextAfterDot, [], p[1], sfs]
                            # 直到CLOSURE(I)不再增大为止
                            if it not in clo:
                                clo.append(it)
                                converged = False
            i += 1
            # CLOSURE(I)改变，重新开始循环
            if not converged:
                break

    return clo
