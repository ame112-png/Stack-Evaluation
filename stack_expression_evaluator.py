

import os


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b


def infix_to_postfix(expression):
    stack = Stack()
    output = []
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()

    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            output.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while (not stack.is_empty() and precedence(stack.peek()) >= precedence(token)):
                output.append(stack.pop())
            stack.push(token)

    while not stack.is_empty():
        output.append(stack.pop())

    return output


def evaluate_postfix(postfix):
    stack = Stack()
    for token in postfix:
        if token.replace('.', '', 1).isdigit():
            stack.push(float(token))
        else:
            b = stack.pop()
            a = stack.pop()
            result = apply_op(a, b, token)
            stack.push(result)
    return stack.pop()



def process_expressions(input_file='input.txt', output_file='output.txt'):
    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' not found in current directory.")
        return

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            expr = line.strip()
            # Keep the same separator lines in output
            if expr == '' or all(c == '-' for c in expr):
                outfile.write(expr + '\n')
                continue

            try:
                postfix = infix_to_postfix(expr)
                result = evaluate_postfix(postfix)
                # If result is an integer, show it as int (no .0)
                if result.is_integer():
                    result = int(result)
                outfile.write(str(result) + '\n')
            except Exception as e:
                outfile.write(f"Error: {e}\n")

    print(f"Results written successfully to '{output_file}'.")


if __name__ == "__main__":
    process_expressions('input.txt', 'output.txt')
