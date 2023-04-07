# Torque Optimization of Robotic Arm System

<p align="center">
  <img width="910" height="476" src="https://user-images.githubusercontent.com/71158927/229153754-baeb0b9b-055f-4103-b1a4-484094e54173.png">
</p>

#### Development Team: [Camron Sabahi-Pourkashani](https://github.com/csabahi), [Joey Maillette](https://github.com/joeymaillette04), [Karthigan Uthayan](https://github.com/KarthiU)



## Problem
You are an engineer at a company that specializes in designing and building custom robotic manipulators, and have been tasked with developing a three-degree-of-freedom planar serial robotic manipulator. The goal of this project is to determine the optimal length of the three links of the manipulator (l1, l2, l3) in order to minimize the torques (T1, T2, T3) required to maintain the manipulator in a state of equilibrium. 
<p align="center">
  <img width="600" height="426" src="https://user-images.githubusercontent.com/71158927/229880723-53248afc-5736-400b-8db0-16802040d28c.png">
</p>
The material, width, and thickness of the manipulator's links have already been predetermined, and your job is to find the optimal link lengths that will make the base motor require the least amount of torque possible for the given positions.


## Approach
Instead of exclusively conducting research on conventional design patterns for three-degree-of-freedom machines, we have opted to develop a script that incorporates an initial "educated estimate" based on our findings, which will subsequently be refined utilizing the advanced frameworks available through Python.



## Built With
In order to develop this optimization script, we have utilized various python frameworks. Moreover, the successful implementation of this script also necessitates a strong grasp of static analysis within the domain of physics.


* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
* ![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)
* ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

Additional information about the project can be found in the [Report](https://github.com/joeymaillette04/MinTorqueScript/blob/main/TorqueReport.pdf).

## Solution
The program was run with an initial guess of [1, 1, 0.5], the SciPy optimization function took 31 iterations to refine the value's of the lengths (optimized torque ≈ 35Nm) which were then passed to TestAlgorithm.py where the values were fine-tuned to precisely: 

[1.0821468359052653, 1.0641662437491748, 0.6427511332656937] 

with a final combined torque of 32.872Nm.

![image](https://user-images.githubusercontent.com/71158927/230661833-93182f1e-7dbd-421c-811d-3c361726b79e.png)

## Contributors

* [Joey Maillette](https://www.linkedin.com/in/joeymaillette/)
* [Camron Sabahi-Pourkashani](https://www.linkedin.com/in/camron-sabahi/)
* [Karthigan Uthayan](https://www.linkedin.com/in/karthiganu2004/)



