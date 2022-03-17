from FA import *
from Lexicon import *

# 读取词法规则文件
production_formulae = []
file = open("Lexical Syntax.txt", encoding="UTF-8")
line = file.readline()
while line:
    line = line.replace(' ', '')
    line = line.rstrip('\n')
    if line and line[0] != '#':
        production_formulae.append([line.split("==>")[0], line.split("==>")[1]])
    line = file.readline()
file.close()

# NFA的字母表、状态集
alphabet, NFA_statuses = set(), {FA_START_STATUS, FA_FINISH_STATUS}
# 转换函数表：f(A,t)=B——tuple(A,t,B)
transition_functions = []
# 分析所有产生式
for pf in production_formulae:
    one_terminals, one_non_terminals, one_transitions = ProducerToNFA(pf[0], pf[1])
    for ot in one_terminals:
        alphabet.add(ot)
    for ont in one_non_terminals:
        NFA_statuses.add(ont)
    transition_functions += one_transitions

# DFA
DFA_statuses, DFA_transitions = NFAToDFA(alphabet, transition_functions)

# 读取源代码
source_code = []
file = open("Source Code.txt", encoding="UTF-8")
line = file.readline()
while line:
    # 去除首尾空白字符
    line = line.strip()
    # 将连续空格统一为一个空格，增加分析器的鲁棒性
    lsp = line.split(" ")
    i = 0
    while i in range(len(lsp)):
        if lsp[i] == "":
            lsp.pop(i)
        else:
            i += 1
    line = " ".join(lsp)
    # 按行存储
    source_code.append(line)
    line = file.readline()
file.close()

# 分析源代码
# (行号, 单词, Token, 值)
token_tuples = []
# DFA初态
DFA_start_status = GetDFAStartSubset(DFA_statuses)
# 是否处于多行注释中
inCommentBlock = False
# 报错输出信息
# (行号, 整行, 错误所在下标, 错误类型)
errorInfo = []

# 取一行
for line_index in range(len(source_code)):
    line = source_code[line_index]

    # 去除多行注释
    # 若处于多行注释中，且本行没有结束符号，则跳过本行
    if inCommentBlock and COMMENT_BLOCK_END not in line:
        continue
    # 记录所有注释开始和结束的位置
    cmt_start, cmt_end = [], []
    for i in range(len(line) - len(COMMENT_BLOCK_START) + 1):
        if line[i:i + len(COMMENT_BLOCK_START)] == COMMENT_BLOCK_START:
            cmt_start.append(i)
    for i in range(len(line) - len(COMMENT_BLOCK_END) + 1):
        if line[i:i + len(COMMENT_BLOCK_END)] == COMMENT_BLOCK_END:
            cmt_end.append(i)
    # 上一个多行注释块结束
    if len(cmt_end) == len(cmt_start) + 1:
        inCommentBlock = False
        line = line[cmt_end[0] + len(COMMENT_BLOCK_END):]
        cmt_end.pop(0)
    # 队列操作，去除行内的注释块
    while cmt_start and cmt_end:
        line = line[:cmt_start[0]] + line[cmt_end[0] + len(COMMENT_BLOCK_END):]
        cmt_start.pop(0)
        cmt_end.pop(0)
    # 下一个多行注释块开始
    if len(cmt_start) == len(cmt_end) + 1:
        inCommentBlock = True
        line = line[:cmt_start[0]]
        cmt_start.pop(-1)

    # 去除单行注释
    cmt_line = line.find(COMMENT_LINE)
    if cmt_line != -1:
        line = line[:cmt_line]

    # 字符列表
    chars = list(line)
    # 字符列表下标
    i = 0
    # DFA当前状态
    atFA = DFA_start_status
    # DFA状态栈
    status_stack = [atFA]
    # 待输出单词
    word = ""

    # 若当前字符不可转换，则需要处理已读取的字符串；否则转换新状态
    # 转换新状态后，若当前字符为最后一个字符，则需要处理已读取的字符串
    # 处理已读取的字符串：若处于DFA终态，则输出单词；若非终态，则报错
    while i in range(len(chars)):
        # 当前字符
        ch = chars[i]
        # 是否需要处理
        needProcessing = False

        # 查询转换表
        new_node = DFATransit(atFA, ch, DFA_transitions)
        # 存在转换
        if new_node:
            # 到下一站
            atFA = new_node
            status_stack.append(atFA)
            # 当前字符加入输出区
            word += ch
            # 如果到达最后一个字符，需要处理
            if i == len(chars) - 1:
                needProcessing = True
        # 不存在转换
        else:
            # 判断是否错误
            isErr = IsSyntaxError(word, ch, alphabet)
            if isErr:
                # 报错
                token_tuples.append((line_index + 1, word + ch, TOK_ERROR, isErr))
                # 添加报错信息
                errorInfo.append((line_index + 1, line, i, isErr))
                # 取下一行
                break
            # 若不是空白字符，则回退至上一个已读取的字符，需要处理
            if ch not in BLANK_CHARACTER:
                i -= 1
            needProcessing = True

        # 需要处理
        if needProcessing:
            # DFA到达可接受状态
            if FA_FINISH_STATUS in atFA:
                # 获取Token
                tok, val = GetToken(status_stack, word)
                # 交付Tuple
                token_tuples.append((line_index + 1, word, tok, val))
            # DFA处于不可接受状态
            else:
                # 报错：未完成的单词
                token_tuples.append((line_index + 1, word, TOK_ERROR, ERR_UNFINISHED_WORD))
                # 添加报错信息
                errorInfo.append((line_index + 1, line, i, ERR_UNFINISHED_WORD))
                # 取下一行
                break
            # 初始化
            atFA = DFA_start_status
            status_stack.clear()
            word = ""

        # 读取下一个字符
        i += 1

