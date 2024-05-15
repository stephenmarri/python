import os

board = [3] * 9
players = ['X', 'O', '-']
turn = 1
is_game_over = False
moves = 0
message = None
win = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def show_board():
    global board, message
    os.system('cls')
    for i in range(0, 9):
        print(players[board[i] - 1], end="\t")
        if (i + 1) % 3 == 0:
            print("\n")
    if message is not None:
        print(message)
        message = None


def seek_input():
    global turn, moves, board, message
    choice = input(f"{players[turn - 1]}'s Turn: ")
    if not (choice.isnumeric() and 0 < int(choice) <= 9):
        message = "Invalid input. Try again"
        return
    if board[int(choice) - 1] != 3:
        message = "Invalid square. Try again"
        return
    board[int(choice) - 1] = turn
    turn = 3 - turn
    moves += 1


def is_game_complete() -> bool:
    player = 3 - turn
    for arr in win:
        check_sum = 0
        for ind in arr:
            if board[ind] == player:
                check_sum += 1
        if check_sum == 3:
            print(f"Winner is: [{players[2 - turn]}] !!!")
            return True
    if moves >= 9:
        return True
    return False


if __name__ == "__main__":
    print("Game Started")
    while True:
        show_board()
        if is_game_complete():
            break
        seek_input()

    print("Game Completed")
