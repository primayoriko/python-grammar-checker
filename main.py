import sys, re

token_list = [
    (r'[ \n\t]+',                                        None),
    (r'#[^\n]*',                                         None),
    (r'(([1-9][0-9]*)?[0-9](\.[0-9]*)?|\.[0-9]+)',     'num'),
    (r'0x[0-9a-fA-F]+',                     'num'),
    (r'->', 'panah'),
    (r'\*\*',        'op'),
    (r'//',        'op'),
    (r'==',        'op'),
    (r'!=',        'op'),
    (r'[\+\-\*/]?=',                    'assign'),
    (r'[\+\*/\-]',        'opm'),
    (r'[><]=?',                           'op'),
    (r'False',                   'false'),
    (r'None',                    'none'),
    (r'True',                    'true'),
    (r'and ',                     'and'),
    (r'as ',                    'as'),
    (r'break',                     'break'),
    (r'class',                    'class'),
    (r'continue',                     'continue'),
    (r'def ',                    'def'),
    (r'elif',                     'elif'),
    (r'else',                   'else'),
    (r'for ',                     'for'),
    (r'from ',                     'from'),
    (r'if',                    'if'),
    (r'import ',                   'import'),
    (r'in ',                    'in'),
    (r'is ',                   'is'),
    (r'not',                    'not'),
    (r'or ',                  'or'),
    (r'pass',                  'pass'),
    (r'while',                 'while'),
    (r'raise',                    'raise'),
    (r'range',                    'range'),
    (r'return ',                   'return'),
    (r'with ',                   'with'),
    (r'print',                   'print'),
    (r'(["\'])(?:(?=(\\?))\2.)*?\1',                   'str'),
    (r'\(',                   '('),
    (r'\)',                   ')'),
    (r'\[',                   '['),
    (r'\]',                   ']'),
    (r'\{',                   '{'),
    (r'\}',                   '}'),
    (r'\:',                   ':'),
    (r'\'',                   '\''),
    (r'\"',                  '"'),
    (r',',                   ','),
    (r'[_a-zA-Z][_a-zA-Z0-9]*(\.[_a-zA-Z][_a-zA-Z0-9]*)*', 'var')
]
def lexer(text_code, token_list):
    pos = 0 
    tokenized = []

    while pos < len(text_code):
        match = None
        for token in token_list:
            pattern, tag = token
            regex = re.compile(pattern)
            match = regex.match(text_code, pos)

            if match:
                #text = match.group(0)
                if tag:
                    #tokenz = (text, tag)
                    tokenz = tag
                    tokenized.append(tokenz)
                break

        if not match:
            tokenized = ["ojanganteng"]
        pos = match.end(0)

    return tokenized 


def parseGrammar(filename):
    rules = {}
    with open(filename, 'r') as file:   
        grammar = file.read().splitlines()
        for i in grammar:
            temp = i.split(' -> ')
            product = temp[1].split(' | ')
            if temp[0] not in rules: rules[temp[0]] = product
            else : rules[temp[0]] += product

    return rules

def readCNF(filepath):
    grammarLeft = []
    grammarRight = []
    with open(filepath) as fp:
        line = fp.readline()

        cnt = 1
        while line:
            a = line.split(" -> ")
            left = a[0]
            right = a[1].split(" | ")

            ln = len(right)
            right[ln - 1] = right[ln - 1][:-1]
            grammarLeft.append(left)
            ss = []
            for g in right:
                if(" " in g):
                    x = g.split(" ")
                    ss.append(x)
                else:
                    x = [g, ""]
                    ss.append(x)
            
            grammarRight.append(ss)
            line = fp.readline()
        return grammarLeft, grammarRight

def isTerminal(a):
    return (a[1] == "" and not(a[0].isupper()))

