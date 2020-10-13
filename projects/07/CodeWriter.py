class CodeWriter():
    """
    Writes the assembly code that implements the parsed command
    """

    def __init__(self, filename):
        """Opens the output file and gets ready to write into it."""
        self.outfile = open(filename + '.asm', 'w')
        self.filename = filename
        self._current_function = 'none'
        self._counter = 0
        self._a_counter = 0

    def __del__(self):
        """Closes the output file."""
        self.outfile.write('(END)\n')
        self.outfile.write('@END\n')
        self.outfile.write('0;JMP\n')
        self.outfile.close()

    def writeArithmetic(self, command):
        """Writes the assembly code for the corresponding math command."""
        if command == 'add':
            self.outfile.write('@SP\nA=M-1\nD=M\nA=A-1\nM=D+M\nD=A+1\n')
            self.outfile.write('@SP\nM=D\n')
        elif command == 'sub':
            self.outfile.write('@SP\nA=M-1\nD=M\nA=A-1\nM=M-D\nD=A+1\n')
            self.outfile.write('@SP\nM=D\n')
        elif command == 'neg':
            self.outfile.write('@SP\nA=M-1\nM=-M\n')
        elif command == 'and':
            self.outfile.write('@SP\nA=M-1\nD=M\nA=A-1\nM=D&M\n@SP\nM=M-1\n')
        elif command == 'or':
            self.outfile.write('@SP\nA=M-1\nD=M\nA=A-1\nM=D|M\n@SP\nM=M-1\n')
        elif command == 'not':
            self.outfile.write('@SP\nA=M-1\nM=!M\n')
        elif command == 'eq':
            self.outfile.write('@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@SP\n')
            self.outfile.write('M=M-1\n')
            self.outfile.write('@EQUAL_' + str(self._a_counter) + '\n')
            self.outfile.write('D;JEQ\n')
            self.outfile.write('@NOT_EQUAL_' + str(self._a_counter) + '\n')
            self.outfile.write('D;JNE\n')
            self.outfile.write('(EQUAL_' + str(self._a_counter) + ')\n')
            self.outfile.write('@SP\nA=M-1\nM=-1\n')
            self.outfile.write('@END_EQ_' + str(self._a_counter) + '\n')
            self.outfile.write('0;JMP\n')
            self.outfile.write('(NOT_EQUAL_' + str(self._a_counter) + ')\n')
            self.outfile.write('@SP\nA=M-1\nM=0\n')
            self.outfile.write('@END_EQ_' + str(self._a_counter) + '\n')
            self.outfile.write('0;JMP\n')
            self.outfile.write('(END_EQ_' + str(self._a_counter) + ')\n')
        elif command == 'gt':
            self.outfile.write('@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\n')
            self.outfile.write('M=M-1\n')
            self.outfile.write('@GREATER_' + str(self._a_counter) + '\n')
            self.outfile.write('D;JGT\n')
            self.outfile.write('@LESS_EQUAL_' + str(self._a_counter) + '\n')
            self.outfile.write('D;JLE\n')
            self.outfile.write('(GREATER_' + str(self._a_counter) + ')\n')
            self.outfile.write('@SP\nA=M-1\nM=-1\n')
            self.outfile.write('@END_GT_' + str(self._a_counter) + '\n')
            self.outfile.write('0;JMP\n')
            self.outfile.write('(LESS_EQUAL_' + str(self._a_counter) + ')\n')
            self.outfile.write('@SP\nA=M-1\nM=0\n')
            self.outfile.write('@END_GT_' + str(self._a_counter) + '\n')
            self.outfile.write('0;JMP\n')
            self.outfile.write('(END_GT_' + str(self._a_counter) + ')\n')
        elif command == 'lt':
            self.outfile.write('@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\n')
            self.outfile.write('M=M-1\n')
            self.outfile.write('@LESS_' + str(self._a_counter) + '\n')
            self.outfile.write('D;JLT\n')
            self.outfile.write('@GE_' + str(self._a_counter) + '\n')
            self.outfile.write('D;JGE\n')
            self.outfile.write('(LESS_' + str(self._a_counter) + ')\n')
            self.outfile.write('@SP\nA=M-1\nM=-1\n')
            self.outfile.write('@END_LT_' + str(self._a_counter) + '\n')
            self.outfile.write('0;JMP\n')
            self.outfile.write('(GE_' + str(self._a_counter) + ')\n')
            self.outfile.write('@SP\nA=M-1\nM=0\n')
            self.outfile.write('@END_LT_' + str(self._a_counter) + '\n')
            self.outfile.write('0;JMP\n')
            self.outfile.write('(END_LT_' + str(self._a_counter) + ')\n')
        self._a_counter += 1

    def writePushPop(self, command, segment, index):
        """Writes the assembly code that is the translation of the given
           command where command is either C_PUSH or C_POP."""
        if command == 'C_PUSH':
            if segment == 'constant':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write('D=A\n@SP\nA=M\n')
                self.outfile.write('M=D\n@SP\nM=M+1\n')
            if segment == 'local':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@LCL\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            if segment == 'argument':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@ARG\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            if segment == 'this':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@THIS\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            if segment == 'that':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@THAT\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            if segment == 'pointer':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@3\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            if segment == 'temp':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@5\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            if segment == 'static':
                self.outfile.write('@' + self._file_name +
                                   '.' + str(index) + '\n')
                self.outfile.write('D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        if command == 'C_POP':
            if segment == 'local':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@LCL\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\nA=M\nM=D\n')
            if segment == 'argument':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@ARG\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\nA=M\nM=D\n')
            if segment == 'this':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@THIS\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\nA=M\nM=D\n')
            if segment == 'that':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@THAT\nD=D+M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\nA=M\nM=D\n')
            if segment == 'pointer':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@3\nD=D+A\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\nA=M\nM=D\n')
            if segment == 'temp':
                self.outfile.write('@' + str(index) + '\n')
                self.outfile.write(
                    'D=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R14\nM=D\n@SP\nM=M-1\n@R14\nD=M\n@R13\nA=M\nM=D\n')
            if segment == 'static':
                self.outfile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n')
                self.outfile.write('@' + self._file_name +
                                   '.' + str(index) + '\n')
                self.outfile.write('M=D\n')

    def writeLabel(self, label):
        """Writes assembly code that effects the label command."""
        self.outfile.write('(' + self._current_function + '$' + label + ')\n')

    def writeGoto(self, label):
        """Writes assembly code that effects the goto command."""
        self.outfile.write('@' + self._current_function + '$' + label + '\n')
        self.outfile.write('0;JMP\n')

    def writeIf(self, label):
        """Writes assembly code that effects the if-goto command."""
        self.outfile.write('@SP\nA=M-1\nD=M\n@SP\nM=M-1\n')
        self.outfile.write('@' + self._current_function + '$' + label + '\n')
        self.outfile.write('D;JNE\n')

    def writeCall(self, func_name, num_args):
        """Writes assembly code that effects the call command."""
        self.outfile.write('@RET_' + func_name + '_')
        self.outfile.write(str(self._counter) + '\n')
        self.outfile.write('D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@' + str(num_args) + '\n')
        self.outfile.write('D=A\n@SP\nD=M-D\n@5\nD=D-A\n@ARG\nM=D\n')
        self.outfile.write('@SP\nD=M\n@LCL\nM=D\n')
        self.outfile.write('@' + func_name + '\n')
        self.outfile.write('0;JMP\n')
        self.outfile.write('(RET_' + func_name + '_')
        self.outfile.write(str(self._counter) + ')\n')
        self._counter += 1

    def writeReturn(self):
        """Writes the assembly code that effects the return command."""
        self.outfile.write('@LCL\nD=M\n@FRAME\nM=D\n')
        self.outfile.write('@5\nD=A\n@FRAME\nD=M-D\nA=D\nD=M\n@RET\nM=D')
        self.outfile.write('\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n')
        self.outfile.write('@ARG\nD=M\n@SP\nM=D+1\n')
        self.outfile.write('@1\nD=A\n@FRAME\nA=M-D\nD=M\n@THAT\nM=D\n')
        self.outfile.write('@2\nD=A\n@FRAME\nA=M-D\nD=M\n@THIS\nM=D\n')
        self.outfile.write('@3\nD=A\n@FRAME\nA=M-D\nD=M\n@ARG\nM=D\n')
        self.outfile.write('@4\nD=A\n@FRAME\nA=M-D\nD=M\n@LCL\nM=D\n')
        self.outfile.write('@RET\nA=M\n0;JMP\n')

    def writeFunction(self, func_name, num_locals):
        """Writes assembly code that effects the function command."""
        self.outfile.write('(' + func_name + ')\n')
        self.outfile.write('@' + str(num_locals) + '\n')
        self.outfile.write('D=A\n@END_LOOP_' + func_name + '\n')
        self.outfile.write('D;JLE\n(LOOP_' + func_name + ')\n')
        self.outfile.write('@SP\nA=M\nM=0\n@SP\nM=M+1\nD=D-1\n')
        self.outfile.write('@LOOP_' + func_name + '\nD;JGT\n')
        self.outfile.write('(END_LOOP_' + func_name + ')\n')
        self._current_function = func_name

    def writeInit(self):
        """Writes the bootstrap code."""
        self.outfile.write('@256\nD=A\n@SP\nM=D\n')
        self.outfile.write('@RET_Sys.init\n')
        self.outfile.write('D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.outfile.write('D=0\n@SP\nD=M-D\n@5\nD=D-A\n@ARG\nM=D\n')
        self.outfile.write('@SP\nD=M\n@LCL\nM=D\n')
        self.outfile.write('@Sys.init\n')
        self.outfile.write('0;JMP\n')
        self.outfile.write('(RET_Sys.init)\n')
