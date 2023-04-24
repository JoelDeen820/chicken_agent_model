# chicken_agent_model

chickens

import enviroment run the following command
```bash
conda env create -f environment.yml
```

Note, 1 pixel is equal to 3 cm.

To-Do List
- [x] Create a simple barn environment
  - This will need to be appended to as the other few classes are added
- [x] Create a simple chicken
- [x] Create the Feedline Class
  - Center needs to affect occupancy of the barn its self (about 10 cm Diameter)
  - The feeder needs to be able to be filled with food (See waterline implementation)
- [x] Create the Waterline Class
- [x] Create the temperature map of the barn
  - Two types of heaters
    - Tube heaters (assume height of the barn)
    - Central Heaters (like this one [https://solvenoequipment.com/en/solveno-rmx-acv-fan-heater/](https://solvenoequipment.com/en/solveno-rmx-acv-fan-heater/)
  - Birds have a range where they are conformable (see paper [https://solvenoequipment.com/en/solveno-rmx-acv-fan-heater/](https://solvenoequipment.com/en/solveno-rmx-acv-fan-heater/) )
  - Birds may also do clumping based on how cold they are, you can see that in the paper. This is a stretch goal though
 - [ ] making the notebook look nice 
   - Currently, each class( for the most part) has their own file. This is ideal for development, as it keeps it more tidy.
      However, I think Graham would like all the code we wrote into the notebook its self. Probably compile everything into a single file at the end
 - [ ] Start working on the report, and see what exactly that should look like. 

