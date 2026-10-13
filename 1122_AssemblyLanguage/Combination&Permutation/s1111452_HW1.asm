.data
str0: .string "s1111452\n"
str1: .string "input number M = "
str2: .string "input number N = "
str3: .string "P(M,N): "
str4: .string "C(M,N): "
str5: .string "H(M,N): "
str6: .string "M^N: "
overflow: .string "Overflow\n"
NoOutput: .string "P(M,N), C(M,N), H(M,N), M^N: No Output\n"
One: .string "P(M,N), C(M,N), H(M,N), M^N: 1\n"

.text
main:
	jal printSID
	jal printInputM
	jal inputM	# return the result a0	
	jal printInputN
	jal inputN	# return the result a0
	mv s0,a0	# Set s0 equal to the result
	
		
	jal permutation #permutation(s0)
	jal printmPn
	jal printResult #printResult(s0)

	jal combination #combination(s0)
	jal printmCn
	jal printResult #printResult(s0)

	jal RepeatedPermutation #RepeatedPermutation(s0)
	jal printMn	
	jal printResult #printResult(s0)

	jal RepeatedCombination #RepeatedCombination(s0)
	jal printmHn
	jal printResult #printResult(s0)

	j end

factorial: 
	li t0, 1
	mv t1,a0
	bgt a0, s4, printOverflow
	addi t1,t1,-1
loop: 
	bge t0, t1, endfactorial
	mul a0, a0, t1
	addi t1, t1, -1
	jal x0, loop
endfactorial: 
	jr ra

printResult:
	mv a0,s0
	li a7, 1	# print string
 	ecall

	# print a newline
    li a0, 10   # ASCII value for newline
    li a7, 11   # print character
    ecall
 	ret

permutation:
	# save ra
    addi sp, sp, -4
    sw ra, 0(sp)

	# calculate factorial of M
    mv a0, s1
    call factorial
    mv t4, a0

    # calculate factorial of M-N
    sub t5, s1, s2
    mv a0, t5
    call factorial
    mv t5, a0

  	# restore ra
    lw ra, 0(sp)
    addi sp, sp, 4

    # calculate permutation: M! / (M-N)!
    div t6, t4, t5
    mv s0, t6
    ret

combination:
	# save ra
    addi sp, sp, -4
    sw ra, 0(sp)

	# calculate factorial of N
	mv a0, s2
	call factorial
	mv t6, a0

	# restore ra
    lw ra, 0(sp)
    addi sp, sp, 4

	# calculate combination: M! / (N! * (M-N)!)
	mul t3, t6, t5
	div s3, t4, t3
	mv s0, s3
	ret

RepeatedPermutation:	# calculate m^n
	# initialize result to 1
    li t3, 1

    # loop n times
    mv t4, s2
    loop2:
        beqz t4, end_loop
        mul t3, t3, s1
        addi t4, t4, -1
        j loop2

    end_loop:
    mv s0, t3
    ret

RepeatedCombination: # calculate H(M,N)
	# save ra
    addi sp, sp, -4
    sw ra, 0(sp)
	
	# calculate factorial of M+N-1
	add t2, s1, s2
	addi t2, t2, -1
	mv t3, t2
	mv a0, t3
	call factorial
	mv t3, a0

	# calculate factorial of N
	mv a0, s2
	call factorial
	mv t4, a0

	# calulate factorial of (M-N)
	sub t5, t2, s2
	mv a0, t5
	call factorial
	mv t5, a0

	# restore ra
    lw ra, 0(sp)
    addi sp, sp, 4

	# calculate combination: M! / (N! * (M-N)!)
	mul t2, t4, t5
	div t6, t3, t2
	mv s0, t6

	ret

inputM:
	li s4, 12
	li a7,5
	ecall
	mv s1, a0	
	ret
inputN:
	li a7,5
	ecall
	mv s2, a0
	
	#detect M<0 || N<0 || N>M
	bltz s1, PrintNoOutput
    bltz s2, PrintNoOutput
    bge s2, s1, PrintNoOutput

	#detect N==0
	beqz s2, printOne

	ret	

printSID:
	la a0, str0			# prepare to print str0
	li a7, 4			# print string
 	ecall
 	ret
printInputM:
	la a0, str1			# prepare to print str1
	li a7, 4			# print string
 	ecall
 	ret
printInputN:
	la a0, str2		# prepare to print str2
	li a7, 4			# print string
 	ecall
 	ret
printmPn:
	la a0, str3		# prepare to print str3
	li a7, 4			# print string
 	ecall
 	ret
printmCn:
	la a0, str4		# prepare to print str4
	li a7, 4			# print string
 	ecall
 	ret
printmHn:
	la a0, str5		# prepare to print str5
	li a7, 4			# print string
 	ecall
 	ret
printMn:
	la a0, str6		# prepare to print str6
	li a7, 4			# print string
 	ecall
 	ret
PrintNoOutput:
	la a0, NoOutput		# prepare to print NoOutput
	li a7, 4			# print string
 	ecall
 	j end
 	ret
printOne:
	la a0, One		# prepare to print One
	li a7, 4			# print string
 	ecall
 	j end
 	ret
printOverflow:
	la a0, overflow		# prepare to print overflow
	li a7, 4			# print string
 	ecall
 	j end
 	ret

end:
	li a7, 10			
 	ecall
