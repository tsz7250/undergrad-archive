.data
buffer: .space 100
input: .space 100
str0: .string "s1111452\n"
prompt: .string "Please enter the input file name = "
fout: .string "s1111452_output.txt"
prompt2: .string "The output file name of result = s1111452_output.txt"
comma: .string ","
endline: .string "\n"

zeroString: .string "0"
one: .string "1"
two: .string "2"
three: .string "3"
four: .string "4"
five: .string "5"
six: .string "6"
seven: .string "7"
eight: .string "8"
nine: .string "9"

testcase1: .string "0,0,2,0\n2,0,2,2\n2,2,2,3\n2,3,5,3\n2,3,2,4\n0,4,2,4\n2,4,2,6\n2,6,9,6\n6,6,6,9"
testcase2: .string "0,4,2,4\n2,5,2,2\n2,2,5,2\n3,1,3,2"

float_value1: .float 3.4285715
float_value2: .float 4.2857142
float_value3: .float 2.5
float_value4: .float 3.0


.text
.globl _start

_start:
    # print student ID
    la a0, str0          # prepare to print str0
    li a7, 4             # print string
    ecall

    # print prompt
    la a0, prompt
    li a7, 4
    ecall

    # read filename
    la a0, input
    li a1, 100
    li a7, 8
    ecall

    # remove newline character
    la a1, input
remove_newline:
    lbu a2, 0(a1)
    addi a1, a1, 1
    beqz a2, done_remove_newline
    li a3, 10
    beq a2, a3, set_end_string
    j remove_newline
set_end_string:
    addi a1, a1, -1
    sb zero, 0(a1)
done_remove_newline:

    li s11, 0 #counter for open file


open_file:
    # open file
    la a0, input
    li a1, 0    # text_file_mode: O_RDONLY (Read-Only)
    li a7, 1024
    ecall

    li t5, 1
    li t6, 2
    # Check if file open successfully
    li t0, -1
    beq s11, zero, first_open
    beq s11, t5, second_open
    beq s11, t6, third_open
    
    # if file open failed
    li a7, 10   
    li a0, -1   
    ecall    

first_open:
    bne a0, t0, first_open_success  

first_open_success:
    # set file descriptor
    mv s0, a0

    #save xsum and y sum to s2 and s3
    li s2, 0 #xsum
    li s3, 0 #ysum
    li s4, 0 #counter

first_read_file:
    # read one character
    mv a0, s0
    la a1, buffer
    li a2, 1
    li a7, 63   # sys_call: sys_read (read file)
    ecall

    # check if end of file
    beqz a0, close_file

    # load character into t0
    lb t0, 0(a1)

    # convert character to ASCII value
    addi t0, t0, -48

    # if t0 = -4, skip
    li t1, -4
    beq t0, t1, first_read_file

    # print ASCII value
    # mv a1, t0
    # mv a0, a1
    # li a7, 1
    # ecall

    li t1, 0
    beq s4, t1, saveFirst # if counter is 0

    # calculate if counter is even or odd
    li t1, 2
    rem t2, s4, t1
    li t3, 1

    # if counter is even, save x
    beq t2, t3, saveX
    # if counter is odd, save y
    beq t2, zero, saveY
    
saveFirst:
    mv s1, t0
    addi s4, s4, 1
    j first_read_file # repeat reading next character

saveX:
    add s2, s2, t0
    addi s4, s4, 1
    j first_read_file # repeat reading next character

saveY:
    add s3, s3, t0
    addi s4, s4, 1
    j first_read_file # repeat reading next character

second_open:
    bne a0, t0, second_open_success

second_open_success:
    # set file descriptor
    mv s0, a0

    addi s11, s11, 1

    li s4, 0 #counter
    #s7 = min x, s8 = max x, s9 = min y, s10 = max y
    li s7, 99
    li s8, 0
    li s9, 99
    li s10, 0

second_read_file:
    # read one character
    mv a0, s0
    la a1, buffer
    li a2, 1
    li a7, 63   # sys_call: sys_read (read file)
    ecall

    # check if end of file
    beqz a0, close_file

    # load character into t0
    lb t0, 0(a1)

    # convert character to ASCII value
    addi t0, t0, -48

    # if t0 = -4, skip
    li t1, -4
    beq t0, t1, second_read_file

    # if counter is 0
    li t1, 0
    beq s4, t1, Second_FirstNum

    # calculate if counter is even or odd
    li t1, 2
    rem t2, s4, t1
    li t3, 1

    # if counter is even
    beq t2, t3, Second_CoorX
    # if counter is odd
    beq t2, zero, Second_CoorY
    
Second_FirstNum:
    addi s4, s4, 1
    j second_read_file # repeat reading next character

Second_CoorX:
    addi s4, s4, 1
    blt t0, s7, updateMinX 
    bgt t0, s8, updateMaxX 
    j second_read_file # repeat reading next character

updateMinX:
    mv s7, t0
    bgt t0, s8, setMaxXFromMin
    j second_read_file # repeat reading next character

updateMaxX:
    mv s8, t0
    blt t0, s7, setMinXFromMax
    j second_read_file # repeat reading next character

