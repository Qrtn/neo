#include "lightsout.h"

namespace lightsout {
    void toggle_light(int row, int col, LightsOut* puzzle, int action_num){
        int num_rows = puzzle->num_rows;
        int num_cols = puzzle->num_cols;
        int num_colors = puzzle->num_colors;
        unsigned char* board = (puzzle-> board);
        board[row*num_cols + col] = (board[row*num_cols + col] + action_num) % num_colors;
        if (row > 0){
            board[(row-1)*num_cols + col] = (board[(row-1)*num_cols + col] + action_num) % num_colors;
        }
        if (col > 0){
            board[(row)*num_cols + col-1] = (board[(row)*num_cols + col-1] + action_num) % num_colors;
        }
        
        if (row < num_rows - 1){
            board[(row+1)*num_cols + col] = (board[(row+1)*num_cols + col] + action_num) % num_colors;
        }

        if (col < num_cols - 1){
            board[(row)*num_cols + col+1] = (board[(row)*num_cols + col+1] + action_num) % num_colors;
        }
    }

    void zero_board(int num_rows, int num_cols, unsigned char* solution){
        for (int row = 0; row < num_rows; row++) {
            for (int col = 0; col < num_cols; col++) {
                solution[(row)*num_cols + col] = 0;
            }
        }
    }

    // it just checks if all lights are off 
    bool board_done(int num_rows, int num_cols,unsigned char* board){ 
        for (int row = 0; row < num_rows; row++) {
            for (int col = 0; col < num_cols; col++) {
                if (board[(row)*num_cols + col] != 0) {
                    return false;
                }
            }
        }
        return true;
    }

    bool solve(LightsOut* puzzle, unsigned char* solution, int row, int col){
        int num_rows = puzzle->num_rows; 
        int num_cols = puzzle->num_cols;
        int num_colors = puzzle->num_colors;
        int next_row = ((col == num_cols-1) ? row + 1 : row);
        if (row >= num_rows || col >= num_cols) {
             return board_done(num_rows,num_cols,puzzle->board);
        }
        if (row != 0) {
            int actions = (num_colors - puzzle->board[(row-1)*num_cols + col]) % num_colors;
            solution[row*num_cols + col] = actions;
            toggle_light(row, col, puzzle, actions);
            if (solve(puzzle,solution, next_row, (col + 1) % num_cols)) {
                return true;
            }
            solution[row*num_cols + col] = 0;
            toggle_light(row, col, puzzle, num_colors - actions);
            return false;
        }

        for(char actions = 0; actions < num_colors; actions++) {
            solution[row*num_cols + col] = actions;
            toggle_light(row, col, puzzle, actions);
            if (solve(puzzle,solution, next_row, (col + 1) % num_cols)) {
                return true;
            }
            toggle_light(row, col, puzzle, num_colors - actions); 
            solution[row*num_cols + col] = 0;
        }
        return false;
    }
}
