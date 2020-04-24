# syscall constants
PRINT_STRING            = 4
PRINT_CHAR              = 11
PRINT_INT               = 1

# memory-mapped I/O
VELOCITY                = 0xffff0010
ANGLE                   = 0xffff0014
ANGLE_CONTROL           = 0xffff0018

BOT_X                   = 0xffff0020
BOT_Y                   = 0xffff0024
GET_OPPONENT_HINT       = 0xffff00ec

TIMER                   = 0xffff001c
ARENA_MAP               = 0xffff00dc

SHOOT_UDP_PACKET        = 0xffff00e0
GET_BYTECOINS           = 0xffff00e4
USE_SCANNER             = 0xffff00e8

REQUEST_PUZZLE          = 0xffff00d0  ## Puzzle
SUBMIT_SOLUTION         = 0xffff00d4  ## Puzzle

BONK_INT_MASK           = 0x1000
BONK_ACK                = 0xffff0060

TIMER_INT_MASK          = 0x8000
TIMER_ACK               = 0xffff006c

REQUEST_PUZZLE_INT_MASK = 0x800       ## Puzzle
REQUEST_PUZZLE_ACK      = 0xffff00d8  ## Puzzle

RESPAWN_INT_MASK        = 0x2000      ## Respawn
RESPAWN_ACK             = 0xffff00f0  ## Respawn

# our constants
DEBUG = 0

.data
### Movement Pattern
# -360 to 360	absolute angle
# 1500 +- v	velocity
# 2000		UDP, may be contingent on previous check of arena map
# 3000 + x	Check arena map, x
# 3000 + y	Check arena map, y
# 90000		End program
# 100000 + cm	Set current_move to cm
# 100000000 + c	Delay c cycles

