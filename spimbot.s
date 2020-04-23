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
DEFAULT_VELOCITY	= 10

.data
### Puzzle
puzzle:     .byte 0:268
solution:   .byte 0:256
#### Puzzle

has_puzzle: .word 0

flashlight_space: .word 0

#### Scanner
scanner_wb: .byte 0 0 0 0

.text
main:
    # Construct interrupt mask
	li      $t4, 0
	or      $t4, $t4, BONK_INT_MASK # request bonk
	or      $t4, $t4, REQUEST_PUZZLE_INT_MASK           # puzzle interrupt bit
	or      $t4, $t4, RESPAWN_INT_MASK           # respawn interrupt bit
	or      $t4, $t4, 1 # global enable
	mtc0    $t4, $12

    #Fill in your code here
	li      $t0, 1                          
	sw      $t0, VELOCITY

	li      $t0, 45
	sw      $t0, ANGLE				# Set initial angle to southeast
	li      $t0, 1
	sw      $t0, ANGLE_CONTROL			# absolute

	li      $t1, 500
	li      $t4, 7

main_loop:

	rem     $t5, $t1, $t4                       # The idea here is that we want to limit the times we check_bytecoin and hence scan to happen 1/7 times 
	sub     $t1, $t1, 1
	beq     $t5, $zero, check_bytecoin
	j       main_loop

check_bytecoin:
	lw      $t0, GET_BYTECOINS                  # Anytime we have less than 300 bytecoins, we'll solve puzzles
	li      $t1, 300
	blt     $t0, $t1, prep_puzzle
	j       main_scan

prep_puzzle:
	la      $t0, puzzle
	sw      $t0, REQUEST_PUZZLE

check_response:
	la      $t0, has_puzzle
	lw      $t0, 0($t0)
	beq     $t0, $zero, check_response

	la      $a0, puzzle
	la      $a1, solution
	li      $a2, 0
	li      $a3, 0

	jal     solve

	la      $t0, solution
	sw      $t0, SUBMIT_SOLUTION

	la      $t0, has_puzzle
	sw      $zero, 0($t0)

	j       check_bytecoin

main_scan:
	la      $t2, scanner_wb
	sw      $t2, USE_SCANNER

	lbu     $t2, 2($t2)                         # Loads the identifying byte from the scanner, can be found in docs

	beq     $t2, 2, main_UDP			# If neutral host, prep to fire UDP

	beq     $t2, 10, main_UDP_2			# If enemy host, prep to fire 2 UDP

	beq     $t2, 24, main_UDP			# If enemy player, prep to fire UDP

	beq     $t2, 1, main_rotate			# If wall, rotate

    #beq     $t2, 4, main_rotate			# If friendly host, rotate

	j       main_loop

main_UDP_2:					# Shoot 2 UDP
	li      $t0, 0                              # Slow velocity while shooting
	sw      $t0, VELOCITY

	sw      $zero, SHOOT_UDP_PACKET
	sw      $zero, SHOOT_UDP_PACKET

	li      $t0, DEFAULT_VELOCITY			# Restore velocity
	sw      $t0, VELOCITY
	j       main_loop                           # Restarts loop

main_UDP:
	li      $t0, 0                              # Slow velocity while shooting
	sw      $t0, VELOCITY

	sw      $zero, SHOOT_UDP_PACKET

	li      $t0, DEFAULT_VELOCITY			# Restore velocity
	sw      $t0, VELOCITY
	j       main_loop                           # Restarts loop

main_rotate:
	li      $t0, 5                              # Slow velocity
	sw      $t0, VELOCITY

sub_rotate:
	li      $t0, 3                              # Angle we want to rotate, can be tweaked to help get out of some spots
	sw      $t0, ANGLE
	sw      $zero, ANGLE_CONTROL

	la      $t2, scanner_wb
	sw      $t2, USE_SCANNER

	lbu     $s0, 0($t2)                         # Loads hit_x
	lbu     $s1, 1($t2)                         # Loads hit_y
	lb      $s2, 2($t2)                         # Loads tile_type

	lw	$s3, BOT_X				# distance check for hit tile
	lw	$s4, BOT_Y

	srl	$s3, $s3, 3				# divide by 8 to get tiles
	srl	$s4, $s4, 3				# divide by 8

	sub	$s3, $s3, $s0				# BOT_X -= hit_x
	sub	$s4, $s4, $s1				# BOT_Y -= hit_y

	mul	$s3, $s3, $s3				# (BOT_X - hit_x)^2
	mul	$s4, $s4, $s4				# (BOT_Y - hit_y)^2

	add	$s3, $s3, $s4				# dist squared

	bge	$s3, 25, end_rotate			# rotate if more than 5 tiles away

	beq     $s2, 1, sub_rotate

end_rotate:
	li      $t0, DEFAULT_VELOCITY
	sw      $t0, VELOCITY				# Restore velocity

	j       main_loop

main_finish:
	jr      $ra

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

	and     $a0, $k0, BONK_INT_MASK     # is there a bonk interrupt?
	bne     $a0, 0, bonk_interrupt

	and     $a0, $k0, TIMER_INT_MASK    # is there a timer interrupt?
	bne     $a0, 0, timer_interrupt

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

timer_interrupt:
	sw      $0, TIMER_ACK
    #Fill in your timer interrupt code here
	j        interrupt_dispatch     # see if other interrupts are waiting

request_puzzle_interrupt:
	sw      $0, REQUEST_PUZZLE_ACK

	la      $t0, has_puzzle
	li      $t1, 1
	sw      $t1, 0($t0)

	j       interrupt_dispatch

respawn_interrupt:
	sw      $0, RESPAWN_ACK

	li      $t0, DEFAULT_VELOCITY
	sw      $t0, VELOCITY($zero)

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
