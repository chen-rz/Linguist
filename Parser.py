from LR1 import *

# 读取语法规则
grammar_formulae = []
file = open("Grammar.txt", encoding="UTF-8")
line = file.readline()
while line:
    line = line.replace(' ', '')
    line = line.rstrip('\n')
    if line and line[0] != '#':
        grammar_formulae.append([line.split("==>")[0], line.split("==>")[1]])
    line = file.readline()
file.close()

# 获取所有非终结符、终结符、产生式
terminal_set, non_term_set, producer_list = set(), set(), []
for gf in grammar_formulae:
    tms, nts, ltr = LR1_FormulaeResolution(gf[0], gf[1])
    terminal_set = terminal_set.union(tms)
    non_term_set = non_term_set.union(nts)
    producer_list += ltr

# 项目集族、GO表
allItemSets = []
GOTable = {}

# 初始项目
IS = [["START'", [], ["START"], ""]]
clo = ItemSetClosure(IS, terminal_set, non_term_set, producer_list)
allItemSets.append(clo)

# 所有的文法符号
allSymbols = set().union(terminal_set).union(non_term_set)
allSymbols.discard("")

terminated = False
while not terminated:
    terminated = True
    # 每个文法符号
    for X in allSymbols:
        # 每个项目集
        for s in range(len(allItemSets)):
            # 新的项目集
            IS = []
            # 一个项目集的每个项目
            for i in allItemSets[s]:
                # [A→α·Xβ,a]∈I
                if i[IT_AFTER_DOT] and i[IT_AFTER_DOT][0] == X:
                    # 任何形如[A→αX·β,a]的项目
                    newBefore = i[IT_BEFORE_DOT].copy()
                    newBefore.append(i[IT_AFTER_DOT][0])
                    newAfter = i[IT_AFTER_DOT].copy()
                    newAfter.pop(0)
                    IS.append([i[IT_LEFT], newBefore, newAfter, i[IT_SEARCH]])
            # 有新项目产生
            if IS:
                clo = ItemSetClosure(IS, terminal_set, non_term_set, producer_list)
                if clo not in allItemSets:
                    allItemSets.append(clo)
                    # 使用下标作为编号，刚刚加入的应为最后一项
                    GOTable[(s, X)] = len(allItemSets) - 1
                    terminated = False
                    # 重新开始循环
                    break
                # 已有的项目集也需要加入GO表
                else:
                    # 查找已有项目集下标
                    for cx in range(len(allItemSets)):
                        if allItemSets[cx] == clo:
                            GOTable[(s, X)] = cx
                            break
        if not terminated:
            break

# 语法分析过程展示
file = open("Process of LR(1) Parsing.txt", "w", encoding="UTF-8")
file.write("Process of LR(1) Parsing" + "\n" + "=" * 100 + "\n")
# 终结符
file.write("Terminals:\n")
terminalList = list(terminal_set)
terminalList.sort()
for k in range(len(terminalList)):
    file.write(str(terminalList[k]).center(20, ' '))
    if (k + 1) % 5 == 0:
        file.write("\n")
file.write("\n" + "=" * 100 + "\n")
# 非终结符
file.write("Non-terminals:\n")
nonTerminalList = list(non_term_set)
nonTerminalList.sort()
for k in range(len(nonTerminalList)):
    file.write(str(nonTerminalList[k]).center(20, ' '))
    if (k + 1) % 5 == 0:
        file.write("\n")
file.write("\n" + "=" * 100 + "\n")
# 项目集
file.write("Closures of Item Sets:\n")
for ax in range(len(allItemSets)):
    file.write(str(ax).rjust(3, ' '))
    for k in range(len(allItemSets[ax])):
        s1, s2, s3, s4 = allItemSets[ax][k][IT_LEFT], \
                         " ".join(allItemSets[ax][k][IT_BEFORE_DOT]), \
                         " ".join(allItemSets[ax][k][IT_AFTER_DOT]), \
                         allItemSets[ax][k][IT_SEARCH]
        if not s4:
            s4 = "#"
        file.write((s1 + " => " + s2 + " · " + s3 + ", " + s4).center(50, ' '))
        if (k + 1) % 2 == 0:
            file.write("\n" + ' ' * 3)
    file.write("\n")
file.write("\n" + "=" * 100 + "\n")
# 转换函数（GO）
file.write("GO Functions:\n")
GOList = list(zip(list(GOTable.keys()), list(GOTable.values())))
GOList.sort(key=lambda ki: ki[0])
for k in range(len(GOList)):
    file.write((str(GOList[k][0]) + " => " + str(GOList[k][1])).center(25, ' '))
    if (k + 1) % 4 == 0:
        file.write("\n")
file.write("\n" + "=" * 100 + "\n")
