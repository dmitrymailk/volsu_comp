import ply.lex as lex

# Определение токенов
tokens = (
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "POWER",
    "LPAREN",
    "RPAREN",
)

# Определение регулярных выражений для токенов
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_POWER = r"\*\*|\^"
t_LPAREN = r"\("
t_RPAREN = r"\)"

# Игнорируем пробелы и табуляции
t_ignore = " \t"


# Обработка чисел
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Обработка ошибок
def t_error(t):
    print(f"Нераспознанный символ '{t.value[0]}'")
    t.lexer.skip(1)


# Создание лексического анализатора
lexer = lex.lex()

import ply.yacc as yacc

# Определение грамматики
precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "UMINUS"),
)


# Определение структуры выражений
def p_expression_binop(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression POWER expression"""
    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]
    elif p[2] == "**" or p[2] == "^":
        p[0] = p[1] ** p[3]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]


def p_error(p):
    print("Синтаксическая ошибка")


# Создание синтаксического анализатора
parser = yacc.yacc()

precedence = (
    ("right", "UMINUS"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "POWER"),
)

while True:
    try:
        s = input("Введите выражение: ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s, lexer=lexer)
    print(f"Результат: {result}")