# 写入输出文件
file = open("Token List.txt", "w", encoding="UTF-8")
file.write("Line".ljust(5, ' ') + "Word".ljust(20, ' ') + "Token".ljust(15, ' ') + "Value")
file.write("\n" + "=" * 50 + "\n")
for tt in token_tuples:
    file.write(str(tt[0]).ljust(5, ' ') + str(tt[1]).ljust(20, ' ')
               + str(tt[2]).ljust(15, ' ') + str(tt[3]) + "\n")
file.close()

# 控制台输出报错信息
if errorInfo:
    print("\033[1;35;40m", end="")
    print(str(len(errorInfo)) + " error(s)")
    print("\033[0m", end="")
    for ei in errorInfo:
        line_info = "In Line " + str(ei[0]) + ": "
        print(line_info + ei[1])
        print(" " * len(line_info) + " " * ei[2] + "^")
        if ei[3] == ERR_HEX:
            print(" " * len(line_info) + "Error: Illegal hexadecimal")
            print(" " * len(line_info) +
                  "Hint: Hex digits should be numbers or letters in A-F (case insensitive)")
        elif ei[3] == ERR_IDENTIFIER:
            print(" " * len(line_info) + "Error: Illegal identifier, or incorrect decimal number")
            print(" " * len(line_info) +
                  "Hint: Identifiers should begin with a letter or an underline, " +
                  "and should only consist of letters, digits and underline")
        elif ei[3] == ERR_ILLEGAL_CHAR:
            print(" " * len(line_info) + "Error: Unsupported character")
            print(" " * len(line_info) +
                  "Hint: Non-ascii characters are currently unacceptable")
        elif ei[3] == ERR_UNFINISHED_WORD:
            print(" " * len(line_info) + "Error: Unexpected ending")
            print(" " * len(line_info) +
                  "Hint: It looks like an unfinished word")
    print("Analysis terminated.")

# 词法分析过程展示
file = open("Process of Lexical Analysis.txt", "w", encoding="UTF-8")
file.write("Process of Lexical Analysis" + "\n" + "=" * 100 + "\n")
# 字母表
file.write("Alphabet:\n")
alphabetList = list(alphabet)
alphabetList.sort()
for k in range(len(alphabetList)):
    file.write(str(alphabetList[k]).center(5, ' '))
    if (k + 1) % 10 == 0:
        file.write("\n")
file.write("\n" + "=" * 100 + "\n")
# NFA状态集
file.write("NFA Statuses:\n")
NFAStatusList = list(NFA_statuses)
NFAStatusList.sort()
for k in range(len(NFAStatusList)):
    file.write(str(NFAStatusList[k]).center(15, ' '))
    if (k + 1) % 5 == 0:
        file.write("\n")
file.write("\n" + "=" * 100 + "\n")
# NFA转换函数
file.write("NFA Transition Functions:\n")
for k in range(len(transition_functions)):
    TFstr = str(transition_functions[k][0]) + " == " \
            + str(transition_functions[k][1]) + " => " + str(transition_functions[k][2])
    file.write(TFstr.center(40, ' '))
    if (k + 1) % 2 == 0:
        file.write("\n")
file.write("\n" + "=" * 100 + "\n")
# DFA状态集
file.write("DFA Statuses:\n")
DFAStatusList = list(DFA_statuses)
# 按名称排序
DFAStatusList.sort(key=lambda s: s.name)
for k in range(len(DFAStatusList)):
    file.write(str(DFAStatusList[k].name).rjust(5, ' '))
    # 标记可接受的状态集
    if DFAStatusList[k].isTerminalStatus:
        file.write(" (T) ")
    else:
        file.write(" " * 5)
    # 每个DFA状态包含的NFA状态集合
    kthSubset = list(DFAStatusList[k].NFA_subset)
    kthSubset.sort()
    for ks in range(len(kthSubset)):
        if (ks + 1) % 5 == 0:
            file.write("\n" + " " * 10)
        file.write(str(kthSubset[ks]).center(15, ' '))
    file.write("\n")
file.write("\n" + "=" * 100 + "\n")
# DFA转换函数
file.write("DFA Transition Functions:\n")
# 转换结果为空集说明不存在转换，需要排除，因此用count记录实际的转换数量
count = 0
k = 0
while k in range(len(DFA_transitions)):
    # 排除到空集的转换
    if not DFA_transitions[k][2]:
        k += 1
        continue
    # 记录有效的转换
    count += 1
    if (count + 1) % 2 == 0:
        file.write("\n")
    # 因为DFA转换函数表记录的是包含的NFA状态集合，因此需要获取DFA状态的名称
    TFstr = str(GetDFANameBySubset(DFA_transitions[k][0], DFA_statuses)) + " == " \
            + str(DFA_transitions[k][1]) + " => " \
            + str(GetDFANameBySubset(DFA_transitions[k][2], DFA_statuses))
    file.write(TFstr.center(30, ' '))
    k += 1
file.write("\n" + "=" * 100 + "\n")
file.close()
