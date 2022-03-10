# 注释符
COMMENT_LINE = "//"
COMMENT_BLOCK_START = "/*"
COMMENT_BLOCK_END = "*/"

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

# 关键字
KEYWORD = {}
KWD_INT, KWD_FLOAT, KWD_STRING, KWD_IF, KWD_ELSE, \
KWD_CONTINUE, KWD_BREAK, KWD_FOR, KWD_TRUE, KWD_FALSE \
    = range(101, 111)

KEYWORD["int"] = KWD_INT
KEYWORD["float"] = KWD_FLOAT
KEYWORD["string"] = KWD_STRING
KEYWORD["if"] = KWD_IF
KEYWORD["else"] = KWD_ELSE
KEYWORD["continue"] = KWD_CONTINUE
KEYWORD["break"] = KWD_BREAK
KEYWORD["for"] = KWD_FOR
KEYWORD["true"] = KWD_TRUE
KEYWORD["false"] = KWD_FALSE

# 界符
DELIMITER = {}
DEL_L_PARENTHESIS, DEL_R_PARENTHESIS, DEL_L_BRACKET, DEL_R_BRACKET, DEL_L_BRACE, \
DEL_R_BRACE, DEL_SEMICOLON, DEL_COLON, DEL_COMMA, DEL_PERIOD, \
DEL_OCTOTHORPE \
    = range(201, 212)

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

# 运算符
OPERATOR = {}
OPR_PLUS, OPR_MINUS, OPR_MUL, OPR_DIV, OPR_ASSIGN, \
OPR_EQUAL, OPR_GT, OPR_LT, OPR_GET, OPR_LET, \
OPR_SELF_PLUS, OPR_SELF_MINUS, OPR_SELF_MUL, OPR_SELF_DIV, OPR_MOD, \
OPR_DBL_GT, OPR_DBL_LT, OPR_ARITH_AND, OPR_ARITH_OR, OPR_NOT \
    = range(301, 321)
OPERATOR["+"] = OPR_PLUS
OPERATOR["-"] = OPR_MINUS
OPERATOR["*"] = OPR_MUL
OPERATOR["/"] = OPR_DIV
OPERATOR["="] = OPR_ASSIGN
OPERATOR["=="] = OPR_EQUAL
OPERATOR[">"] = OPR_GT
OPERATOR["<"] = OPR_LT
OPERATOR[">="] = OPR_GET
OPERATOR["<="] = OPR_LET
OPERATOR["+="] = OPR_SELF_PLUS
OPERATOR["-="] = OPR_SELF_MINUS
OPERATOR["*="] = OPR_SELF_MUL
OPERATOR["/="] = OPR_SELF_DIV
OPERATOR["%"] = OPR_MOD
OPERATOR[">>"] = OPR_DBL_GT
OPERATOR["<<"] = OPR_DBL_LT
OPERATOR["&"] = OPR_ARITH_AND
OPERATOR["|"] = OPR_ARITH_OR
OPERATOR["!"] = OPR_NOT


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


# 判断词法是否错误
def IsSyntaxError(word: str, ch: str):
    # 空白字符、界符或运算符结束，不是错误
    if word[-1] in BLANK_CHARACTER or OPERATOR.get(word[-1]) or DELIMITER.get(word[-1]):
        return False
    # 遇到空白字符、界符或运算符，不是错误
    if ch in BLANK_CHARACTER or OPERATOR.get(ch) or DELIMITER.get(ch):
        return False
    return True
