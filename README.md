# Symbolic Algebra System

## Overview
This project implements a symbolic algebra engine in Python capable of constructing, evaluating, differentiating, simplifying, and parsing mathematical expressions.

Expressions are represented as recursive expression trees, allowing algebraic operations to be performed symbolically rather than numerically.

The system supports variables, constants, arithmetic operations, symbolic differentiation, expression simplification, and parsing of fully parenthesized expressions.

---

## Features

### Symbolic Expression Construction
Expressions can be built naturally using Python operators.

```python
x = Var("x")

expr = (x + 2) * (x - 3)
```

Resulting expression:
```text
(x + 2) * (x - 3)
```

---

### Expression Evaluation

Evaluate symbolic expressions by providing values for variables.

```python
expr.evaluate({"x": 5})
```

Output:

```text
14
```

---

### Symbolic Differentiation
Compute derivatives symbolically with respect to a chosen variable.

```python
expr.deriv("x")
```

Example:

```text
(x + 2)(1) + (x - 3)(1)
```

The system implements:
- Constant Rule
- Variable Rule
- Sum Rule
- Difference Rule
- Product Rule
- Quotient Rule

---

### Expression Simplification
Expressions can be simplified using algebraic identities.

Examples:

```text
x + 0 → x
0 + x → x
x * 1 → x
1 * x → x
x * 0 → 0
0 * x → 0
x / 1 → x
0 / x → 0
```

Constant-only subexpressions are automatically evaluated.

Example:

```text
(2 + 3) → 5
```

---

### Expression Parsing

Convert strings into symbolic expression trees.

```python
make_expression("(x * (2 + 3))")
```

Produces:

```python
Mul(Var("x"), Add(Num(2), Num(3)))
```

The parser supports:
- Addition
- Subtraction
- Multiplication
- Division
- Nested parenthesized expressions

---

## Implementation

### Expression Hierarchy
All expressions inherit from a common base class:

```text
Expr
├── Var
├── Num
└── BinOp
    ├── Add
    ├── Sub
    ├── Mul
    └── Div
```

---

### Operator Overloading
Python operator overloading allows expressions to be written naturally.

```python
x + y
x - y
x * y
x / y
```

instead of:
```python
Add(x, y)
Sub(x, y)
Mul(x, y)
Div(x, y)
```

---

### Recursive Expression Trees
Expressions are represented as trees.

Example:

```text
(x + 2) * (x - 3)
```

is stored as:

```text
        *
      /   \
     +     -
    / \   / \
   x  2  x  3
```

This structure enables recursive evaluation, differentiation, and simplification.

---

## Example Usage

### Create Variables
```python
x = Var("x")
y = Var("y")
```

### Build an Expression
```python
expr = (x + 2) * (y - 1)
```

### Evaluate
```python
expr.evaluate({
    "x": 3,
    "y": 4
})
```

### Differentiate
```python
expr.deriv("x")
```

### Simplify
```python
expr.deriv("x").simplify()
```

---

## Skills Demonstrated
- Python
- Object-Oriented Programming
- Recursive Data Structures
- Expression Trees
- Symbolic Computation
- Parsing
- Operator Overloading
- Tree Traversal Algorithms
- Recursive Simplification
- Mathematical Software Design

---

## Applications
The techniques used in this project form the foundation of:

- Computer Algebra Systems
- Symbolic Mathematics Software
- Scientific Computing Tools
- Mathematical Modeling Systems
- Programming Language Compilers
- Expression Evaluators

Examples include software such as Mathematica, Maple, and SymPy.
