import math
import tkinter as tk
from functools import partial, update_wrapper
from random import random
from tkinter import font
from shape_type import ShapeType
from shape import Shape
from anytree import Node, RenderTree, AnyNode
import copy


def draw_board(alpha_pruning):
    board_frame = tk.Frame(frame, bg='black')
    board_frame.pack()
    for row in range(6):
        board_row = []

        for col in range(7):
            shape = Shape(board_frame)
            shape.grid(row=row, column=col)
            partial_fun = partial(play, col, board,alpha_pruning)
            shape.bind("<Button-1>", partial_fun)
            board_row.append(shape)
        board.append(board_row)
    # test()


def play(col, board,alpha_pruning, event):
    if board[0][col].get_type() != ShapeType.EMPTY:
        return
    insert_disc(0, col, ShapeType.RED, board)
    mini_max(alpha_pruning)


def insert_disc(row, col, type, board):
    print(board[0][col].get_type())
    if row > 0:
        board[row - 1][col].set_type(ShapeType.EMPTY)
    if board[row][col].get_type() != ShapeType.EMPTY:
        return
    shape = board[row][col]
    shape.set_type(type)
    if row == 5 or board[row + 1][col].get_type() != ShapeType.EMPTY:
        return
    insert_disc(row + 1, col, type, board)
    # partial_fun = partial(insert_disc, row + 1, col, type, board)
    # update_wrapper(partial_fun, insert_disc)
    # root.after(10, partial_fun)


def show_home_page():
    text_font = tk.font.Font(size=30, )
    tk.Label(frame, text='Welcome to Connect-4 Game!', font=text_font, width=200, height=5, bg='black',
             fg='white').pack()
    tk.Button(frame, text='play with alpha pruning', width=22, height=2,
              font=text_font,

              bg='#0052cc', fg='#ffffff', command=play_with_alpha_pruning).pack(
        pady=50)
    tk.Button(frame, text='play without alpha pruning', width=22, height=2,
              font=text_font,
              bg='#0052cc', fg='#ffffff', command=play_without_alpha_pruning).pack()


def play_with_alpha_pruning():
    clear_frame()
    draw_board(True)


def play_without_alpha_pruning():
    clear_frame()
    draw_board(False)


def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()


def insert(board, col, type):
    if board[0][col].get_type() != ShapeType.EMPTY:
        return
    for i in range(6):
        if i == 5:
            board[i][col].set_type(type)
            return
        if board[i + 1][col].get_type() != ShapeType.EMPTY:
            board[i][col].set_type(type)
            return



def build_mini_max_tree(board_copy, cur_player, k, parent, computer_color):
    if k == 0:
        return
    children = []
    next_player = ShapeType.RED
    if cur_player == ShapeType.RED:
        next_player = ShapeType.YELLOW
    for col in range(7):
        if board_copy[0][col].get_type() == ShapeType.EMPTY:
            insert(board_copy, col, cur_player)
            score = calculate_heuristic(board_copy, computer_color)
            node = AnyNode(score=score, parent=parent, index=col)
            children.append(node)
            build_mini_max_tree(board_copy, next_player, k - 1, node, computer_color)
            for i in range(6):
                if board_copy[i][col].get_type() != ShapeType.EMPTY:
                    board_copy[i][col].set_type(ShapeType.EMPTY)
                    break
    parent.children = children


def mini_maxing(node, is_max):
    if len(node.children) == 0:
        return
    score = math.inf
    next_max = True
    if is_max:
        score = 0
        next_max = False

    for child in node.children:
        mini_maxing(child, next_max)
        if is_max:
            score = max(score, child.score)
        else:
            score = min(score, child.score)

    node.score = score

def mini_maxing_alpha_pruning(node):
    if len(node.children) == 0:
        return 0
    node.score = max_value(node,-math.inf,math.inf)


def mini_max(alpha_pruning):
    # for i in range(6):
    #     for j in range(7):
    #         board[i][j].set_type(ShapeType.RED)

    board_copy = []
    f = tk.Frame()
    for i in range(len(board)):
        row_copy = []
        for j in range(len(board[i])):
            shape = Shape(f)
            shape.set_type(board[i][j].get_type())
            row_copy.append(shape)
        board_copy.append(row_copy)
    # board[0][6].set_type(ShapeType.EMPTY)

    # board[0][6].set_type(ShapeType.EMPTY)
    is_max = True
    max_score = 0
    min_score = math.inf
    cur_player = ShapeType.YELLOW
    root = AnyNode(score="root", index=-1)
    build_mini_max_tree(board_copy, cur_player, 1
                        , root, ShapeType.YELLOW)
    if alpha_pruning:
        mini_maxing_alpha_pruning(root)
    else:
        mini_maxing(root, True)
    print(root.score)
    for child in root.children:
        if child.score == root.score:
            insert_disc(0, child.index, ShapeType.YELLOW, board)
            break
    # print(root.children)
    # print(root.leaves)
    # for pre, fill, node in RenderTree(root):
    #     print("%s%s" % (pre, node.score))

    # print(root.score)


