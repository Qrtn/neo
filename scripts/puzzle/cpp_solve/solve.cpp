#include <iostream>

#include "lightsout.h"

int main() {
    lightsout::LightsOut puzzle;
    unsigned char solution[lightsout::MAX_GRIDSIZE * lightsout::MAX_GRIDSIZE];

    std::cin >> puzzle.num_rows >> puzzle.num_cols >> puzzle.num_colors;

    for (int i = 0; i < puzzle.num_rows; ++i) {
        for (int j = 0; j < puzzle.num_cols; ++j) {
            int state;

            std::cin >> state;
            puzzle.board[i * puzzle.num_cols + j] = static_cast<unsigned char>(state);
        }
    }

    std::fill(std::begin(puzzle.clue), std::end(puzzle.clue), false);

    bool solvable = lightsout::solve(&puzzle, solution, 0, 0);

    if (!solvable) {
        std::cerr << "No solution found" << std::endl;
        return -1;
    }

    for (int i = 0; i < puzzle.num_rows; ++i) {
        for (int j = 0; j < puzzle.num_cols; ++j) {
            int presses = static_cast<int>(solution[i * puzzle.num_cols + j]);

            std::cout << presses << " ";
        }
        std::cout << std::endl;
    }

    std::cout << std::endl;

    return 0;
}
