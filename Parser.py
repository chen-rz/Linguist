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

print(terminal_set)
print(non_term_set)
print(producer_list)
# print(FIRST(['START', 'c', 'd'], terminal_set, non_term_set, producer_list))

# 项目集族、GO表
allItemSets = []
GOTable = {}
itemSetID = 0

# 初始项目
IS = ItemSet()
IS.setIdNo(itemSetID)
itemSetID += 1
IS.addItem(["START'", [], ["START"], ""])
clo = ItemSetClosure(itemSetID, IS, terminal_set, non_term_set, producer_list)
allItemSets.append(clo)

allSymbols = set().union(terminal_set).union(non_term_set)
allSymbols.discard("")
# 每个文法符号
for X in allSymbols:

    # TODO There is an unknown error that leads to a dead loop!
    terminated = False
    while not terminated:
        # 假设没有新项目产生
        terminated = True
        # 每个项目集
        for s in allItemSets:
            # 新的项目集
            IS = ItemSet()
            IS.setIdNo(itemSetID)
            itemSetID += 1
            # 一个项目集的每个项目
            for i in s.items:
                # [A→α·Xβ,a]∈I
                if i[IT_AFTER_DOT] and i[IT_AFTER_DOT][0] == X:
                    # 任何形如[A→αX·β,a]的项目
                    newBefore = i[IT_BEFORE_DOT].copy()
                    newBefore.append(i[IT_AFTER_DOT][0])
                    newAfter = i[IT_AFTER_DOT].copy()
                    newAfter.pop(0)
                    IS.addItem([i[IT_LEFT], newBefore, newAfter, i[IT_SEARCH]])
            # 有新项目产生
            if IS.items:
                clo = ItemSetClosure(itemSetID, IS, terminal_set, non_term_set, producer_list)
                if clo not in allItemSets:
                    allItemSets.append(clo)
                    GOTable[(s.idNo, X)] = clo
                    terminated = False
                    # 重新开始循环
                    break
            # 没有新项目产生
            else:
                itemSetID -= 1

for al in allItemSets:
    print(al.items)
