Desired scenario: given the location of the bot after the respawn, convert
the location to an index in an array of 16 pointers, which point to the
correct instruction to restart at.

First, divide `BOT_X`, `BOT_Y` (which are in pixels) by 8 to get tile
coordinates.

This is the mapping scheme:

	index bits: ABCD
	A = x < 16
	B = y < 16
	C = A ? (x * 2 < 16) : (x // 2 < 16)
	D = B ? (y * 2 < 16) : (y // 2 < 16)

Having a 1-to-1 function means minimal memory usage and no wasted space on
unused pointers in the array.

Host locations:

	# Top-left
	5 13
	7 7
	13 5
	14 14

	# Top-right
	26 2
	27 12
	37 13
	33 6

	# Bottom-right
	25 25
	26 34
	32 32
	34 26

	# Bottom-left
	2 26
	6 33
	12 27
	13 37
