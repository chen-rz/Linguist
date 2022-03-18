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
terminal_set, non_term_set, production_list = set(), set(), []
for gf in grammar_formulae:
    tms, nts, ltr = LR1_FormulaeResolution(gf[0], gf[1])
    terminal_set = terminal_set.union(tms)
    non_term_set = non_term_set.union(nts)
    production_list += ltr

print(terminal_set)
print(non_term_set)
print(production_list)

print(FIRST(['S', 'c', 'd'], terminal_set, non_term_set, production_list))
