def isDelimiter(ch):
    delimiters = [' ', '+', '-', '*', '/', ',', ';', '>', '<', '=', '(', ')', '[', ']', '{', '}']
    return True if ch in delimiters else False


def isOperator(ch):
    Operators = ['+', '-', '*', '/', '>', '<', '=', '%']
    return True if ch in Operators else False


def isKeyword(string):
    keywords = ["if", "else", "for", "while", "do", "break", "continue",
                "case", "switch", "unsigned", "void", "static", "auto",
                "goto", "default", "sizeof", "volatile", "const", "union",
                "enum", "register", "extern", "return", "signed", "unsigned",
                "typedef", "struct", "int", "double", "float", "long", "short",
                "char", "bool", "printf", "scanf", "main"]
    return True if string in keywords else False


def printInfo(word, type_of_word, block_number, line_number, column_number):
    print("{}\t\t{}\t\tblockNumber : {}\t\tline : {}\t\tcolumn : {}".format
          (word, type_of_word, block_number, line_number, column_number))


def Parse(string, block_num, line):
    column, cursor_start, state, flag = 1,  0,  0, 0
    for i in range(len(string)):
        if state == 0:
            cursor_start = i
            if string[i] == ' ' or string[i] == '\n' or string[i] == '\t':
                continue
            elif 'A' <= string[i] <= 'Z' or 'a' <= string[i] <= 'z' or string[i] == '_':
                state = 1
                continue
            elif string[i].isdigit():
                state = 2
                continue
            elif isDelimiter(string[i]):
                if string[i] == '{':
                    block_num += 1
                    printInfo(string[i], "Delimiter", block_num, line, i)
                elif string[i] == '}':
                    printInfo(string[i], "Delimiter", block_num, line, i)
                    block_num -= 1
                else:
                    printInfo(string[i], "Delimiter", block_num, line, i)

        elif state == 1:
            if 'A' <= string[i] <= 'Z' or 'a' <= string[i] <= 'z' or string[i] == '_' or string[i].isdigit():
                state = 1
                continue
            elif isDelimiter(string[i]):
                sub = string[cursor_start:i]

                if isKeyword(sub):
                    printInfo(sub, "Keyword", block_num, line, i - len(sub))
                elif len(sub) > 0:
                    printInfo(sub, "Identifier", block_num, line, i - len(sub))

                if isOperator(string[i]):
                    printInfo(string[i], "Operator", block_num, line, i)
                elif string[i] != ' ':
                    printInfo(string[i], "Delimiter", block_num, line, i)

                if string[i] == '{':
                    block_num += 1
                    printInfo(string[i], "Delimiter", block_num, line, i)
                elif string[i] == '}':
                    printInfo(string[i], "Delimiter", block_num, line, i)
                    block_num -= 1
                state = 0
                continue
        elif state == 2:
            if string[i].isdigit():
                state = 2
                continue
            elif 'A' <= string[i] <= 'Z' or 'a' <= string[i] <= 'z' or string[i] == '_' or string[i].isdigit():
                state = 2
                flag = 1
                continue
            elif isDelimiter(string[i]):
                sub = string[cursor_start:i]

                if flag == 1:
                    printInfo(sub, "Invalid Identifier", block_num, line, i - len(sub))
                    flag = 0
                else:
                    printInfo(sub, "Digit", block_num, line, i - len(sub))

                if isOperator(string[i]):
                    printInfo(string[i], "Operator", block_num, line, i)
                elif string[i] != ' ':
                    printInfo(string[i], "Delimiter", block_num, line, i)

                if string[i] == '{':
                    block_num += 1
                    printInfo(string[i], "Delimiter", block_num, line, i)
                elif string[i] == '}':
                    printInfo(string[i], "Delimiter", block_num, line, i)
                    block_num -= 1
                state = 0
                continue
    return block_num


file = open("Test.txt")
line = 1
block_number = 0

for line_of_file in file:
    text = line_of_file
    block_number = Parse(text, block_number, line)
    line += 1
    print()
file.close()
while(True):
	pass