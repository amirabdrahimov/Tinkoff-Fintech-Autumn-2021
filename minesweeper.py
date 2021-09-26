import random
import pickle
import os


def print_board(slots, board_size):
    st = "   "
    for i in range(board_size):
        st = st + "     " + str(i + 1)
    print(st)

    for row in range(board_size):
        st = "     "
        if row == 0:
            for col in range(board_size):
                st = st + "______"
            print(st)

        st = "     "
        for col in range(board_size):
            st = st + "|     "
        print(st + "|")

        st = "  " + str(row + 1) + "  "
        for col in range(board_size):
            st = st + "|  " + str(slots[row][col]) + "  "
        print(st + "|")

        st = "     "
        for col in range(board_size):
            st = st + "|_____"
        print(st + '|')
    print()


def set_mines(board, num_of_mines, board_size):
    count = 0
    while count < num_of_mines:
        value = random.randint(0, board_size * board_size - 1)

        row = value // board_size
        col = value % board_size

        if board[row][col] != -1:
            count = count + 1
            board[row][col] = -1


def set_values(board, board_size):
    # Function that counts value of cell

    for r in range(board_size):
        for col in range(board_size):

            # Skip, if it contains a mine
            if board[r][col] == -1:
                continue

            if r > 0 and board[r - 1][col] == -1:
                board[r][col] = board[r][col] + 1
            # Check down
            if r < board_size - 1 and board[r + 1][col] == -1:
                board[r][col] = board[r][col] + 1
            # Check left
            if col > 0 and board[r][col - 1] == -1:
                board[r][col] = board[r][col] + 1
            # Check right
            if col < board_size - 1 and board[r][col + 1] == -1:
                board[r][col] = board[r][col] + 1
            # Check top-left
            if r > 0 and col > 0 and board[r - 1][col - 1] == -1:
                board[r][col] = board[r][col] + 1
            # Check top-right
            if r > 0 and col < board_size - 1 and board[r - 1][col + 1] == -1:
                board[r][col] = board[r][col] + 1
            # Check below-left
            if r < board_size - 1 and col > 0 and board[r + 1][col - 1] == -1:
                board[r][col] = board[r][col] + 1
            # Check below-right
            if r < board_size - 1 and col < board_size - 1 and board[r + 1][col + 1] == -1:
                board[r][col] = board[r][col] + 1


def neighbours(row, col, slots, board, board_size, opened):
    if [row, col] not in opened:
        opened.append([row, col])

        if board[row][col] == 0:

            slots[row][col] = board[row][col]

            if row > 0:
                neighbours(row - 1, col, slots, board, board_size, opened)
            if row < board_size - 1:
                neighbours(row + 1, col, slots, board, board_size, opened)
            if col > 0:
                neighbours(row, col - 1, slots, board, board_size, opened)
            if col < board_size - 1:
                neighbours(row, col + 1, slots, board, board_size, opened)
            if row > 0 and col > 0:
                neighbours(row - 1, col - 1, slots, board, board_size, opened)
            if row > 0 and col < board_size - 1:
                neighbours(row - 1, col + 1, slots, board, board_size, opened)
            if row < board_size - 1 and col > 0:
                neighbours(row + 1, col - 1, slots, board, board_size, opened)
            if row < board_size - 1 and col < board_size - 1:
                neighbours(row + 1, col + 1, slots, board, board_size, opened)

        if board[row][col] != 0:
            slots[row][col] = board[row][col]


def check_game_over(slots, board_size, num_of_mines):
    count = 0
    # Loop for checking each cell in the grid
    for r in range(board_size):
        for col in range(board_size):

            if slots[r][col] != ' ' and slots[r][col] != 'F':
                count = count + 1

    if count == board_size * board_size - num_of_mines:
        return True
    else:
        return False


# Show all mines at the end of the game
def show_mines(slots, board, board_size):
    for r in range(board_size):
        for col in range(board_size):
            if board[r][col] == -1:
                slots[r][col] = 'M'


def show_instruction():
    print("Instructions:")
    print("1. Enter column and row number to dig a cell, Example \"2 3\"")
    print("2. In order to put or remove a flag, enter F after column and row, Example \"2 3 f\"")
    print("3. If you decide to leave during the game, you can save your progress by writing \"s\"")
    print("4. Write \"q\" in order to quit")


def generate_new_game(board_size, num_of_mines):
    board = [[0 for y in range(board_size)] for x in range(board_size)]
    slots = [[' ' for y in range(board_size)] for x in range(board_size)]

    set_mines(board, num_of_mines, board_size)
    set_values(board, board_size)
    return board, slots


