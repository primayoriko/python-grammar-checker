
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

def CYK(ln, grammarLeft, grammarRight, dp):
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

inp = ["var", "assign", "var"];
dp = []
grammarLeft = []
grammarRight = []
grammarLeft, grammarRight = readCNF("cnf.txt")
dp = CYK(len(inp), grammarLeft, grammarRight, dp)
printTree(dp, len(inp))

if(isValid(dp, len(inp))):
    print("ACCEPTED")
else:
    print("NOT VALID")
