# CS202-final-project


## New features 
For our final project we implemented another type of register allocation, linear scan, and created a machine learning based approach to decide which registers to use.

## Implementation
To implement this we modeified the passes to have a select-allocation pass and a more generic allocate registers. 
#### select-allocation:
Select allocation decides the type of allocation (linear scan or graph coloring) based on a machine learning model that has been pre trained on the data in the data folder. This model was trained using the faster allocation type as the target with other data #TODO.

#### allocate-registers:
Allocate registers takes in an allocation method and then runs either the graph coloring register allocation or linear scan allocation. Graph coloring runs the pre-existing build-interference and allocate-registers (which has now been renamed to allocate_registers_gc). Linear scan runs #TODO and then allocate-registers-ls. #TODO.

## Challenges remaining
