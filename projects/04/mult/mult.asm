// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R2
M=0     // set RAM[2] = 0

@R1
D=M     // D = RAM[1]

@END
D;JEQ   // terminate if R1 = 0

@R0
D=M     // D = RAM[0]

@END
D;JEQ   // terminate if R0 = 0

(LOOP)
@R0
D=M

@R2
M=M+D   // For each iteration, plus R2 with R0

@R1
M=M-1   // Decrement R1, each iteration
D=M

@LOOP
D;JGT   // if R1 > 0 goto R2

(END)
@END
0;JMP   // terminate the program