def min_value(state, alpha, beta):
    if len(state.children) == 0:
        return state.score
    v = math.inf
    for child in state.children:
        v = min(v, max_value(child, alpha, beta))
        if v <= beta:
            return v
        beta = min(beta, v)
    return v


def max_value(state, alpha, beta):
    if len(state.children) == 0:
        return state.score
    v = -math.inf
    for child in state.children:
        v = max(v, min_value(child, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def calculate_heuristic(board, type):
    score = 0
    prev_rows_type = [[None] * 7 for i in range(3)]
    prev_rows_count = [[0] * 7 for i in range(3)]

    for row in range(7):
        prev_cols_type = [None for i in range(3)]
        prev_cols_count = [0 for i in range(3)]
        if row < 6:
            prev_cols_type[2] = board[row][0].get_type()
        prev_cols_count[2] = 1
        for col in range(8):
            if row == 0 and col < 7:
                prev_rows_type[2][col] = board[0][col].get_type()
                prev_rows_count[2][col] = 1
            if row == 6 and col == 7:
                break
            cur_type = None
            if col < 7 and row < 6:
                cur_type = board[row][col].get_type()
            if col > 0 and row < 6:
                if col == 7 or not (prev_cols_type[2] == cur_type and cur_type == type):
                    if prev_cols_count[2] >= 4:
                        score = score + prev_cols_count[2] - 3
                    if cur_type == ShapeType.EMPTY and prev_cols_count[2] >= 3:
                        score = score + 0.1
                    if prev_cols_type[1] == ShapeType.EMPTY and prev_cols_count[2] >= 3:
                        score = score + 0.1
                    if prev_cols_count[1] == 1 and prev_cols_type[2] == type and prev_cols_type[0] == type and \
                            prev_cols_type[1] == ShapeType.EMPTY and prev_cols_count[2] + prev_cols_count[0] >= 3:
                        if prev_cols_count[2] > 1:
                            score = score + 0.1
                        if prev_cols_count[0] > 1:
                            score = score + 0.1
                    prev_cols_count[0] = prev_cols_count[1]
                    prev_cols_count[1] = prev_cols_count[2]
                    prev_cols_count[2] = 1
                    prev_cols_type[0] = prev_cols_type[1]
                    prev_cols_type[1] = prev_cols_type[2]
                    prev_cols_type[2] = cur_type
                    if col == 7:
                        break
                else:
                    prev_cols_count[2] = prev_cols_count[2] + 1
            if row > 0:
                if row == 6 or not (cur_type == prev_rows_type[2][col] and cur_type == type):
                    if prev_rows_count[2][col] >= 4:
                        score = score + prev_rows_count[2][col] - 3
                    if cur_type == ShapeType.EMPTY and prev_rows_count[2][col] >= 3:
                        score = score + 0.1
                    if prev_rows_type[1][col] == ShapeType.EMPTY and prev_rows_count[2][col] >= 3:
                        score = score + 0.1
                    if prev_rows_count[1][col] == 1 and prev_rows_type[2][col] == type and prev_rows_type[0][
                        col] == type and \
                            prev_rows_type[1][col] == ShapeType.EMPTY and prev_rows_count[2][col] + prev_rows_count[0][
                        col] >= 3:
                        if prev_rows_count[2][col] > 1:
                            score = score + 0.1
                        if prev_rows_count[0][col] > 1:
                            score = score + 0.1
                    prev_rows_count[0][col] = prev_rows_count[1][col]
                    prev_rows_count[1][col] = prev_rows_count[2][col]
                    prev_rows_count[2][col] = 1
                    prev_rows_type[0][col] = prev_rows_type[1][col]
                    prev_rows_type[1][col] = prev_rows_type[2][col]
                    prev_rows_type[2][col] = cur_type
                else:
                    prev_rows_count[2][col] = prev_rows_count[2][col] + 1

    prev_type = [None for i in range(3)]
    prev_count = [1 for i in range(3)]
    row = 6
    col = 7
    for i in range(col):
        x = 0
        y = i
        prev_type[2] = board[x][y].get_type()
        x = x + 1
        y = y + 1

        while x < row and y < col + 1:
            cur_type = None
            if y < col:
                cur_type = board[x][y].get_type()
            if y == col or not (cur_type == prev_type[2] and cur_type == type):
                if prev_count[2] >= 4:
                    score = score + prev_count[2] - 3
                if cur_type == ShapeType.EMPTY and prev_count[2] >= 3:
                    score = score + 0.1
                if prev_type[1] == ShapeType.EMPTY and prev_count[2] >= 3:
                    score = score + 0.1
                if prev_count[1] == 1 and prev_type[2] == type and prev_type[0] == type and \
                        prev_type[1] == ShapeType.EMPTY and prev_count[2] + prev_count[0] >= 3:
                    if prev_count[2] > 1:
                        score = score + 0.1
                    if prev_count[0] > 1:
                        score = score + 0.1
                prev_type[0] = prev_type[1]
                prev_type[1] = prev_type[2]
                prev_type[2] = cur_type
                prev_count[0] = prev_count[1]
                prev_count[1] = prev_count[2]
                prev_count[2] = 1
            else:
                prev_count[2] = prev_count[2] + 1
            x = x + 1
            y = y + 1

    prev_type = [None for i in range(3)]
    prev_count = [1 for i in range(3)]
    row = 6
    col = 7
    for i in range(1, row + 1):
        x = i
        y = 0
        if i < row:
            prev_type[2] = board[x][y].get_type()
        x = x + 1
        y = y + 1

        while x < row + 1 and y < col:
            cur_type = None
            if x < row:
                cur_type = board[x][y].get_type()
            if x == row or not (cur_type == prev_type[2] and cur_type == type):
                if prev_count[2] >= 4:
                    score = score + prev_count[2] - 3
                if cur_type == ShapeType.EMPTY and prev_count[2] >= 3:
                    score = score + 0.1
                if prev_type[1] == ShapeType.EMPTY and prev_count[2] >= 3:
                    score = score + 0.1
                if prev_count[1] == 1 and prev_type[2] == type and prev_type[0] == type and \
                        prev_type[1] == ShapeType.EMPTY and prev_count[2] + prev_count[0] >= 3:
                    if prev_count[2] > 1:
                        score = score + 0.1
                    if prev_count[0] > 1:
                        score = score + 0.1
                prev_type[0] = prev_type[1]
                prev_type[1] = prev_type[2]
                prev_type[2] = cur_type
                prev_count[0] = prev_count[1]
                prev_count[1] = prev_count[2]
                prev_count[2] = 1
            else:
                prev_count[2] = prev_count[2] + 1
            x = x + 1
            y = y + 1

    prev_type = [None for i in range(3)]
    prev_count = [1 for i in range(3)]

    for line in range(1, (row + col)):
        start_col = max(0, line - row)
        count = min(line, (col - start_col), row)
        for j in range(0, count + 1):
            r = min(row, line) - j - 1
            c = start_col + j
            cur_type = None
            if j < count:
                cur_type = board[r][c].get_type()
            if c == 0 and j < count:
                prev_type[2] = cur_type
                continue
            if j == count or not (cur_type == prev_type[2] and cur_type == type):
                if prev_count[2] >= 4:
                    score = score + prev_count[2] - 3
                if cur_type == ShapeType.EMPTY and prev_count[2] >= 3:
                    score = score + 0.1
                if prev_type[1] == ShapeType.EMPTY and prev_count[2] >= 3:
                    score = score + 0.1
                if prev_count[1] == 1 and prev_type[2] == type and prev_type[0] == type and \
                        prev_type[1] == ShapeType.EMPTY and prev_count[2] + prev_count[0] >= 3:
                    if prev_count[2] > 1:
                        score = score + 0.1
                    if prev_count[0] > 1:
                        score = score + 0.1
                prev_type[0] = prev_type[1]
                prev_type[1] = prev_type[2]
                prev_type[2] = cur_type
                prev_count[0] = prev_count[1]
                prev_count[1] = prev_count[2]
                prev_count[2] = 1
            else:
                prev_count[2] = prev_count[2] + 1
    return score


def test():
    # board[0][0].set_type(ShapeType.RED)
    # board[1][1].set_type(ShapeType.RED)
    # board[2][2].set_type(ShapeType.RED)
    # board[3][3].set_type(ShapeType.RED)
    # board[4][2].set_type(ShapeType.RED)
    # board[5][1].set_type(ShapeType.RED)
    # board[0][0].set_type(ShapeType.RED)
    # board[0][1].set_type(ShapeType.RED)
    # board[1][2].set_type(ShapeType.RED)
    # board[0][3].set_type(ShapeType.RED)
    # board[1][0].set_type(ShapeType.RED)
    # board[2][0].set_type(ShapeType.RED)
    # board[3][0].set_type(ShapeType.RED)
    print(calculate_heuristic(board, ShapeType.RED))


root = tk.Tk()
root.attributes("-fullscreen", True)
root.title = "connect-4"
root.configure(bg='black')
root.geometry('700x700')
frame = tk.Frame(root, bg='black')
frame.pack(expand=True)
board = []

show_home_page()
root.mainloop()
