// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(START)
@SCREEN
D=A
@0
M=D     // screen map at RAM[0]

(CHECK)
@KBD
D=M
@PRESSED
D;JGT
@NOTPRESSED
D;JEQ

@CHECK
0;JMP   // jump back to check if key is pressed


/// If pressed (black)
(PRESSED)
@1
M=-1    // In binary: 1111111111111111
@UPDATESCREEN
0;JMP

/// If not (white)
(NOTPRESSED)
@1
M=0     // In binary: 0000000000000000)
@UPDATESCREEN
0;JMP


(UPDATESCREEN)
@1      // Saved value for pixels
D=M     // Set D to register for either black or white

@0
A=M     // Adress for the screen pixel to fill
M=D     // Set this to D for either black or white pixel

@0
D=M+1   // Next pixel
@KBD
D=A-D

@0
M=M+1
A=M

@CHECK
D;JGT   // if A > 0 continue

@START
0;JMP