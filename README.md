# Robotic-Arm-Trajectory-Planning-using-Genetic-Algorithm

## Work Done

- Implementation of Genetic Algorithm for finding the interior points joining the initial (start) and target (end) point.
- Found the path for the end-effector to traverse using Cubic Hermite Interpolation. 
- Used reverse kinematics for finding link angles at discrete points on the path. These are used to calculate a fitness value for the chromosome. 
- Reference paper model implemented as 2-link model. 
- Improvised this model to create 3-link model.
- Displaying results –plotting fitness values over generation, and plotting entire path for end-effector.

## Genetic Algorithm
- Random generation of initial population(chromosome).
- Calculating its fitness using fitness function.
- Using Roulette Wheel Method picking the chromosome.
- Doing crossover and mutation of the selected chromosome and getting the new chromosome.
- Repeating it for a set number of generation.

## Trajectory generation and fitness calculation
Cubic Hermite Interpolation: Generates a twice differentiable function over a range of finite points in creating one-to-one mapping in X -> Y
Fitness calculation: Trajectory divided into finite points at same distances (defined by ∊)
Energy function defined as as :
E = 𝝁1T1  + 𝝁2T2 + 𝝁3T3			( 𝝁j is jth coefficient of energy)
Tj = ∑(θi - θi-1)j 		(j = link number, i = step number)

**Contributions**

Aakriti Agrawal - Genetic Algorithm.
Rishabh Mathur - Hermite Interpolation, checking chromosome validity.
Ashutosh Purohit - Fitness Value Calculation , Inverse Kinematics for 2 and 3 link arm.
Fauzan Zaid Khan - Display and animation , Compilation of all codes.

### Conclutions and Future Recommendatins
This technique can be used to control robotic arms in industrial areas where inefficiencies can lead to heavy losses.
Can be extended to 3D with each link rotating in a different plane.
Can use potential space method to calculate cost.
