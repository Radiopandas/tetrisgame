attractor_step: int = 0

steps: list[str] = []

with open("attractor_steps.txt") as file:
    steps = file.readlines()
    lines_to_delete: list[int] = []
    for i in range(len(steps)):
        if '#' in steps[i]:
            lines_to_delete.append(i)
        steps[i] = steps[i][0]
    
    lines_to_delete.reverse()
    for line in lines_to_delete:
        steps.pop(line)

print(f"steps: {steps}")

a = 1


def return_attractor_input():
    global attractor_step

    cur_step = steps[attractor_step]
    attractor_step += 1

    if attractor_step >= len(steps):
        attractor_step -= len(steps)
    
    return cur_step


