"""
Sophie Wang

Symbolic Algebra
"""

# import doctest
# import typing
# import pprint
# import string
# import abc


class Expr:
    """Expression Class"""
    @staticmethod
    def ensure(val):
        """Ensures val is a str, int, or float. If not, raise TypeError"""
        if isinstance(val, Expr):
            return val
        if isinstance(val, str):
            return Var(val)
        if isinstance(val, (int, float)):
            return Num(val)
        else:
            raise TypeError
            
    def __add__(self, others):
        return Add(self, others)
        
    def __radd__(self, others):
        return Add(others, self)
        
    def __sub__(self, others):
        return Sub(self, others)
        
    def __rsub__(self, others):
        return Sub(others, self)
        
    def __mul__(self, others):
        return Mul(self, others)
        
    def __rmul__(self, others):
        return Mul(others, self)
        
    def __truediv__(self, others):
        return Div(self, others)
        
    def __rtruediv__(self, others):
        return Div(others, self)

class SymbolicEvaluationError(Exception):
    """
    An expression indicating that something has gone wrong when evaluating a
    symbolic algebra expression.
    """
    pass

class Var(Expr):
    """Variable Class"""
    precedence= float('inf')

    def __init__(self, name):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"
        
    def evaluate(self, d):
        if self.name not in d:
            raise SymbolicEvaluationError
        else:
            return d[self.name]
            
    def deriv(self,var):
        if self.name == var:
            return Num(1)
        else:
            return Num(0)
            
    def same(self,other):
        """check if self and other are same variable"""
        return self.name == other.name
        
    def simplify(self):
        return Var(self.name)

class Num(Expr):
    """Number Class"""
    precedence= float('inf')
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"
        
    def evaluate(self, d):
        return self.n
        
    def deriv(self, var):
        return Num(0)
        
    def iszero(self):
        return self.n == 0
        
    def isone(self):
        return self.n == 1
        
    def simplify(self):
        return Num(self.n)

class BinOp(Expr):
    """Binary Operation Class"""
    def __init__(self, left, right):
        """Stores and ensures left and right are valid"""
        self.left = Expr.ensure(left)
        self.right = Expr.ensure(right)

    indicator = False

    def parentheses(self, expr, side):
        """Determine if parthenses are needed"""
        expr_str = str(expr)
        # if lower precedence
        if expr.precedence < self.precedence:
            return f'({expr_str})'
        # if self= - or /, check if b.right and if it is - or /
        if self.indicator and side == 'right' and self.precedence == expr.precedence:
            return f'({expr_str})'
        return expr_str
    
    def __str__(self):
        left = self.parentheses(self.left,'left')
        right=  self.parentheses(self.right,'right')
        return f'{left} {self.operator} {right}'

    def __repr__(self):
        name=self.__class__.__name__
        return f'{name}({repr(self.left)},{repr(self.right)})'

class Add(BinOp):
    """Addition Class"""
    # order in PEMDAS
    precedence = 1
    operator = '+'
    
    # def __str__(self):
    #     left = self.parentheses(self.left, 'left')
    #     right = self.parentheses(self.right, 'right')
    #     return f'{left} + {right}'
    
    # def __repr__(self):
    #     return f'Add({repr(self.left)}, {repr(self.right)})'
    
    def evaluate(self,d):
        return self.left.evaluate(d) + self.right.evaluate(d)
        
    def deriv(self,var):
        return self.left.deriv(var) + self.right.deriv(var)
        
    def simplify(self):
        """Simplify for Addition"""
        left = self.left.simplify()
        right = self.right.simplify()
        # if both num, simplify to one number
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n + right.n)
        # if either is 0
        if isinstance(left, Num):
            if left.iszero():
                return right
        if isinstance(right, Num):
            if right.iszero():
                return left
        return Add(left, right)

class Sub(BinOp):
    """Subtraction Class"""
    # is it sub or div
    indicator = True
    # order in PEMDAS
    precedence = 1
    operator = '-'

    # def __str__(self):
    #     left = self.parentheses(self.left, 'left')
    #     right = self.parentheses(self.right, 'right')
    #     return f'{left} - {right}'
    
    # def __repr__(self):
    #     return f'Sub({repr(self.left)}, {repr(self.right)})'
    
    def evaluate(self, d):
        return self.left.evaluate(d) - self.right.evaluate(d)
        
    def deriv(self, var):
        return self.left.deriv(var) - self.right.deriv(var)
        
    def simplify(self):
        """Simplify for Subtraction"""
        left = self.left.simplify()
        right = self.right.simplify()
        # if both num, simplify to one number
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n - right.n)
        # if right is 0
        if isinstance(right, Num):
            if right.iszero():
                return left
        return Sub(left, right)

