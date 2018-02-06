# Playing Snake using Q-learning technique by Jegors Baļzins
Example of using Q-learning technique to play snake game. Performs averege score up to 19 after 10e6 iterations, may perform more after trial of other agent and reward configurations.
## Usage
Train by running:
```
python snake_game.py train
```
Test by running:
```
python snake_game.py test
```
To play yourself rewrite drawing and input functions and run by:
```
python snake_game.py play
```
## Outputs
After trainging, file ```table.Qtable ``` will contain data of Q-table and file ```training_data.txt```  will contain statistics about trainging.
After testing, file ```test_data.txt``` will contain statistics about testing.
You may perform files to output other values.
