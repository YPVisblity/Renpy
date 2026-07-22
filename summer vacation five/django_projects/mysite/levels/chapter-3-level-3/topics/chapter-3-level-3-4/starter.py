def infix_to_postfix(expression):
    """將中序表達式轉換為後序表達式，只需處理 + - * / 與括號"""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = Stack()
    output = []
    # TODO: 請完成這個函式
    return "".join(output)