class Mul(BinOp):
    """Multiplication Class"""
    # order in PEMDAS
    precedence = 2
    operator = '*'
    
    # def __str__(self):
    #     left = self.parentheses(self.left, 'left')
    #     right = self.parentheses(self.right, 'right')
    #     return f'{left} * {right}'

    # def __repr__(self):
    #     return f'Mul({repr(self.left)}, {repr(self.right)})'
    
    def evaluate(self,d):
        return self.left.evaluate(d) * self.right.evaluate(d)
        
    def deriv(self,var):
        return self.left * (self.right.deriv(var)) + self.right * (self.left.deriv(var))
        
    def simplify(self):
        """Simplify for Multiplication"""
        left = self.left.simplify()
        right = self.right.simplify()

        # if both num, simplify to one number
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n * right.n)
        # if left is 1 or 0
        if isinstance(left, Num):
            if left.isone():
                return right
            if left.iszero():
                return Num(0)
        # if right is 1 or 0
        if isinstance(right, Num):
            if right.isone():
                return left
            if right.iszero():
                return Num(0)
        return Mul(left, right)

class Div(BinOp):
    """Division Class"""
    # sub or div
    indicator = True
    # order in PEMDAS
    precedence = 2
    operator = '/'

    # def __str__(self):
    #     left = self.parentheses(self.left, 'left')
    #     right = self.parentheses(self.right, 'right')
    #     return f'{left} / {right}'
    
    # def __repr__(self):
    #     return f'Div({repr(self.left)}, {repr(self.right)})'
    
    def evaluate(self, d):
        return self.left.evaluate(d) / self.right.evaluate(d)
        
    def deriv(self, var):
        top = self.right * (self.left.deriv(var)) - self.left * (self.right.deriv(var))
        return top / (self.right * self.right)
        
    def simplify(self):
        """simplify for Division"""
        left = self.left.simplify()
        right = self.right.simplify()

        # if both num, simplify to one number
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n / right.n)
        # if 0/x=0
        if isinstance(left, Num):
            if left.iszero():
                return Num(0)
        # if x/1=x
        if isinstance(right, Num):
            if right.isone():
                return left
        return Div(left, right)

def seperate_paren(i):
    """Function to seperate ( from strings"""
    if '(' not in i:
        return [i]
    else:
        return ['('] + seperate_paren(i[1:])

def seperate_paren2(i):
    """Function to seperate ) from strings"""
    if ')' not in i:
        return [i]
    else:
        return seperate_paren2(i[:-1]) + [')']

def tokenize(expres):
    """Given expression, tokenize

    >>> tokenize('(x * (2 + 3))')
    ['(', 'x', '*', '(', '2', '+', '3', ')', ')']

    >>> tokenize('x')
    ['x']
    """
    x = expres.split(' ')
    y = []
    for i in x:
        if '(' in i:
            y.extend(seperate_paren(i))
        elif ')' in i:
            y.extend(seperate_paren2(i))
        else:
            y.append(i)
    return y

def parse(tokens):
    """Given tokenized expression, parse it
    
    >>> parse(['(', 'x', '*', '(', '2', '+', '3', ')', ')'])
    Mul(Var('x'),Add(Num(2.0),Num(3.0)))
    
    >>> parse(['x'])
    Var('x')
    """
    def parse_expression(index):
        token = tokens[index]
        if token == '(':
            left = parse_expression(index + 1)
            op = tokens[left[1]]
            right = parse_expression(left[1] + 1)
            if op == '+':
                return Add(left[0], right[0]), (right[1] + 1)
            elif op == '-':
                return Sub(left[0], right[0]), (right[1] + 1)
            elif op == '*':
                return Mul(left[0], right[0]), (right[1] + 1)
            elif op == '/':
                return Div(left[0], right[0]), (right[1] + 1)
        try:
            return Num(float(tokens[index])), (index + 1)
        except ValueError:
            return Var(tokens[index]), (index + 1)
    parsed_expression, next_index = parse_expression(0)
    return parsed_expression

def make_expression(expression):
    """Make expression from string
    """
    tokens = tokenize(expression)
    return parse(tokens)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
