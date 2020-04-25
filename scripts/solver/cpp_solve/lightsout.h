namespace lightsout {
    const int MAX_GRIDSIZE = 16;

    struct LightsOut {
        int num_rows;
        int num_cols;
        int num_colors;
        unsigned char board[MAX_GRIDSIZE*MAX_GRIDSIZE];
        bool clue[MAX_GRIDSIZE*MAX_GRIDSIZE]; //(using bytes in SpimBot)
    };

    bool solve(LightsOut* puzzle, unsigned char* solution, int row, int col);
}