movement:
.word 45 1502 100452548 1500 -135 2000 127 2000 -37 2000 66 1502 100665463 1500 -95 2000 12 2000 139 1502 100307121 1500 65 2000 -19 2000 -179 1502 100103494 1500 -155 2000 100 2000 0 1502 100096497 1500 -40 1502 100298258 1500 24 1502 100714507 1500 47 2000 -52 2000 139 2000 -114 1502 100713481 1500 -55 1502 100349511 1500 -113 2000 108 2000 34 2000 -85 1502 100032116 1500 -11 2000 104 1502 100039143 1500 125 1502 100359135 1500 -156 1502 100663747 1500 -139 2000 128 2000 -38 2000 67 1502 100662689 1500 -94 2000 11 2000 138 1502 100302417 1500 65 2000 -20 2000 -179 1502 100104748 1500 -155 2000 101 2000 0 1502 100095249 1500 -40 1502 100297896 1500 24 1502 100713007 1500 47 2000 -53 2000 140 2000 -114 1502 100714810 1500 -56 1502 100349556 1500 -112 2000 106 2000 34 2000 -77 1502 100030184 1500 -10 2000 104 1502 100041053 1500 125 1502 100356236 1500 -156 1502 100664227 1500 -136 2000 128 2000 -38 2000 67 1502 100660242 1500 -94 2000 11 2000 139 1502 100299858 1500 65 2000 -17 2000 178 1502 100104274 1500 -155 2000 101 2000 0 1502 100095699 1500 -40 1502 100298900 1500 24 1502 100712992 1500 47 2000 -53 2000 140 2000 -114 1502 100715550 1500 -55 1502 100348009 1500 -113 2000 107 2000 35 2000 -82 1502 100029611 1500 -12 2000 104 1502 100036659 1500 125 1502 100356901 1500 -156 1502 100664406 1500 -137 2000 128 2000 -38 2000 67 1502 100660552 1500 -94 2000 11 2000 139 1502 100300516 1500 64 2000 -18 2000 -179 1502 100100895 1500 -155 2000 99 2000 0 1502 100099101 1500 -40 1502 100299873 1500 24 1502 100717103 1500 47 2000 -53 2000 140 2000 -114 1502 100715645 1500 -55 1502 100346987 1500 -113 2000 107 2000 35 2000 -84 1502 100029041 1500 -11 2000 105 1502 100037262 1500 125 1502 100357305 1500 -156 1502 100663864 1500 -137 2000 128 2000 -38 2000 67 1502 100661303 1500 -94 2000 11 2000 139 1502 100300756 1500 64 2000 -18 2000 179 1502 100100610 1500 -154 2000 99 2000 0 1502 100099383 1500 -40 1502 100301900 1500 24 1502 100714050 1500 48 2000 -52 2000 139 2000 -114 1502 100712990 1500 -55 1502 100348169 1500 -113 2000 108 2000 35 2000 -86 1502 100031070 1500 -11 2000 104 1502 100040238 1500 125 1502 100355552 1500 -155 1502 100664582 1500 -146 2000 128 2000 -37 2000 67 1502 100667317 1500 -95 2000 12 2000 139 1502 100308251 1500 65 2000 -18 2000 179 1502 100103444 1500 -155 2000 100 2000 0 1502 100096548 1500 -40 1502 100299401 1500 24 1502 100713856 1500 46 2000 -52 2000 140 2000 -114 1502 100714997 1500 -56 1502 100350944 1500 -113 2000 107 2000 35 2000 -79 1502 100026607 1500 -11 2000 104 1502 100039630 1500 125 1502 100359523 1500 -156 1502 100663482 1500 -139 2000 128 2000 -38 2000 67 1502 100663191 1500 -94 2000 12 2000 138 1502 100302711 1500 65 2000 -19 2000 -179 1502 100104678 1500 -155 2000 101 2000 0 1502 100095314 1500 -40 1502 100297605 1500 24 1502 100713279 1500 48 2000 -53 2000 139 2000 -114 1502 100714313 1500 -56 1502 100349161 1500 -112 2000 106 2000 34 2000 -77 1502 100029692 1500 -12 2000 104 1502 100036541 1500 125 1502 100356655 1500 -156 1502 100664045 1500 -137 2000 128 2000 -38 2000 67 1502 100660692 1500 -94 2000 11 2000 139 1502 100300201 1500 64 2000 -18 2000 -179 1502 100100492 1500 -155 2000 99 2000 0 1502 100099503 1500 -40 1502 100300191 1500 24 1502 100715314 1500 51 2000 -53 2000 140 2000 -115 1502 100714194 1500 -55 1502 100355644 1500 -113 2000 107 2000 35 2000 -83 1502 100027376 1500 -11 2000 105 1502 100038931 1500 125 1502 100358845 1500 -156 1502 100663530 1500 -139 2000 128 2000 -38 2000 67 1502 100662672 1500 -94 2000 11 2000 138 1502 100302096 1500 65 2000 -20 2000 -178 1502 100104450 1500 -155 2000 101 2000 0 1502 100095518 1500 -40 1502 100297044 1500 24 1502 100713902 1500 48 2000 -52 2000 139 2000 -114 1502 100713249 1500 -56 1502 100348369 1500 -112 2000 106 2000 34 2000 -76 1502 100028682 1500 -11 2000 104 1502 100037549 1500 125 1502 100357591 1500 -156 1502 100663860 1500 -137 2000 128 2000 -38 2000 67 1502 100661507 1500 -94 2000 11 2000 138 1502 100301019 1500 65 2000 -20 2000 -178 1502 100104243 1500 -155 2000 101 2000 0 1502 100095745 1500 -40 1502 100298115 1500 24 1502 100713556 1500 47 2000 -52 2000 139 2000 -114 1502 100714387 1500 -56 1502 100349634 1500 -112 2000 106 2000 34 2000 -76 1502 100030064 1500 -10 2000 104 1502 100041169 1500 125 1502 100356338 1500 -156 1502 100664194 1500 -136 2000 128 2000 -38 2000 67 1502 100660343 1500 -94 2000 11 2000 139 1502 100299945 1500 65 2000 -17 2000 178 1502 100104292 1500 -155 2000 101 2000 0 1502 100095684 1500 -40 1502 100298814 1500 24 1502 100713026 1500 47 2000 -53 2000 140 2000 -114 1502 100715451 1500 -55 1502 100347906 1500 -113 2000 107 2000 35 2000 -82 1502 100029495 1500 -12 2000 104 1502 100036774 1500 125 1502 100357003 1500 -156 1502 100664372 1500 -137 2000 128 2000 -38 2000 67 1502 100660653 1500 -94 2000 11 2000 139 1502 100300602 1500 64 2000 -18 2000 -179 1502 100100909 1500 -155 2000 99 2000 0 1502 100099088 1500 -40 1502 100299787 1500 24 1502 100717138 1500 47 2000 -53 2000 140 2000 -114 1502 100715546 1500 -55 1502 100346884 1500 -113 2000 107 2000 35 2000 -84 1502 100028924 1500 -11 2000 105 1502 100037378 1500 125 1502 100357407 1500 -156 1502 100663830 1500 -137 2000 128 2000 -38 2000 67 1502 100661404 1500 -94 2000 11 2000 138 1502 100300843 1500 65 2000 -20 2000 -178 1502 100104147 1500 -155 2000 101 2000 0 1502 100095845 1500 -40 1502 100298292 1500 24 1502 100713584 1500 47 2000 -52 2000 139 2000 -114 1502 100714484 1500 -56 1502 100349818 1500 -112 2000 106 2000 34 2000 -76 1502 100030237 1500 -10 2000 104 1502 100040995 1500 125 1502 100356155 1500 -156 1502 100664164 1500 -136 2000 128 2000 -38 2000 67 1502 100660240 1500 -94 2000 11 2000 139 1502 100299768 1500 65 2000 -17 2000 178 1502 100104187 1500 -155 2000 101 2000 0 1502 100095786 1500 -40 1502 100298991 1500 24 1502 100713055 1500 46 2000 -53 2000 140 2000 -114 1502 100715548 1500 -55 1502 100348090 1500 -113 2000 107 2000 35 2000 -82 1502 100029661 1500 -12 2000 104 1502 100036600 1500 125 1502 100356820 1500 -156 1502 100664343 1500 -137 2000 128 2000 -38 2000 67 1502 100660550 1500 -94 2000 11 2000 139 1502 100300426 1500 64 2000 -18 2000 -179 1502 100100808 1500 -155 2000 99 2000 0 1502 100099187 1500 -40 1502 100299963 1500 24 1502 100717166 1500 47 2000 -53 2000 140 2000 -114 1502 100715643 1500 -55 1502 100347067 1500 -113 2000 107 2000 35 2000 -84 1502 100029087 1500 -11 2000 105 1502 100037203 1500 125 1502 100357224 1500 90000