def play(board, slots, opened, flags, num_of_mines, board_size):
    show_instruction()

    game_over = False

    # Game loop
    while not game_over:
        print_board(slots, board_size)

        user_input = input("Enter column and row number: ").split()

        if (user_input[0]) == "q":
            quit()

        if user_input[0] == "s":
            file = open('save.p', 'wb')
            pickle.dump(board, file)
            pickle.dump(slots, file)
            pickle.dump(opened, file)
            pickle.dump(flags, file)
            pickle.dump(num_of_mines, file)
            file.close()
            print("Game saved\n")

        if len(user_input) == 2:
            try:
                value = list(map(int, user_input))
            except ValueError:
                print("Wrong input!")
                show_instruction()
                continue

        elif len(user_input) == 3:
            if user_input[2] != 'F' and user_input[2] != 'f':
                print("Wrong Input!")
                show_instruction()
                continue

            try:
                value = list(map(int, user_input[:2]))
            except ValueError:
                print("Wrong input!")
                show_instruction()
                continue

            if value[0] > board_size or value[0] < 1 or value[1] > board_size or value[1] < 1:
                print("Wrong input!")
                show_instruction()
                continue

            col = value[0] - 1
            row = value[1] - 1

            if [row, col] in flags:
                print("Removing flag")
                flags.remove([row, col])
                slots[row][col] = ' '
                continue

            # Check the number of flags
            if len(flags) < num_of_mines:
                flags.append([row, col])
                slots[row][col] = 'F'
                print("Flag set")
                continue
            else:
                print("All flags set")
                continue

        else:
            print("Wrong input!")
            show_instruction()
            continue

        # Check if the input fit size of board
        if value[0] > board_size or value[0] < 1 or value[1] > board_size or value[1] < 1:
            print("Wrong Input!")
            show_instruction()
            continue

        col = value[0] - 1
        row = value[1] - 1

        if board[row][col] == -1:
            slots[row][col] = 'M'
            show_mines(slots, board, board_size)
            print_board(slots, board_size)
            print("Step on a mine!")
            print(
                "\n"
                "┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼\n"
                "███▀▀▀██┼███▀▀▀███┼███▀█▄█▀███┼██▀▀▀\n"
                "██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼█┼┼┼██┼██┼┼┼\n"
                "██┼┼┼▄▄▄┼██▄▄▄▄▄██┼██┼┼┼▀┼┼┼██┼██▀▀▀\n"
                "██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██┼┼┼\n"
                "███▄▄▄██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██▄▄▄\n"
                "┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼\n"
                "███▀▀▀███┼▀███┼┼██▀┼██▀▀▀┼██▀▀▀▀██▄┼\n"
                "██┼┼┼┼┼██┼┼┼██┼┼██┼┼██┼┼┼┼██┼┼┼┼┼██┼\n"
                "██┼┼┼┼┼██┼┼┼██┼┼██┼┼██▀▀▀┼██▄▄▄▄▄▀▀┼\n"
                "██┼┼┼┼┼██┼┼┼██┼┼█▀┼┼██┼┼┼┼██┼┼┼┼┼██┼\n"
                "███▄▄▄███┼┼┼─▀█▀┼┼─┼██▄▄▄┼██┼┼┼┼┼██▄\n"
                "┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼\n")
            game_over = True
            continue

        elif board[row][col] == 0:
            # opened = []
            slots[row][col] = '0'
            neighbours(row, col, slots, board, board_size, opened)

        else:
            slots[row][col] = board[row][col]

        # Check if all cells are open
        if check_game_over(slots, board_size, num_of_mines):
            show_mines(slots, board, board_size)
            print_board(slots, board_size)
            print("Congratulations!!! YOU WIN")
            game_over = True
            continue


def choose_game_mode():
    while True:
        try:
            user_input = int(input("\nMINESWEEPER\nMAIN MENU\n1 - Standard game 5x5\n2 - Custom game\n3 - Load game\n"
                                   "4 - Quit\nSelect the game mode: "))
            # Standard game 5x5
            if user_input == 1:
                board_size = 5
                num_of_mines = random.randint(2, 5)
                board, slots = generate_new_game(board_size, num_of_mines)
                flags = []
                opened = []
                play(board, slots, opened, flags, num_of_mines, board_size)

            # Custom game
            elif user_input == 2:
                board_size = int(input("Print size of board: "))
                num_of_mines = int(input("Print number of mines: "))
                board, slots = generate_new_game(board_size, num_of_mines)
                flags = []
                opened = []
                play(board, slots, opened, flags, num_of_mines, board_size)

            # Loaded game
            elif user_input == 3:
                if os.path.isfile('./save.p'):
                    file = open('save.p', 'rb')
                    board = pickle.load(file)
                    slots = pickle.load(file)
                    opened = pickle.load(file)
                    flags = pickle.load(file)
                    num_of_mines = pickle.load(file)
                    board_size = len(board)

                    play(board, slots, opened, flags, num_of_mines, board_size)
                else:
                    print("There is no any savings")
                    quit(1)
            elif user_input == 4:
                quit()

        except ValueError:
            print("\nProvide an integer value!")
            continue


if __name__ == "__main__":
    choose_game_mode()
