# 内部常量
FA_START_STATUS, FA_FINISH_STATUS = "START", "FINISH"


# 产生式右部处理
def RightSideProcess(s: str):
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


# 产生式分析
def ProducerToNFA(l: str, r: str):
    # 拆分右部
    all_r = RightSideProcess(r)

    # 统计终结符和非终结符，建立转换函数
    ter, non, transit = [], [], []
    # 左部
    l_n = l[l.find("<") + 1:l.find(">")]
    non.append(l_n)
    # 右部
    for one_r in all_r:
        # # 不是A→ε
        # if one_r:
        #     # A→tB
        #     if one_r.find("<") != -1:
        #         n = one_r[one_r.find("<") + 1:one_r.find(">")]
        #         t = one_r[0:one_r.find("<")]
        #         non.append(n)
        #         ter.append(t)
        #         transit.append((l_n, t, n))
        #     # A→t
        #     else:
        #         t = one_r
        #         ter.append(t)
        #         transit.append((l_n, t, FA_FINISH_STATUS))

        # 考虑产生式含有终结符<或>的情况
        # 不是A→ε
        if one_r:
            # 转义空格
            one_r = one_r.replace("__space__", " ")
            # A→tB
            if one_r.count("<") == 1 and one_r.count(">") == 1:
                n = one_r[one_r.find("<") + 1:one_r.find(">")]
                t = one_r[0:one_r.find("<")]
                non.append(n)
                ter.append(t)
                transit.append((l_n, t, n))
            # A→<B或A→>B
            elif one_r.count("<") + one_r.count(">") == 3:
                n = one_r[2:len(one_r) - 1]
                t = one_r[0]
                non.append(n)
                ter.append(t)
                transit.append((l_n, t, n))
            # A→t
            elif one_r.count("<") == 0 or one_r.count(">") == 0:
                t = one_r
                ter.append(t)
                transit.append((l_n, t, FA_FINISH_STATUS))

        # 是A→ε
        else:
            t = ''
            ter.append(t)
            transit.append((l_n, t, FA_FINISH_STATUS))

    return ter, non, transit


def EpsilonClosure(status_set: set, trans_func_table: list):
    closure = set()
    # 对于集合中的每一个状态，对其ε通路进行深度优先搜索
    for s in status_set:
        stack, visited = [], []
        # 当前状态
        stack.append(s)
        visited.append(s)
        # 深度优先搜索
        while stack:
            arcTail = stack[-1]
            visited.append(stack[-1])
            closure.add(stack[-1])
            stack.pop()
            # 遍历转换函数表
            for trf in trans_func_table:
                if trf[0] == arcTail and trf[1] == '' and (trf[2] not in visited):
                    stack.append(trf[2])

    return closure


def Move(status_set: set, arc: str, trans_func_table: list):
    moveSet = set()
    for s in status_set:
        # 遍历转换函数表
        for trf in trans_func_table:
            if trf[0] == s and trf[1] == arc:
                moveSet.add(trf[2])

    return moveSet


# 一个DFA状态包含一个NFA状态集的子集
# 正规文法生成的NFA只有一个终态，但转换得到的DFA可能有多个终态，因此不能再使用内部常量FA_FINISH_STATUS作为终态
# 根据生成原理，NFA终态不可能有出弧，但DFA终态可能存在出弧
class DFA_node:
    def __init__(self, name, subset):
        self.name = name
        self.NFA_subset = subset
        self.isTerminalStatus = False

    def setAsFINISH(self):
        self.isTerminalStatus = True


def NFAToDFA(alphabet: set, trans_func_table: list):
    initStatus = EpsilonClosure({FA_START_STATUS}, trans_func_table)
    subsets = [initStatus]
    stack = [initStatus]
    # 转换函数表、状态集
    DFA_transition, DFA_statuses = [], set()

    while stack:
        T = stack[-1]
        stack.pop()
        for a in alphabet:
            # 排除ε输入符
            if a == '':
                continue
            U = EpsilonClosure(Move(T, a, trans_func_table), trans_func_table)
            DFA_transition.append((T, a, U))
            # 排除空集
            if U and (U not in subsets):
                subsets.append(U)
                stack.append(U)

    for i in range(len(subsets)):
        # 创建DFA节点对象
        dn = DFA_node("DS" + str(i).zfill(2), subsets[i])
        # 正规文法生成的DFA开始状态只有一个
        if subsets[i] == initStatus:
            dn.name = FA_START_STATUS
        # 正规文法生成的DFA终态可能有多个
        elif FA_FINISH_STATUS in subsets[i]:
            dn.setAsFINISH()
        DFA_statuses.add(dn)

    return DFA_statuses, DFA_transition


def GetDFAStartSubset(statuses: set):
    for sta in statuses:
        if sta.name == FA_START_STATUS:
            return sta.NFA_subset
    return set()


def DFATransit(node: set, ch: str, trans_func: list):
    for trs in trans_func:
        if trs[0] == node and trs[1] == ch:
            return trs[2]
    return set()


def GetDFANameBySubset(subset: set, DFA_statuses: set):
    for ds in DFA_statuses:
        if subset == ds.NFA_subset:
            return ds.name
    return None