current_move: .word 0

### Puzzle
puzzle:     .byte 0:268
solution:   .byte 0:256
has_puzzle: .word 0

#############
# Main code #
#############
.text
main:
	# Construct interrupt mask
	li      $t4, 0
	or      $t4, $t4, REQUEST_PUZZLE_INT_MASK	# puzzle interrupt bit
	or      $t4, $t4, RESPAWN_INT_MASK		# respawn interrupt bit
	or      $t4, $t4, TIMER_INT_MASK		# timer interrupt bit
	or      $t4, $t4, 1				# global enable
	mtc0    $t4, $12

	li	$t0, 1000
	sw	$t0, TIMER

	la      $s0, puzzle

request_puzzle:
	sw      $s0, REQUEST_PUZZLE

check_puzzle_available:
	lw      $t0, has_puzzle
	beq     $t0, $zero, check_puzzle_available

	la      $a0, puzzle				# load arguments
	la      $a1, solution
	li      $a2, 0
	li      $a3, 0

	jal	solve					# call solver

	la	$t0, solution				# submit solution
	sw	$t0, SUBMIT_SOLUTION

	sw	$zero, has_puzzle			# reset has_puzzle

	j	request_puzzle

	jr      $ra

###############
# Kernel code #
###############
.kdata
chunkIH:    .space 40
non_intrpt_str:    .asciiz "Non-interrupt exception\n"
unhandled_str:    .asciiz "Unhandled interrupt type\n"
.ktext 0x80000180
interrupt_handler:
.set noat
	move    $k1, $at        # Save $at
# NOTE: Don't touch $k1 or else you destroy $at!
.set at
	la      $k0, chunkIH
	sw      $a0, 0($k0)        # Get some free registers
	sw      $v0, 4($k0)        # by storing them to a global variable
	sw      $t0, 8($k0)
	sw      $t1, 12($k0)
	sw      $t2, 16($k0)
	sw      $t3, 20($k0)
	sw      $t4, 24($k0)
	sw      $t5, 28($k0)

    # Save coprocessor1 registers!
    # If you don't do this and you decide to use division or multiplication
    #   in your main code, and interrupt handler code, you get WEIRD bugs.
	mfhi    $t0
	sw      $t0, 32($k0)
	mflo    $t0
	sw      $t0, 36($k0)

	mfc0    $k0, $13                # Get Cause register
	srl     $a0, $k0, 2
	and     $a0, $a0, 0xf           # ExcCode field
	bne     $a0, 0, non_intrpt