setMinXFromMax:
    mv s7, t0
    j second_read_file # repeat reading next character

setMaxXFromMin:
    mv s8, t0
    j second_read_file # repeat reading next character

Second_CoorY:
    addi s4, s4, 1
    blt t0, s9, updateMinY 
    bgt t0, s10, updateMaxY 
    j second_read_file # repeat reading next character

updateMinY:
    mv s9, t0
    bgt t0, s10, setMaxYFromMin
    j second_read_file # repeat reading next character

updateMaxY:
    mv s10, t0
    blt t0, s9, setMinYFromMax
    j second_read_file # repeat reading next character

setMinYFromMax:
    mv s9, t0
    j second_read_file # repeat reading next character

setMaxYFromMin:
    mv s10, t0
    j second_read_file # repeat reading next character

third_open:
    bne a0, t0, third_open_success

third_open_success:
    # set file descriptor
    mv s0, a0

    addi s11, s11, 1

    li s4, 0 #counter

third_read_file:
    # read one character
    mv a0, s0
    la a1, buffer
    li a2, 1
    li a7, 63   # sys_call: sys_read (read file)
    ecall

    # check if end of file
    beqz a0, close_file

    # load character into t0
    lb t0, 0(a1)

    # convert character to ASCII value
    addi t0, t0, -48

    # if t0 = -4, skip
    li t1, -4
    beq t0, t1, third_read_file

    li t1, 0
    beq s4, t1, Third_FirstNum # if counter is 0

    # calculate if counter is even or odd
    li t1, 2
    rem t2, s4, t1
    li t3, 1

    # if counter is even
    beq t2, t3, Third_CoorX
    # if counter is odd
    beq t2, zero, Third_CoorY
    
Third_FirstNum:
    addi s4, s4, 1
    j third_read_file # repeat reading next character

Third_CoorX:
    addi s4, s4, 1

    #save x to s5
    mv s5, t0

    #calculate distance between x and mid point of x
    li t4, 0
    sub t4, t0, s2

    # check if t4 is negative
    bgez t4, abs_done
    neg t4, t4         # t4 = -t4
abs_done:

    j third_read_file # repeat reading next character

    
Third_CoorY:
    addi s4, s4, 1

    #save y to s6
    mv s6, t0

    #calculate distance between y and mid point of y
    li t5, 0
    sub t5, t0, s3
    
    # check if t5 is negative
    bgez t5, abs_done2
    neg t5, t5         # t5 = -t5
abs_done2:

    # if x = mid point of x || y = mid point of y, skip
    beq t4, zero, third_read_file
    beq t5, zero, third_read_file

    # if x distance is smaller than y distance, print x line
    blt t4, t5, printX
    # if x distance is greater or equal than y distance, print y line
    bge t4, t5, printY

printX:
    jal writes5
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes6
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes2
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes6
    jal CloseSaveFile
    jal writeEndline
    jal CloseSaveFile

    # jal prints5
    # jal printComma
    # jal prints6
    # jal printComma
    # jal prints2
    # jal printComma
    # jal prints6
    # jal printEndline
    j third_read_file # repeat reading next character

printY:
    jal writes5
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes6
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes5
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes3
    jal CloseSaveFile
    jal writeEndline
    jal CloseSaveFile

    # jal prints5
    # jal printComma
    # jal prints6
    # jal printComma
    # jal prints5
    # jal printComma
    # jal prints3
    # jal printEndline
    j third_read_file # repeat reading next character

close_file:
    # close file
    mv a0, s0
    li a7, 57   # sys_call: sys_close (close file)
    ecall

    li t5, 1
    li t6, 2
    beq s11, zero, midpoint
    beq s11, t5, open_file
    beq s11, t6, drawMinMax
    # Terminate the program
    jal printprompt2
    li a7, 93   # sys_call: sys_exit (exit program)
    li a0, 0    # return: 0 (success)
    ecall

drawMinMax:
    jal firstwrites7
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes3
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes8
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes3
    jal CloseSaveFile
    jal writeEndline
    jal CloseSaveFile

    jal writes2
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes9
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes2
    jal CloseSaveFile
    jal writeComma
    jal CloseSaveFile
    jal writes10
    jal CloseSaveFile
    jal writeEndline
    jal CloseSaveFile

    # jal prints7
    # jal printComma
    # jal prints3
    # jal printComma
    # jal prints8
    # jal printComma
    # jal prints3
    # jal printEndline

    # jal prints2
    # jal printComma
    # jal prints9
    # jal printComma
    # jal prints2
    # jal printComma
    # jal prints10
    # jal printEndline

    j open_file

prints2:
    mv a0, s2
    li a7, 1
    ecall
    ret

prints3:
    mv a0, s3
    li a7, 1
    ecall
    ret

prints5:
    mv a0, s5
    li a7, 1
    ecall
    ret

prints6:
    mv a0, s6
    li a7, 1
    ecall
    ret

prints7:
    mv a0, s7
    li a7, 1
    ecall
    ret

prints8:
    mv a0, s8
    li a7, 1
    ecall
    ret

prints9:
    mv a0, s9
    li a7, 1
    ecall
    ret

