# import os
import sys
from Parser import Parser
from CodeWriter import CodeWriter


def main():
    filename = sys.argv[1]
    parser = Parser(filename)
    writer = CodeWriter(filename)
    writer.writeInit()

    while parser.hasMoreCommands():
        parser.advance()
        lineType = parser.commandType()
        if lineType == 'C_ARITHMETIC':
            writer.writeArithmetic(parser.getCommand())
        elif lineType == 'C_PUSH' or lineType == 'C_POP':
            writer.writePushPop(lineType, parser.arg1(), parser.arg2())
        elif lineType == 'C_LABEL':
            writer.writeLabel(parser.arg1())
        elif lineType == 'C_GOTO':
            writer.writeGoto(parser.arg1())
        elif lineType == 'C_IF':
            writer.writeIf(parser.arg1())
        elif lineType == 'C_CALL':
            writer.writeCall(parser.arg1(), parser.arg2())
        elif lineType == 'C_RETURN':
            writer.writeReturn()
        elif lineType == 'C_FUNCTION':
            writer.writeFunction(parser.arg1(), parser.arg2())


""" run program """
if __name__ == "__main__" and len(sys.argv) == 2:
    main()