interrupt_dispatch:                 # Interrupt:
	mfc0    $k0, $13                # Get Cause register, again
	beq     $k0, 0, done            # handled all outstanding interrupts

	and     $a0, $k0, TIMER_INT_MASK    # is there a timer interrupt?
	bne     $a0, 0, timer_interrupt

	and     $a0, $k0, BONK_INT_MASK     # is there a bonk interrupt?
	bne     $a0, 0, bonk_interrupt

	and     $a0, $k0, REQUEST_PUZZLE_INT_MASK
	bne     $a0, 0, request_puzzle_interrupt

	and     $a0, $k0, RESPAWN_INT_MASK
	bne     $a0, 0, respawn_interrupt

	li      $v0, PRINT_STRING       # Unhandled interrupt types
	la      $a0, unhandled_str
	syscall
	j       done

bonk_interrupt:
	sw      $0, BONK_ACK
    #Fill in your bonk handler code here
	j       interrupt_dispatch      # see if other interrupts are waiting

### Movement Pattern
# -360 to 360	absolute angle
# 1500 +- v	velocity
# 2000		UDP, may be contingent on previous check of arena map
# 3000 + x	Check arena map, x
# 3000 + y	Check arena map, y
# 100000000 + c	Delay c cycles

timer_interrupt:
	sw      $zero, TIMER_ACK

	lw	$t0, current_move

execute_until_delay:
	lw	$t1, movement($t0)

	add	$t0, $t0, 4

	li	$t9, DEBUG
	beq	$t9, $zero, no_debug

	li      $v0, PRINT_INT
	lw      $a0, BOT_X
	syscall
	li	$v0, PRINT_CHAR
	li	$a0, ','
	syscall
	li      $v0, PRINT_INT
	lw      $a0, BOT_Y
	syscall
	li	$v0, PRINT_CHAR
	li	$a0, '\n'
	syscall

no_debug:
	blt	$t1, 1000, execute_angle
	blt	$t1, 2000, execute_velocity
	beq	$t1, 2000, execute_udp
	beq	$t1, 90000, return_end
	blt	$t1, 100000000, execute_jump
	j	return_delay

execute_angle:
	sw	$t1, ANGLE
	li	$t2, 1
	sw	$t2, ANGLE_CONTROL
	j	execute_until_delay

execute_velocity:
	sub	$t2, $t1, 1500
	sw	$t2, VELOCITY
	j	execute_until_delay

execute_udp:
	sw	$zero, SHOOT_UDP_PACKET
	j	execute_until_delay

execute_jump:
	sub	$t0, $t1, 100000
	j	execute_until_delay

return_delay:
	sub	$t1, $t1, 100000000
	lw	$t2, TIMER
	add	$t2, $t2, $t1
	sw	$t2, TIMER

return_end:
	sw	$t0, current_move
	j       interrupt_dispatch     # see if other interrupts are waiting

request_puzzle_interrupt:
	sw      $0, REQUEST_PUZZLE_ACK
    #Fill in your puzzle interrupt code here

	# Write true to M[has_puzzle]
	la	$t0, has_puzzle
	li	$t1, 1
	sw	$t1, ($t0)

	j       interrupt_dispatch

respawn_interrupt:
	sw      $0, RESPAWN_ACK
    #Fill in your respawn handler code here
	j       interrupt_dispatch

non_intrpt:                         # was some non-interrupt
	li      $v0, PRINT_STRING
	la      $a0, non_intrpt_str
	syscall                         # print out an error message
# fall through to done

done:
	la      $k0, chunkIH

    # Restore coprocessor1 registers!
    # If you don't do this and you decide to use division or multiplication
    #   in your main code, and interrupt handler code, you get WEIRD bugs.
	lw      $t0, 32($k0)
	mthi    $t0
	lw      $t0, 36($k0)
	mtlo    $t0

	lw      $a0, 0($k0)             # Restore saved registers
	lw      $v0, 4($k0)
	lw      $t0, 8($k0)
	lw      $t1, 12($k0)
	lw      $t2, 16($k0)
	lw      $t3, 20($k0)
	lw      $t4, 24($k0)
	lw      $t5, 28($k0)

.set noat
	move    $at, $k1        # Restore $at
.set at
	eret


###############
# Solver code #
###############
.text

