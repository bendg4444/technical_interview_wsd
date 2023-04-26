# technical_interview_wsd

# # Files:

- solution.py = This file contains the solution to the problem
- test.py = This file contains the tests for the edge cases

# # How to use Files:

# # # solution.py:

- - At the top of the file there are global variables:

- - - USE_DIFF_FILL_RATES: boolean. Selects random fill rates from the FLOW_RATES

- - - USE_WALK_TO_TAP_TIME: boolean. Adds a walk to tap time (Not for starting users). Uses global variable WALK_TIME.

- - - WALK_TIME: int. Dictates how long it takes for the queue to walk to the taps

- - - FLOW_RATES: list[int]: Dictates the different flow rates that could be selected

- - - DEFAULT_FILL_RATE: int. Dictates the standard flow rate for the taps.

- - command to run file: python3 initial_solution.py

# # # test.py:

- - command to run file: pytest test.py
