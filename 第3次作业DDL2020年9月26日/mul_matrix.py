import numpy as np

M = np.array(
    [[0, (1) / (2), 0, (1) / (2)], [(1) / (3), 0, 0, (1) / (2)], [(1) / (3), (1) / (2), 0, 0], [(1) / (3), 0, 1, 0]])
res = np.array([[(1) / (4)], [(1) / (4)], [(1) / (4)], [(1) / (4)]])

i = 10

while (i > 0):
    res = np.dot(M, res)
    i -= 1
    print('fin_res: %s' % (res))

print('fin_res: %s' % (res))