.globl toggle_light
toggle_light:
    ## Variables corresponding to registers:

    ##
    ##    $t6 = tmp_var
    ##    $t5 = array_index
    ##    $t3 = board
    ##    $t4 = cond_var
    ##    $t2 = num_colors
    ##    $t1 = num_cols
    ##    $t0 = num_rows
    ##    $a3 = action_num
    ##    $a2 = puzzle
    ##    $a1 = col
    ##    $a0 = row
    ##
	## End aliases



	# assign  $t0   = *0($a2)
	lw      $t0, 0($a2)
	# assign  $t1   = *4($a2)
	lw      $t1, 4($a2)
	# assign  $t2 = *8($a2)
	lw      $t2, 8($a2)
	# assign  $t3   = 12($a2)
	add      $t3, $a2, 12

	# assign  $t5 = $t3&[$a0 * $t1 + $a1]
	mul     $t5, $a0, $t1
	add     $t5, $t5, $a1
	add     $t5, $t5, $t3
	# assign  $t6 = (*::($t5) + $a3) % $t2
	lbu     $t6, 0($t5)
	add     $t6, $t6, $a3
	div     $t6, $t2
	mfhi    $t6
	# assign  $t6 =>:: $t5
	sb      $t6, 0($t5)

toggle_light_row_greater_if:
	ble     $a0, $0, toggle_light_col_greater_if

	# assign  $t5 = $t3&[($a0 - 1) * $t1 + $a1]
	addi    $t5, $a0, -1
	mul     $t5, $t5, $t1
	add     $t5, $t5, $a1
	add     $t5, $t5, $t3
	# assign  $t6 = (*::($t5) + $a3) % $t2
	lbu     $t6, 0($t5)
	add     $t6, $t6, $a3
	div     $t6, $t2
	mfhi    $t6
	# assign  $t6 =>:: $t5
	sb      $t6, 0($t5)

toggle_light_col_greater_if:
	ble     $a1, $0, toggle_light_row_less_if

	# assign  $t5 = $t3&[($a0) * $t1 + $a1 - 1]
	mul     $t9, $a0, $t1
	add     $t9, $t9, $a1
	addi    $t5, $t9, -1
	add     $t5, $t5, $t3
	# assign  $t6 = (*::($t5) + $a3) % $t2
	lbu     $t6, 0($t5)
	add     $t6, $t6, $a3
	div     $t6, $t2
	mfhi    $t6
	# assign  $t6 =>:: $t5
	sb      $t6, 0($t5)

toggle_light_row_less_if:
	# assign  $t4 = $t0 - 1
	addi    $t4, $t0, -1
	bge     $a0, $t4, toggle_light_col_less_if

	# assign  $t5 = $t3&[($a0 + 1) * $t1 + $a1]
	addi    $t5, $a0, 1
	mul     $t5, $t5, $t1
	add     $t5, $t5, $a1
	add     $t5, $t5, $t3
	# assign  $t6 = (*::($t5) + $a3) % $t2
	lbu     $t6, 0($t5)
	add     $t6, $t6, $a3
	div     $t6, $t2
	mfhi    $t6
	# assign  $t6 =>:: $t5
	sb      $t6, 0($t5)

toggle_light_col_less_if:
	# assign  $t4 = $t1 - 1
	addi    $t4, $t1, -1
	bge     $a1, $t4, toggle_light_end

	# assign  $t5 = $t3&[($a0) * $t1 + $a1 + 1]
	mul     $t5, $a0, $t1
	add     $t5, $t5, $a1
	addi    $t5, $t5, 1
	add     $t5, $t5, $t3
	# assign  $t6 = (*::($t5) + $a3) % $t2
	lbu     $t6, 0($t5)
	add     $t6, $t6, $a3
	div     $t6, $t2
	mfhi    $t6
	# assign  $t6 =>:: $t5
	sb      $t6, 0($t5)

toggle_light_end:
	jr      $ra


# const int MAX_GRIDSIZE = 16;
# struct LightsOut {
#     int num_rows;
#     int num_cols;
#     int num_color;
#     unsigned char board[MAX_GRIDSIZE*MAX_GRIDSIZE];
#     bool clue[MAX_GRIDSIZE*MAX_GRIDSIZE]; //(using bytes in SpimBot)
#     };

