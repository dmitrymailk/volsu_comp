import ply.lex as lex

# Определение токенов
tokens = (
    "NUMBER",
    "PERCENT",
    "HASH",
)

# Определение регулярных выражений для токенов
t_PERCENT = r"\%"
t_HASH = r"\#"

# Игнорировать пробелы и табуляции
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

precedence = (
    ("left", "PERCENT"),
    ("left", "HASH"),
)


# Определение грамматики
def p_expression(p):
    """expression : expression HASH expression
    | expression PERCENT expression"""
    if p[2] == "#":
        p[0] = (p[1] / p[3]) * 100
    elif p[2] == "%":
        p[0] = (p[1] * p[3]) / 100


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_error(p):
    print("Синтаксическая ошибка")


# Создание синтаксического анализатора
parser = yacc.yacc()

while True:
    try:
        s = input("Введите выражение: ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s, lexer=lexer)
    print(f"Результат: {result}")
