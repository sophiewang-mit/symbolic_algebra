str1='((x + 2) * (x + 3))'
x=str1.split(' ')
# y=[]
# for i in x:
#     if '(' in i:
#         y.append('(')
#         y.append(i[1:])
#     elif ')' in i:
#         y.append(i[:-1])
#         y.append(')')
#     else:
#         y.append(i)
# print(y)
# # a='2'
def seperate_paren(i):
    if '(' not in i:
        return [i]
    else:
        return ['(']+seperate_paren(i[1:])
    
def seperate_paren2(i):
    if ')' not in i:
        return [i]
    else:
        return seperate_paren2(i[:-1])+[')']

y=[]
for i in x:
    if '(' in i:
        y.extend(seperate_paren(i))
    elif ')' in i:
        y.extend(seperate_paren2(i))
    else:
        y.append(i)
# print(y)

# a='3))'
# print(seperate_paren2(a))

# def bruh(a):
#     return a,1

# print(bruh('b'))

# for i in range(n):
#     print('hello',i)

def repeat_n_times(n,func):
    if n==0:
        return
    func(n)
    repeat_n_times(n-1,func)
print(repeat_n_times(20,lambda i:print('hello',i)))

def counter():
    tally=0
    def increment():
        tally+=1
        return tally
    return increment