# bool solve(LightsOut* puzzle, unsigned char* solution, int row, int col){
#     int num_rows = puzzle->num_rows; 
#     int num_cols = puzzle->num_cols;
#     int num_colors = puzzle->num_colors;
#     int next_row = ((col == num_cols-1) ? row + 1 : row);
#     if (row >= num_rows || col >= num_cols) {
#          return board_done(num_rows,num_cols,puzzle->board);
#     }
#     if (row != 0) {
#         int actions = (num_colors - puzzle->board[(row-1)*num_cols + col]) % num_colors;
#         solution[row*num_cols + col] = actions;
#         toggle_light(row, col, puzzle, actions);
#         if (solve(puzzle,solution, next_row, (col + 1) % num_cols)) {
#             return true;
#         }
#         solution[row*num_cols + col] = 0;
#         toggle_light(row, col, puzzle, num_colors - actions);
#         return false;
#     }
# 
#     for(char actions = 0; actions < num_colors; actions++) {
#         solution[row*num_cols + col] = actions;
#         toggle_light(row, col, puzzle, actions);
#         if (solve(puzzle,solution, next_row, (col + 1) % num_cols)) {
#             return true;
#         }
#         toggle_light(row, col, puzzle, num_colors - actions); 
#         solution[row*num_cols + col] = 0;
#     }
#     return false;
# }
.globl solve
solve:
    ## Stack setup
    ##
    ## Index 4  Variable puzzle
    ## Index 0  Variable ra
	addi    $sp, $sp, -40
	sw      $ra, 0($sp)
	sw      $a0, 4($sp)
	sw      $s0, 8($sp) 
	sw      $s1, 12($sp)
	sw      $s2, 16($sp)
	sw      $s3, 20($sp)
	sw      $s4, 24($sp)
	sw      $s5, 28($sp)
	sw      $s6, 32($sp)
	sw      $s7, 36($sp)
    ##
    ## End stack setup block

    ## Variables corresponding to registers:

    ##
    ##    $t0 = tmp_var
    ##    $s4 = actions
    ##    $s3 = next_row
    ##    $s2 = num_colors
    ##    $s1 = num_cols
    ##    $s0 = num_rows
    ##    $s6 = col
    ##    $s5 = row
    ##    $a3 = col_in
    ##    $a2 = row_in
    ##    $s7 = solution
    ##    $a1 = solution_in
    ##    $a0 = puzzle
    ##
    ## End aliases



    # .stackalloc (4)solution
	# .stackalloc (4)row (4)col


	move    $s7, $a1
	move    $s5, $a2
	move    $s6, $a3

	# assign  $s0   = *0($a0)
	lw      $s0, 0($a0)
	# assign  $s1   = *4($a0)
	lw      $s1, 4($a0)
	# assign  $s2 = *8($a0)
	lw      $s2, 8($a0)


solve_next_row_ternary:
	# assign  $t0 = $s1 - 1
	addi    $t0, $s1, -1
	bne     $s6, $t0, solve_next_row_ternary_else

	# assign  $s3 = $s5 + 1
	addi    $s3, $s5, 1
	j       solve_next_row_ternary_end
solve_next_row_ternary_else:
	# assign  $s3 = $s5
	move    $s3, $s5
solve_next_row_ternary_end:

solve_if_done:
	bge     $s5, $s0, solve_if_done_cond
	bge     $s6, $s1, solve_if_done_cond
	j       solve_if_done_skip
solve_if_done_cond:
	# return board_done(num_rows,num_cols,puzzle->board);
	move    $a0, $s0
	move    $a1, $s1
	# assign  $a2 = *12($a0)
	lw      $a2, 4($sp)
	add     $a2,$a2,12

	jal     solver_board_done

    ## Stack frame teardown block
    ##
	lw      $ra, 0($sp)
	lw      $s0, 8($sp) 
	lw      $s1, 12($sp)
	lw      $s2, 16($sp)
	lw      $s3, 20($sp)
	lw      $s4, 24($sp)
	lw      $s5, 28($sp)
	lw      $s6, 32($sp)
	lw      $s7, 36($sp)
	addi    $sp, $sp, 40
    ##
    ## End stack teardown

	jr      $ra