def CYK(ln, grammarLeft, grammarRight, dp, inp):
    dp = [[[] for j in range(ln + 1)] for i in range(ln + 1)]
    panjang = len(grammarLeft)
    for i in range(ln):
        target = inp[i]

        vc = []
        for t in range(panjang):
            for k in grammarRight[t]:
                if(isTerminal(k) and k[0] == target):
                    if grammarLeft[t] not in vc:
                        vc.append(grammarLeft[t])

        dp[1][i + 1] = vc

    for i in range(2, ln + 1):
        for j in range(1, ln + 1):

            m = j
            n = i + j - 1
            st = []
            if(n <= ln):
                for t in range(m, n):
                    a = m
                    b = t

                    c = t + 1
                    d = n

                    for x in dp[b - a + 1][a]:
                        for y in dp[d - c + 1][c]:
                            yey = [x, y]

                            for q in range(panjang):
                                for k in grammarRight[q]:
                                    if(yey[0] == k[0] and yey[1] == k[1]):
                                        if(grammarLeft[q] not in st):
                                            st.append(grammarLeft[q])
            
            dp[i][j] = st



    return dp

def isValid(dp, ln):
    return (not(dp[ln][1] == [])) and ("STARTSYMBOL" in dp[ln][1])

def printTree(dp, ln):
    for i in range(1, ln + 1):
        for j in range(1, ln + 1):
            if(len(dp[i][j]) == 0):
                print(" - ", end="")
            else:
                print(" [", end="")
                for k in dp[i][j]:
                    print(k + ",", end="")
                print("] ", end="")
        print()



grammarLeft = []
grammarRight = []
grammarLeft, grammarRight = readCNF("cnf.txt")

#inputfile = str(input("masukkan input file : "))

isFunc = False
isLoop = False

ifStack = []
mtlStack = []
idxStack = []
msg = ""
ptr = 0
Er = -1
currline = 1
with open(sys.argv[1]) as fp:
    line = fp.readline()
    while line:
        if(line[-1:] == '\n'):
            inp = line[:-1]
        else:
            inp = line
        if(inp!=""):
            lex = lexer(inp, token_list)
            #print(lex)
            if(not(lex == [])):
                if(lex ==["ojanganteng"]):
                    Er = currline
                    msg = "Error parsing"
                    break
                else:
                    if(lex[0] == "def"):
                        isFunc = True
                    elif(lex[0] == "while" or lex[0] == "for"):
                        isLoop = True
                    elif(lex[0] == "return"):
                        if(isFunc == False):
                            Er = currline
                            msg = "you can't use return! you didn't define any function!"
                            break
                    elif(lex[0] == "continue" or lex[0] == "break"):
                        if(isLoop == False):
                            Er = currline
                            msg = "you can't use that! you didn't define any loop!"
                            break
                    elif(lex[0] == "if"):
                        ifStack.append("if")
                    elif(lex[0] == "elif"):
                        if(len(ifStack) == 0):
                            Er = currline
                            msg = "you cant use elif without if"
                            break
                        else:
                            ifStack.pop()
                            ifStack.append("elif")
                    elif(lex[0] == "else"):
                        if(len(ifStack) == 0):
                            Er = currline
                            msg = "you cant use else without if or elif"
                            break
                        else:
                            ifStack.pop()
                    elif(lex[0] == "mtl" and len(lex) > 1):
                        mtlStack.append("mtl")
                        idxStack.append(currline)
                    elif(lex[0] == "mtl" and len(lex) == 1):
                        if(len(mtlStack) > 0):
                            mtlStack.pop()
                            idxStack.pop()
                        else:
                            mtlStack.append("mtl")
                            idxStack.append(currline)
                    elif(lex[len(lex) - 1] == "mtl"):
                        if(len(mtlStack) > 0):
                            mtlStack.pop()
                            idxStack.pop()
                        else:
                            mtlStack.append("mtl")
                            idxStack.append(currline)


                    if(len(mtlStack) == 0 and not(lex[len(lex) - 1] == "mtl")):
                        dp = []
                        dp = CYK(len(lex), grammarLeft, grammarRight, dp, lex)
                        #printTree(dp, len(lex))
                        if(isValid(dp, len(lex)) == False):
                            Er = currline
                            break
            
            
            
            
            
        currline += 1
        line = fp.readline()
if(Er == -1):
    if(len(mtlStack) == 0):
        print("ACCEPTED")
    else:
        t = idxStack[len(idxStack) - 1]
        print("Syntax Error on line : " + str(t))
        print("Error Message = comment syntax is wrong")
else:
    print("Syntax Error on line : " + str(Er))
    print(msg)
