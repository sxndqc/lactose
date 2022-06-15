import numpy as np
from matplotlib import pyplot as plt

good_mortality = 0.7
bad_mortality = 0.4
N = 20
N_Off = 5
INITIAL = 1000

def breed(generation):
    
    new_generation = []

    np.random.shuffle(generation)
    if len(generation) % 2 == 1:
        generation = generation[:-1]
    male = generation[ : len(generation) // 2]
    female = generation[len(generation) // 2 : ]

    # for i in range(N_Off):
    #     babies = uniform_newborn(male + female)
    #     new_generation += list(babies)

    for i in range(len(male)):
        babies = newborn(male[i], female[i])
        for baby in babies:
            if baby >= 0:
                new_generation.append(baby)

    return np.array(new_generation)

def uniform_newborn(couple):

    babies = couple
    print(couple)
    pos = np.where(babies == 1)[0]
    r = np.random.ranf(len(pos))
    r[r < 0.25] = 0
    r[r >= 0.75] = 2
    r[np.logical_and(r >= 0.25, r < 0.75)] = 1
    print(r)
    babies[pos] = r

    r = np.random.ranf(len(babies))
    r[r >= good_mortality] = 0
    r[np.logical_and(r >= bad_mortality, r < good_mortality)] = -1
    r[r < bad_mortality] = -3

    babies -= r

    babies = babies[babies>=0]

    return babies


def newborn(male, female):
    
    if (male, female) == (0,0):
        babies = np.zeros(N_Off)
    elif ((male, female) == (1,0)) or ((male, female) == (0,1)):
        r = np.random.ranf(N_Off)
        r[r<0.5] = 0
        r[r>=0.5] = 1
        babies = r
        #print(babies)
    elif ((male, female) == (2,0)) or ((male, female) == (0,2)):
        babies = np.ones(N_Off)
    elif ((male, female) == (1,2)) or ((male, female) == (2,1)):  
        r = np.random.ranf(N_Off)
        r[r<0.5] = 0
        r[r>=0.5] = 2
        r[r==0] = 1
        babies = r
    elif (male,female) == (2,2):
        babies = np.ones(N_Off) * 2
    elif (male, female) == (1,1):
        r = np.random.ranf(N_Off)
        r[r < 0.25] = 0
        r[r >= 0.75] = 2
        r[np.logical_and(r >= 0.25, r < 0.75)] = 1
        babies = r

    r = np.random.ranf(N_Off)
    for i, baby in enumerate(babies):
        if r[i] >= good_mortality:
            continue
        elif r[i] < bad_mortality:
            babies[i] = -1
        else:
            if baby == 0:
                babies[i] = -1

    return babies

def visualization_hist(matrix):
    g0 = []
    g1 = []
    g2 = []
    gn = []

    X = np.arange(N+1)

    plt.subplot(211)

    for g in matrix:
        g0.append(len(np.where(g==0)[0]))
        g1.append(len(np.where(g==1)[0]))
        g2.append(len(np.where(g==2)[0]))
        gn.append(len(g))
    print(g1)
    plt.bar(X, g0, color = 'blue', label="Homozygous non")
    plt.bar(X, g1, color = 'yellow', bottom = g0, label="Heterozygous")
    plt.bar(X, g2, color = 'red', bottom = g1, label="Homozygous Carrier")

    plt.legend()

    plt.subplot(212)

    plt.plot(X, np.array(g0) / np.array(gn), color = 'blue', label="Non")

    plt.plot(X, (np.array(g2)+np.array(g1))/np.array(gn), color = 'red', label="Carrier")

    plt.legend()

    plt.show()

if __name__ == "__main__":

    G0 = np.zeros(INITIAL)
    G0[0] = 1

    matrix_generation = [G0]

    og = G0

    for i in range(N):
        print(i)
        ng = breed(og)
        matrix_generation.append(ng)
        og = ng

    visualization_hist(matrix_generation)