import Lexer
import Parser

# token_list = Lexer.lex_analyze()

# abab
token_list = [(1, "a", "a", "a"),
              (2, "b", "b", "b"),
              (3, "a", "a", "a"),
              (4, "b", "b", "b")]
Parser.parse(token_list)