solve_if_done_skip:
#if (row != 0) {
#         int actions = (num_colors - puzzle->board[(row-1)*num_cols + col]) % num_colors;
#         solution[row*num_cols + col] = actions;
#         toggle_light(row, col, puzzle, actions);
#         if (solve(puzzle,solution, next_row, (col + 1) % num_cols)) {
#             return true;
#         }
#         solution[row*num_cols + col] = 0;
#         toggle_light(row, col, puzzle, num_colors - actions);
#         return false;
    #     }
	beq     $s5, $zero, solve_if_row_not_zero_skip
	sub     $t0, $s5, 1
	mul     $t0, $t0, $s1
	add     $t0, $t0, $s6    # (row-1)*num_cols + col
	lw      $a0, 4($sp)
	add     $a0, $a0, 12
	add     $t2, $t0, $a0   # t0: offset, a0: puzzle->board
	lbu     $t1, 0($t2)     # puzzle->board[(row-1)*num_cols + col]
	sub     $t1, $s2, $t1
	rem     $s4, $t1, $s2   # s4: actions = (num_colors - puzzle->board[(row-1)*num_cols + col]) % num_colors;
	add     $t0, $t0, $s1 
	add     $t0, $t0, $s7
	sb      $s4, 0($t0)     # solution[row*num_cols + col] = actions


	move    $a0, $s5
	move    $a1, $s6
	lw      $a2, 4($sp)
	move    $a3, $s4
	jal     toggle_light    #toggle_light(row, col, puzzle, actions);

	lw      $a0, 4($sp)
	move    $a1, $s7
	move    $a2, $s3
	add     $a3, $s6, 1
	rem     $a3, $a3, $s1
	jal     solve           #solve(puzzle,solution, next_row, (col + 1) % num_cols)

	beq     $v0, 0, solve_if_row_not_zero_solved_skip
    ## Stack frame teardown block
    ##
	lw      $ra, 0($sp)
	lw      $s0, 8($sp) 
	lw      $s1, 12($sp)
	lw      $s2, 16($sp)
	lw      $s3, 20($sp)
	lw      $s4, 24($sp)
	lw      $s5, 28($sp)
	lw      $s6, 32($sp)
	lw      $s7, 36($sp)
	addi    $sp, $sp, 40
    ##
    ## End stack teardown

	jr      $ra

solve_if_row_not_zero_solved_skip:
	mul    $t0, $s5, $s1       
	add     $t0, $t0, $s6
	add     $t0, $t0, $s7
	sb      $zero, 0($t0)         #         solution[row*num_cols + col] = 0;

	lw      $a2, 4($sp)
	move    $a0, $s5
	move    $a1, $s6
	sub     $a3, $s2, $s4
	jal     toggle_light    #toggle_light(row, col, puzzle, num_colors - actions);

	move    $v0, $zero          # return false
    ## Stack frame teardown block
    ##
	lw      $ra, 0($sp)
	lw      $s0, 8($sp) 
	lw      $s1, 12($sp)
	lw      $s2, 16($sp)
	lw      $s3, 20($sp)
	lw      $s4, 24($sp)
	lw      $s5, 28($sp)
	lw      $s6, 32($sp)
	lw      $s7, 36($sp)
	addi    $sp, $sp, 40
    ##
    ## End stack teardown

	jr      $ra
solve_if_row_not_zero_skip:

	# Saving things to the stack
	sw      $a0, 4($sp) # sstk    $puzzle, puzzle

	li      $s4, 0
solve_for_actions:
	bge     $s4, $s2, solve_for_actions_end

	# assign  $s4 =>:: $s7&[$s5 * $s1 + $s6]
	mul     $t9, $s5, $s1
	add     $t9, $t9, $s6
	add     $t9, $t9, $s7
	sb      $s4, 0($t9)

	# toggle_light(row, col, puzzle, actions);
	move    $a0, $s5
	move    $a1, $s6
	lw      $a2, 4($sp) # lstk    $a2, puzzle
	move    $a3, $s4
	jal     toggle_light

    # if (solve(puzzle,solution, next_row, (col + 1) % num_cols)) {
solve_recurse_if:
	lw      $a0, 4($sp) # lstk    $a0, puzzle
	move    $a1, $s7
	move    $a2, $s3
	# assign  $a3 = ($s6 + 1) % $s1
	addi    $a3, $s6, 1
	div     $a3, $s1
	mfhi    $a3
	jal     solve

	beq     $v0, $0, solve_recurse_if_skip

    ## Stack frame teardown block
    ##
	lw      $ra, 0($sp)
	lw      $s0, 8($sp) 
	lw      $s1, 12($sp)
	lw      $s2, 16($sp)
	lw      $s3, 20($sp)
	lw      $s4, 24($sp)
	lw      $s5, 28($sp)
	lw      $s6, 32($sp)
	lw      $s7, 36($sp)
	addi    $sp, $sp, 40
    ##
    ## End stack teardown

	jr      $ra

