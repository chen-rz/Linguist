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

terminal_set, non_term_set, l_to_r_list = set(), set(), []
for gf in grammar_formulae:
    t, n, l = LR1_FormulaeResolution(gf[0], gf[1])
    terminal_set = terminal_set.union(t)
    non_term_set = non_term_set.union(n)
    l_to_r_list += l

print(terminal_set)
print(non_term_set)
print(l_to_r_list)
