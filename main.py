codeTable = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8',
    '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
    'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-',
    '.', '~', '(', ')', '!', '*', '@', ',', ';'
]

decBase = len(codeTable)


def encode(val):
    num = int(val)

    if num == 0:
        return '0'

    res = ''

    while num > 0:
        res = codeTable[int(num % decBase)] + res
        num = int(num / decBase)

    return res


def decoder(val):
    code = str(val)
    j = len(code) - 1

    res = int(0)

    for i in range(0, len(code)):
        num = codeTable.index(code[i])
        res += num * pow(decBase, j)
        j -= 1

    return res
