
import random

for i in range(1, 11):
    points = [(random.randint(0, 800), random.randint(0, 500)) for _ in range(100)]
    with open(f'points_set_{i}.txt', 'w') as f:
        for point in points:
            f.write(f"{point[0]} {point[1]}\n")

for i in range(1, 11):
    x = random.randint(10**99, 10**100)
    y = random.randint(10**99, 10**100)
    with open(f'integers_set_{i}.txt', 'w') as f:
        f.write(f"{x} {y}\n")
