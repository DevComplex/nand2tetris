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

(MAIN_LOOP)
@KBD
D=M

@PIXEL
M=0

@SET_PIXEL
D;JGT

(PAINT_SCREEN)
@i
M=0			// i = 0

@8191
D=A

@n
M=D

@SCREEN
D=A
@address
M=D	

(PAINT_SCREEN_LOOP)
@i
D=M
@n
D=D-M
@MAIN_LOOP
D;JGT

@PIXEL
D=M

@address
A=M		// writing to memory using a pointer
M=D		// RAM[address] = -1 (16 pixels)
 
@i
M=M+1	// i = i + 1
@1
D=A
@address
M=D+M	// address = address + 32
@PAINT_SCREEN_LOOP
0;JMP		// goto LOOP

(SET_PIXEL)
@PIXEL
M=-1
@PAINT_SCREEN
0;JMP


