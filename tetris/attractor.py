attractor_step: int = 0

steps: list[str] = []

spawn_instructions: list[str] = []

var_defaults: list = [0]

# Converts the instructions file to a list
with open("attractor_steps.txt") as file:
    steps = file.readlines()
    lines_to_delete: list[int] = []
    # Removes any 'comments' in the instructions file
    # Also removes all newline characters
    for i in range(len(steps)):
        if '#' in steps[i]:
            lines_to_delete.append(i)
        steps[i] = steps[i][0]
    
    lines_to_delete.reverse()
    for line in lines_to_delete:
        steps.pop(line)

    # Seperates out any commands to spawn pieces
    for i in range(len(steps)):
        if steps[i] in ['1', '2', '3', '4', '5', '6', '7']:
            #lines_to_delete.append(i)
            spawn_instructions.append(steps[i])

    spawn_instructions.reverse()

print(f"steps: {steps}")

def reset():
    global attractor_step
    attractor_step = var_defaults[0]
    pass

def setup_piece_sequence(piece_sequence: list[int]):
    
    for piece in spawn_instructions:
        piece_sequence.insert(0, int(piece))
    
    return piece_sequence

def return_attractor_input():
    global attractor_step

    cur_step = steps[attractor_step]
    attractor_step += 1

    if attractor_step >= len(steps):
        attractor_step -= len(steps)
    
    return cur_step


