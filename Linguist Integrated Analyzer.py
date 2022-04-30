import os
from Lexer import *
import Parser
from Utils import *

# 日志文件
logFile = ""

# 欢迎
logFile += CONSOLE("Welcome to Linguist, the integrated lexer and parser!", "PLAIN")
logFile += CONSOLE("Copyright © 2022 Runze Chen\n", "PLAIN")

# 输入各文件名
sourceCode_file = input("Input path of source code " +
                        "(press Enter directly for default \"Source Code.txt\"):\n")
if not sourceCode_file:
    sourceCode_file = "Source Code.txt"

syntax_file = input("Input path of lexical syntax rules " +
                    "(press Enter directly for default \"Lexical Syntax.txt\"):\n")
if not syntax_file:
    syntax_file = "Lexical Syntax.txt"

grammar_file = input("Input path of grammar rules " +
                     "(press Enter directly for default \"Grammar.txt\"):\n")
if not grammar_file:
    grammar_file = "Grammar.txt"

# 词法分析
token_list, errorInfo, log_lex = lex_analyze(syntax_file, sourceCode_file)
logFile += log_lex
# 词法分析报错信息
if errorInfo:
    er = "\n" + str(len(errorInfo)) + " error(s) in lexical analysis:\n"
    logFile += CONSOLE(er, "ERROR")
    for ei in errorInfo:
        line_info = "In Line " + str(ei[0]) + ": "
        er = line_info + ei[1]
        logFile += CONSOLE(er, "ERROR")
        wn = " " * len(line_info) + " " * ei[2] + "^"
        logFile += CONSOLE(wn, "WARN")
        if ei[3] == ERR_HEX:
            er = " " * len(line_info) + "Error: Illegal hexadecimal"
            logFile += CONSOLE(er, "ERROR")
            hn = " " * len(line_info) + \
                 "Hint: Hex digits should be numbers or letters in A-F (case insensitive)"
            logFile += CONSOLE(hn, "INFO")
        elif ei[3] == ERR_IDENTIFIER:
            er = " " * len(line_info) + "Error: Illegal identifier, or incorrect decimal number"
            logFile += CONSOLE(er, "ERROR")
            hn = " " * len(line_info) + \
                 "Hint: Identifiers should begin with a letter or an underline, " + \
                 "and should only consist of letters, digits and underline"
            logFile += CONSOLE(hn, "INFO")
        elif ei[3] == ERR_ILLEGAL_CHAR:
            er = " " * len(line_info) + "Error: Unsupported character"
            logFile += CONSOLE(er, "ERROR")
            hn = " " * len(line_info) + \
                 "Hint: Non-ascii characters are currently unacceptable"
            logFile += CONSOLE(hn, "INFO")
        elif ei[3] == ERR_UNFINISHED_WORD:
            er = " " * len(line_info) + "Error: Unexpected ending"
            logFile += CONSOLE(er, "ERROR")
            hn = " " * len(line_info) + \
                 "Hint: It looks like an unfinished word"
            logFile += CONSOLE(hn, "INFO")
    logFile += CONSOLE("Analysis terminated.", "ERROR")

# 词法分析无错误才能继续
else:
    logFile += Parser.parse(token_list, grammar_file)

# 写入日志文件
file = open("Log.txt", "w", encoding="UTF-8")
file.write(logFile)
file.close()

os.system("pause")
