# 注释符
COMMENT_LINE = "#"
COMMENT_BLOCK_START = "<!--"
COMMENT_BLOCK_END = "-->"

# 空白字符
BLANK_CHARACTER = [' ', '\t', '\n', '\r', '\f', '\v']

# DFA终态，对应判断分支
# 1
FIN_KW_ID = "F_K_I"
# 2
FIN_DECIMAL = "F_DEC"
# 3
FIN_HEX = "F_HEX"
# 4
FIN_FLOAT = "F_FLO"
# 5
FIN_SCIENTIFIC = "F_SCI"
# 6
FIN_CP_EP = "F_C_E"
# 7
FIN_STRING = "F_STR"
# 8
FIN_DELIMITER = "F_DEL"
# 9
FIN_OPERATOR = "F_OPE"

# Token
TOK_KEYWORD = "KEYWORD"
TOK_IDENTIFIER = "IDENTIFIER"
TOK_CONSTANT = "CONSTANT"
TOK_DELIMITER = "DELIMITER"
TOK_OPERATOR = "OPERATOR"
TOK_ERROR = "ERROR"

# Constant
CON_DECIMAL = "DECIMAL"
CON_HEX = "HEXADECIMAL"
CON_FLOAT = "FLOAT"
CON_SCIENTIFIC = "SCIENTIFIC"
CON_EXPRESSION = "EXPRESSION"
CON_COMPLEX = "COMPLEX"
CON_STRING = "STRING"

# Error
# 1 标识符错误（数字后面跟字母）
ERR_IDENTIFIER = "ILLEGAL_IDENTIFIER"
# 2 十六进制错误
ERR_HEX = "ILLEGAL_HEXADECIMAL"
# 3 不支持的字符
ERR_ILLEGAL_CHAR = "UNSUPPORTED_CHARACTER"
# 4 未完成的单词
ERR_UNFINISHED_WORD = "UNFINISHED_WORD"

# 关键字
KEYWORD = {}
# Common (11)
KWD_IF, KWD_ELSE, KWD_FOR, KWD_WHILE, KWD_BREAK, \
KWD_CONTINUE, KWD_CLASS, KWD_RETURN, KWD_IMPORT, KWD_TRY, \
KWD_FINALLY \
    = range(101, 112)
KEYWORD["if"] = KWD_IF
KEYWORD["else"] = KWD_ELSE
KEYWORD["for"] = KWD_FOR
KEYWORD["while"] = KWD_WHILE
KEYWORD["break"] = KWD_BREAK
KEYWORD["continue"] = KWD_CONTINUE
KEYWORD["class"] = KWD_CLASS
KEYWORD["return"] = KWD_RETURN
KEYWORD["import"] = KWD_IMPORT
KEYWORD["try"] = KWD_TRY
KEYWORD["finally"] = KWD_FINALLY

# Python (22)
KWD_AND, KWD_AS, KWD_ASSERT, KWD_DEL, KWD_IN, \
KWD_IS, KWD_NOT, KWD_OR, KWD_NONE, KWD_FALSE, \
KWD_TRUE, KWD_ELIF, KWD_DEF, KWD_YIELD, KWD_GLOBAL, \
KWD_LAMBDA, KWD_NONLOCAL, KWD_FROM, KWD_PASS, KWD_WITH, \
KWD_EXCEPT, KWD_RAISE \
    = range(112, 134)
KEYWORD["and"] = KWD_AND
KEYWORD["as"] = KWD_AS
KEYWORD["assert"] = KWD_ASSERT
KEYWORD["del"] = KWD_DEL
KEYWORD["in"] = KWD_IN
KEYWORD["is"] = KWD_IS
KEYWORD["not"] = KWD_NOT
KEYWORD["or"] = KWD_OR
KEYWORD["None"] = KWD_NONE
KEYWORD["False"] = KWD_FALSE
KEYWORD["True"] = KWD_TRUE
KEYWORD["elif"] = KWD_ELIF
KEYWORD["def"] = KWD_DEF
KEYWORD["yield"] = KWD_YIELD
KEYWORD["global"] = KWD_GLOBAL
KEYWORD["lambda"] = KWD_LAMBDA
KEYWORD["nonlocal"] = KWD_NONLOCAL
KEYWORD["from"] = KWD_FROM
KEYWORD["pass"] = KWD_PASS
KEYWORD["with"] = KWD_WITH
KEYWORD["except"] = KWD_EXCEPT
KEYWORD["raise"] = KWD_RAISE

# 限定符
DELIMITER = {}
DEL_L_PARENTHESIS, DEL_R_PARENTHESIS, DEL_L_BRACKET, DEL_R_BRACKET, DEL_L_BRACE, \
DEL_R_BRACE, DEL_SEMICOLON, DEL_COLON, DEL_COMMA, DEL_PERIOD, \
DEL_OCTOTHORPE, DEL_QUESTION \
    = range(201, 213)

