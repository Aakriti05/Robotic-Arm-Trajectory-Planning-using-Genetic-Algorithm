import numpy as np
import scipy.interpolate as sc
import matplotlib.pyplot as plt

'''
generate_trajectories(population, start, end) : 
    population - matrix of (interlaced x and y coordinates of internal points) of each chromosome of the population. 
                 Each row contains 1 chromosome
    start - x and y coordinates of start point
    end - x and y coordinates of end point
    outputs - list of interpolated functions for each chromosome (list of PchipInterpolator objects)
            - points are also returned.
    
'''


def generate_trajectories(sorted_population, start, end):
    #Every chromosome's points are seperated and arranged in form of x and y cooridnates. \
    #It is then arranged in the order of x coordinated. Start and End point coordinates are then added to the array.
    #then the trajectories are generated.
    shape = np.shape(sorted_population)
    population_trajectories = []
    trajectory_points = np.zeros([shape[0], shape[1]+2, shape[2]])
    for i in range(shape[0]):
        ch_with_start = np.insert(sorted_population[i, :, :], 0, start, axis=0)
        chrome_all_pts = np.insert(ch_with_start, (shape[1] + 1), end, axis=0)
        population_trajectories.append(sc.PchipInterpolator(chrome_all_pts[:, 0], chrome_all_pts[:, 1]))
        trajectory_points[i, :, :] = chrome_all_pts
    return trajectory_points, population_trajectories


def format(population) -> object:
    shape = np.shape(population)
    sorted_population = np.zeros([shape[0], int(shape[1]/2), 2])
    for i in range(shape[0]):
        chrome = np.reshape(population[i, :], [int(shape[1]/2), 2])
        chrome_sorted = chrome[chrome[:, 0].argsort()].transpose()
        sorted_population[i, :, :] = chrome_sorted.transpose()
    return sorted_population


def check_point_validity(sorted_population, link1, link2) -> list:
    shape = np.shape(sorted_population)
    validity = []
    for i in range(shape[0]):
        r = np.linalg.norm(sorted_population[i, :, :], axis=1)
        if np.all(r > link1):
            if np.all(r < (link1+link2)):
                validity.append(True)
            else:
                validity.append(False)
        else:
            validity.append(False)
    return validity


def cleanse_chromosomes(sorted_population, validity):
    size = len(validity)
    print(sorted_population, '\n', validity)
    clean_population = sorted_population
    for i in range(size):
        if validity[size-i-1] == False:
            clean_population = np.delete(clean_population, (size-i-1), axis=0)
    return clean_population


def check_trajectory_validity(trajectories, obstacles):
    n = np.shape(obstacles)
    validity = [True for x in range(len(trajectories))]
    for i in range(n[0]):
        for path in trajectories:
                if path(obstacles[i][0]) > obstacles[i][1]:            #value of path at x is greater than y coord of point
                    validity[path] = False
                else:
                    continue
    print(validity)

    
def path_points(y, epsilon, start, end):
    '''
    y = PchipInterpolator object for chromosome
    epsilon = parameter for distance between points
    start = (x, y) coordinates of start point
    end = (x, y) coordinates of end point
    
    epsilon usage: increasing it will improve resolition at the cost of more points to work on.
                   decreasing it will improve computation time at the cost of resolution
    
    returns (2 x N) array of (X, Y) coordinates of points, where N = no. of points
    (N is variable to accomodate for equal disatnce between consecutive points)
    '''
    #temporary lists to store x and y coordinates
    pt_x = [start[0]]
    pt_y = [start[1]]
    der = y.derivative()
    
    #iterator point
    x = start[0]
    
    while (x < end[0]):
        del_x = epsilon/np.sqrt(der(x)**2 +1)
        if (x+del_x) < end[0] :
            pt_x.append(x+del_x)
            pt_y.append(y(x+del_x))
            x += del_x
        else:
            pt_x.append(end[0])
            pt_y.append(end[1])
            break
            
    points = np.zeros([2, len(pt_x)])
    points[0, :] = np.array(pt_x)
    points[1, :] = np.array(pt_y)

    return points


def fitness_chromosome(theta, mu):
    '''
    theta in format of
    [ th11 th12 th13 th14 ... th1n] 
    [ th21 th22 th23 th24 ... th2n]
    theta1 and theta 2 at dicrete pints on the path.
    internal variables:
    div = no. of theta divisions, 1 dimension of theta matrix
    '''
    #check this while changing code for different input format
    div = np.shape(theta)[1]
    
    theta_i = theta[:, 0:div-2]
    theta_j = theta[:, 1:div-1]
    del_theta = abs(theta_j - theta_i)
    fitness = 0
    for i in range(div-2):
        fitness += mu*del_theta[0, i] + (1-mu)*del_theta[1, i]
    return fitness

def testing_2():
    #test case
    X = [1, 2, 3, 4, 5, 6]
    Y = [0, 2, 3, 3, 2, 0]
    y = sc.PchipInterpolator(X, Y)
    epsilon = 0.01
    start = [1, 0]
    end = [6, 0]

    k = path_points(y, epsilon, start, end)
    print(k)
    plt.plot(k[0, :], k[1, :], 'ro')
    plt.show()
    print(fitness_chromosome(k, 0.5))

def testing():
    test_mat = np.array([[1.1, 2.2, 1.5, 2, -1, 1.3],
                         [-2, 1.5, 2, 2, 0, 0.75],
                         [0.5, 0.5, 1, 0.7, -2, 0.5]])
    start_pt = np.array([-3, 1])
    end_pt = np.array([3, 0.5])
    obst = np.array([2, 4])
    link1 = 1
    link2 = 3
    sorted_mat = format(test_mat)
    v = check_point_validity(sorted_mat, link1, link2)
    clean_population = cleanse_chromosomes(sorted_mat, v)
    points, trajectories = generate_trajectories(clean_population, start_pt, end_pt)
    check_trajectory_validity(trajectories, obst)
    t = np.linspace(-3, 3, 100)
    for i in range(len(trajectories)):
        ax = plt.plot(t, trajectories[i](t), lw=1)
        ap = plt.plot(points[i, :, 0], points[i, :, 1], 'ro')
    plt.show()

testing()




def radius_bounds(chrome):
    k = np.linalg.norm(chrome, axis=1)
    print(k)