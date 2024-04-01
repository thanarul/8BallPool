import Physics
import math 
import random

def init_table():
    db = Physics.Database(reset=True)
    db.createDB()

    table = Physics.Table()

    spacing = 4.0  
    offset_x = Physics.TABLE_WIDTH / 2.0
    offset_y = Physics.TABLE_LENGTH / 4.0

    ball_id = 1
    for row in range(1, 6):
        for pos_in_row in range(row):
            x = (
                offset_x
                - (row - 1) * (Physics.BALL_DIAMETER + spacing) / 2
                + pos_in_row * (Physics.BALL_DIAMETER + spacing)
            )
            y = (
                offset_y
                - (row - 1) * (Physics.BALL_DIAMETER + spacing) * math.sqrt(3) / 2
            )

            if row == 3 and pos_in_row == 1:
                current_ball_id = 8
            else:
                current_ball_id = ball_id
                ball_id += 1
                if ball_id == 8:  
                    ball_id += 1

            pos = Physics.Coordinate(x, y)
            sb = Physics.StillBall(current_ball_id, pos)
            table += sb

    cue_ball_pos = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0,
        Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 4.0,
    )
    sb = Physics.StillBall(0, cue_ball_pos)
    table += sb
    table.cueBall()

    db.writeTable(table)

    return table