DELIMITER["("] = DEL_L_PARENTHESIS
DELIMITER[")"] = DEL_R_PARENTHESIS
DELIMITER["["] = DEL_L_BRACKET
DELIMITER["]"] = DEL_R_BRACKET
DELIMITER["{"] = DEL_L_BRACE
DELIMITER["}"] = DEL_R_BRACE
DELIMITER[";"] = DEL_SEMICOLON
DELIMITER[":"] = DEL_COLON
DELIMITER[","] = DEL_COMMA
DELIMITER["."] = DEL_PERIOD
DELIMITER["#"] = DEL_OCTOTHORPE
DELIMITER["?"] = DEL_QUESTION

# 运算符
OPERATOR = {}
OPR_PLUS, OPR_MINUS, OPR_MUL, OPR_DIV, OPR_ASSIGN, \
OPR_EQUAL, OPR_GT, OPR_LT, OPR_GET, OPR_LET, \
OPR_SELF_PLUS, OPR_SELF_MINUS, OPR_SELF_MUL, OPR_SELF_DIV, OPR_MOD, \
OPR_DBL_GT, OPR_DBL_LT, OPR_ARITH_AND, OPR_ARITH_OR, OPR_NOT, \
OPR_INVERSE, OPR_XOR, OPR_LOGI_AND, OPR_LOGI_OR \
    = range(301, 325)
OPERATOR["+"] = OPR_PLUS
OPERATOR["-"] = OPR_MINUS
OPERATOR["*"] = OPR_MUL
OPERATOR["/"] = OPR_DIV
OPERATOR["="] = OPR_ASSIGN
OPERATOR["+="] = OPR_SELF_PLUS
OPERATOR["-="] = OPR_SELF_MINUS
OPERATOR["*="] = OPR_SELF_MUL
OPERATOR["/="] = OPR_SELF_DIV
OPERATOR["=="] = OPR_EQUAL
OPERATOR["~"] = OPR_INVERSE
OPERATOR["!"] = OPR_NOT
OPERATOR["%"] = OPR_MOD
OPERATOR["^"] = OPR_XOR
OPERATOR["&&"] = OPR_LOGI_AND
OPERATOR["||"] = OPR_LOGI_OR
OPERATOR["<<"] = OPR_DBL_LT
OPERATOR[">>"] = OPR_DBL_GT
OPERATOR[">"] = OPR_GT
OPERATOR["<"] = OPR_LT
OPERATOR[">="] = OPR_GET
OPERATOR["<="] = OPR_LET
OPERATOR["&"] = OPR_ARITH_AND
OPERATOR["|"] = OPR_ARITH_OR


def GetToken(status_stack: list, word: str):
    tok, val = None, None
    # 终态子集可能不含类型信息，故需要在状态栈中查找类型信息
    while status_stack:
        # 得到类型信息则退出
        if tok:
            break
        status = status_stack[-1]
        status_stack.pop()
        for elem in status:
            # 1 关键字或标识符
            if FIN_KW_ID in elem:
                # 查询关键字表
                if KEYWORD.get(word):
                    tok, val = TOK_KEYWORD, KEYWORD.get(word)
                # 标识符
                else:
                    tok, val = TOK_IDENTIFIER, ""
                break
            # 常量
            # 2 常量：十进制整数
            elif FIN_DECIMAL in elem:
                tok, val = TOK_CONSTANT, CON_DECIMAL
                break
            # 3 常量：十六进制整数
            elif FIN_HEX in elem:
                tok, val = TOK_CONSTANT, CON_HEX
                break
            # 4 常量：浮点数
            elif FIN_FLOAT in elem:
                tok, val = TOK_CONSTANT, CON_FLOAT
                break
            # 5 常量：科学记数法
            elif FIN_SCIENTIFIC in elem:
                tok, val = TOK_CONSTANT, CON_SCIENTIFIC
                break
            # 6 常量：复数或加减表达式
            elif FIN_CP_EP in elem:
                # 复数
                if word[-1] == "i":
                    tok, val = TOK_CONSTANT, CON_COMPLEX
                # 表达式
                else:
                    tok, val = TOK_CONSTANT, CON_EXPRESSION
                break
            # 7 常量：字符串
            elif FIN_STRING in elem:
                tok, val = TOK_CONSTANT, CON_STRING
                break
            # 8 界符
            elif FIN_DELIMITER in elem:
                tok, val = TOK_DELIMITER, DELIMITER.get(word)
                break
            # 9 运算符
            elif FIN_OPERATOR in elem:
                tok, val = TOK_OPERATOR, OPERATOR.get(word)
                break

    return tok, val


def IsSyntaxError(word: str, ch: str, alphabet: set):
    if word and ("0x" in word or "0X" in word) and ("G" <= ch <= "Z" or "g" <= ch <= "z") \
            and (word[-1].isdigit() or "A" <= word[-1] <= "F" or "a" <= word[-1] <= "f"):
        # 2 十六进制错误
        return ERR_HEX
    if word and word[-1].isdigit() and ch.isalpha():
        # 1 标识符错误
        return ERR_IDENTIFIER
    elif ch not in alphabet:
        # 3 不支持的字符
        return ERR_ILLEGAL_CHAR
    # 4 未完成的单词，由词法分析程序判断
    # 其他情况不是错误
    return None