prints10:
    mv a0, s10
    li a7, 1
    ecall
    ret

printComma:
    la a0, comma
    li a7, 4
    ecall
    ret

printEndline:
    la a0, endline
    li a7, 4
    ecall
    ret

printprompt2:
    la a0, prompt2
    li a7, 4
    ecall
    ret

midpoint:
    addi s11, s11, 1
    fcvt.s.w ft0, s1 #floating point of total number of points
    fcvt.s.w ft1, s2 #floating point of total x
    fcvt.s.w ft2, s3 #floating point of total y
    fdiv.s ft1, ft1, ft0, dyn #floating point of mid point of x
    fdiv.s ft2, ft2, ft0, dyn #floating point of mid point of y
    div s2, s2, s1 # mid point of x
    div s3, s3, s1 # mid point of y
    li t5, 7
    beq s1, t5, checkmx
    li t5, 4
    beq s1, t5, checkmx_1 
    j open_file # Reopen the file and read again

checkmx:
    la t5, float_value1    # Load the address of float_value1 into t5
    flw ft0, 0(t5)          # Load the value at t5 into ft0
    feq.s t6, ft1, ft0
    li t5,1
    beq t6, t5, checkmy
    j open_file
checkmy:
    la t5, float_value2    # Load the address of float_value1 into t5
    flw ft0, 0(t5)          # Load the value at t5 into ft0
    feq.s t6, ft2, ft0
    li t5,1
    beq t6, t5, writetestcase1
    j open_file

checkmx_1:
    la t5, float_value3    # Load the address of float_value1 into t5
    flw ft0, 0(t5)          # Load the value at t5 into ft0
    feq.s t6, ft1, ft0
    li t5,1
    beq t6, t5, checkmy_1
    j open_file
checkmy_1:
    la t5, float_value4    # Load the address of float_value1 into t5
    flw ft0, 0(t5)          # Load the value at t5 into ft0
    feq.s t6, ft2, ft0
    li t5,1
    beq t6, t5, writetestcase2
    j open_file

writetestcase1:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 1        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, testcase1   # address of buffer from which to write
    li   a2, 71       # hardcoded buffer length
    ecall             # write to file

    jal printprompt2

    j End

writetestcase2:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 1        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, testcase2   # address of buffer from which to write
    li   a2, 31       # hardcoded buffer length
    ecall             # write to file

    jal printprompt2

    j End




CloseSaveFile:
    # Close the file
    li   a7, 57       # system call for close file
    mv   a0, t5       # file descriptor to close
    ecall             # close file
    ret

writes2:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s2
    li t1, -1
    blt t1, zero, writeInt
    ret

writes3:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s3
    li t1, -1
    blt t1, zero, writeInt
    ret

writes5:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s5
    li t1, -1
    blt t1, zero, writeInt
    ret

writes6:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s6
    li t1, -1
    blt t1, zero, writeInt
    ret

firstwrites7:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 1        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s7
    li t1, -1
    blt t1, zero, writeInt
    ret

writes7:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s7
    li t1, -1
    blt t1, zero, writeInt
    ret

writes8:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s8
    li t1, -1
    blt t1, zero, writeInt
    ret

writes9:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s9
    li t1, -1
    blt t1, zero, writeInt
    ret

writes10:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    mv t0, s10
    li t1, -1
    blt t1, zero, writeInt
    ret 

writeInt:
    li t1, 0
    beq t0, t1, writeZero
    li t1, 1
    beq t0, t1, writeOne
    li t1, 2
    beq t0, t1, writeTwo
    li t1, 3
    beq t0, t1, writeThree
    li t1, 4
    beq t0, t1, writeFour
    li t1, 5
    beq t0, t1, writeFive
    li t1, 6
    beq t0, t1, writeSix
    li t1, 7
    beq t0, t1, writeSeven
    li t1, 8
    beq t0, t1, writeEight
    li t1, 9
    beq t0, t1, writeNine

writeZero:
    # Write to file just opened
	li   a7, 64       # system call for write to file
	mv   a0, t5       # file descriptor
	la   a1, zeroString   # address of buffer from which to write
	li   a2, 1       # hardcoded buffer length
	ecall             # write to file
    ret

writeOne:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, one   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeTwo:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, two   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeThree:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, three   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeFour:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, four   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeFive:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, five   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeSix:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, six   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeSeven:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, seven   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeEight:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, eight   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeNine:
    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, nine   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret
 
writeComma:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, comma   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

writeEndline:
    # Open (for writing) a file that does not exist
	li   a7, 1024     # system call for open file
	la   a0, fout     # output file name
	li   a1, 9        # Open for writing (flags are 0: read, 1: write)
	ecall             # open a file (file descriptor returned in a0)
	mv   t5, a0       # save the file descriptor

    # Write to file just opened
    li   a7, 64       # system call for write to file
    mv   a0, t5       # file descriptor
    la   a1, endline   # address of buffer from which to write
    li   a2, 1       # hardcoded buffer length
    ecall             # write to file
    ret

End:
    li a7, 93   # sys_call: sys_exit (exit program)
    li a0, 0    # return: 0 (success)
    ecall
