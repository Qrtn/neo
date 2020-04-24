Desired scenario: given the location of the bot after the respawn, convert
the location to an index in an array of 16 pointers, which point to the
correct instruction to restart at.

First, divide `BOT_X`, `BOT_Y` (which are in pixels) by 8 to get tile
coordinates.

This is the mapping scheme:

	index bits: ABCD
	A = x >= 16
	B = y >= 16
	C = A ? (x * 2 >= 16) : (x // 2 >= 16)
	D = B ? (y * 2 >= 16) : (y // 2 >= 16)

Having a 1-to-1 function means minimal memory usage and no wasted space on
unused pointers in the array.

Implemented as:

	C = A ? (x >= 32) : (x >= 8)
	D = B ? (y >= 32) : (y >= 8)

Host locations:

	# Top-left
	7 7		0
	5 13		1
	13 5		2
	14 14		3

	# Bottom-left
	2 26		4
	6 33		5
	12 27		6
	13 37		7

	# Top-right
	26 2		8
	27 12		9
	33 6		10
	37 13		11

	# Bottom-right
	25 25		12
	26 34		13
	34 26		14
	32 32		15