solve_recurse_if_skip:
	# }

	# toggle_light(row, col, puzzle, num_colors - actions);
	move    $a0, $s5
	move    $a1, $s6
	lw      $a2, 4($sp) # lstk    $a2, puzzle
	# assign  $a3 = $s2 - $s4
	sub     $a3, $s2, $s4
	jal     toggle_light

	# assign  $zero =>:: $s7&[$s5 * $s1 + $s6]
	mul     $t9, $s5, $s1
	add     $t9, $t9, $s6
	add     $t9, $t9, $s7
	sb      $zero, 0($t9)

solve_for_actions_inc:
	add     $s4, $s4, 1
	j       solve_for_actions
solve_for_actions_end:

    # @RETURN $zero
	move    $v0, $zero

    ## Stack frame teardown block
    ##
	lw      $ra, 0($sp)
	lw      $s0, 8($sp) 
	lw      $s1, 12($sp)
	lw      $s2, 16($sp)
	lw      $s3, 20($sp)
	lw      $s4, 24($sp)
	lw      $s5, 28($sp)
	lw      $s6, 32($sp)
	lw      $s7, 36($sp)
	addi    $sp, $sp, 40
    ##
    ## End stack teardown

	jr      $ra


# void zero_board(int num_rows, int num_cols, unsigned char* solution){
#     for (int row = 0; row < num_rows; row++) {
#         for (int col = 0; col < num_cols; col++) {
#             solution[(row)*num_cols + col] = 0;
#         }
#     }
# }
.globl solver_zero_board
solver_zero_board:
    ## Variables corresponding to registers:

    ##
    ##    $t1 = col
    ##    $t0 = row
    ##    $a2 = solution
    ##    $a1 = num_cols
    ##    $a0 = num_rows
    ##
	## End aliases


	li      $t0, 0
solver_zero_board_for_row:
	bge     $t0, $a0, solver_zero_board_for_row_end

	li      $t1, 0
solver_zero_board_for_col:
	bge     $t1, $a1, solver_zero_board_for_col_end

	# assign  $zero =>:: $a2&[$t0 * $a1 + $t1]
	mul     $t9, $t0, $a1
	add     $t9, $t9, $t1
	add     $t9, $t9, $a2
	sb      $zero, 0($t9)

	add     $t1, $t1, 1
	j       solver_zero_board_for_col
solver_zero_board_for_col_end:

	add     $t0, $t0, 1
	j       solver_zero_board_for_row
solver_zero_board_for_row_end:

	jr      $ra


# // it just checks if all lights are off 
# bool board_done(int num_rows, int num_cols,unsigned char* board){ 
#     for (int row = 0; row < num_rows; row++) {
#         for (int col = 0; col < num_cols; col++) {
#             if (board[(row)*num_cols + col] != 0) {
#                 return false;
#             }
#         }
#     }
#     return true;
# }
.globl solver_board_done
solver_board_done:
    ## Variables corresponding to registers:

    ##
    ##    $t2 = condition_val
    ##    $t1 = col
    ##    $t0 = row
    ##    $a2 = board
    ##    $a1 = num_cols
    ##    $a0 = num_rows
    ##
	## End aliases


	li      $t0, 0
solver_board_done_for_row:
	bge     $t0, $a0, solver_board_done_for_row_end

	li      $t1, 0
solver_board_done_for_col:
	bge     $t1, $a1, solver_board_done_for_col_end

	# assign  $t2 = $a2[$t0 * $a1 + $t1]
	mul     $t2, $t0, $a1
	add     $t2, $t2, $t1
	add     $t2, $t2, $a2
	lb     $t2, 0($t2)
solver_board_done_if:
	beq     $t2, $0, solver_board_done_if_skip

	# @RETURN $zero
	move    $v0, $zero
	jr      $ra

solver_board_done_if_skip:

	add     $t1, $t1, 1
	j solver_board_done_for_col
solver_board_done_for_col_end:


	add     $t0, $t0, 1
	j solver_board_done_for_row
solver_board_done_for_row_end:

	# @RETURN 1
	li      $v0, 1
	jr      $ra
