import random
import json

# Program settings
USE_DIFF_FILL_RATES = False
USE_WALK_TO_TAP_TIME = False
WALK_TIME = 2
FLOW_RATES = [100, 150, 200, 250]
DEFAULT_FILL_RATE = 100


# Error message types
class OutOfRangeError(Exception):
    pass


class InsufficientArgsError(Exception):
    pass


def seconds_to_string(seconds: float) -> str:
    """Function for turning the seconds in the string"""
    return "x minutes y seconds"


def create_tap(bottle: int) -> dict:
    """Function for creating a tap with a fill rate using a random rate 
    or fixed rate = 100ml"""
    if USE_DIFF_FILL_RATES:
        flow_rate = random.choice(FLOW_RATES)

        return {"flow_rate": flow_rate,
                "time_to_fill": calculate_time_to_fill_for_ml(flow_rate, bottle)}

    return {"flow_rate": DEFAULT_FILL_RATE, "time_to_fill":
            calculate_time_to_fill_for_ml(DEFAULT_FILL_RATE, bottle)}


def create_taps(num_of_taps: int, bottles: list) -> list:
    """Function for creating the taps"""
    taps = []
    # fewer bottles than taps
    if len(bottles) <= num_of_taps:
        for i in range(len(bottles)):
            taps.append(create_tap(bottles[i]))
    # more bottles than taps
    else:
        for i in range(num_of_taps):
            taps.append(create_tap(bottles[i]))
    print("Created Taps initiated with first bottles in queue:")
    print(json.dumps(taps, indent=3))

    return taps


def calculate_min_time_to_fill(taps: list) -> float:
    """Function for finding the minimum time to fill any of the bottles"""
    return min(tap['time_to_fill'] for tap in taps)


def calculate_time_to_fill_for_ml(flow_rate: float, amount_to_fill: float):
    """Function for returning the remaining amount of time to fill this bottle"""
    return amount_to_fill / flow_rate


def fill_bottle_for_time(seconds: float, tap: float) -> dict:
    """Function for filling the bottle for flow_rate for amount of seconds 
    returning the bottle"""
    tap['time_to_fill'] -= seconds

    return tap


def fill_all_current_bottles_for_time(taps: list, seconds: float) -> list:
    """Function for filling all the bottles currently being used"""
    return [fill_bottle_for_time(seconds, tap) for tap in taps]


def count_filled_bottles(taps):
    """Function for counting the number of filled bottles on this iteration"""
    return len([i for i in taps if i['time_to_fill'] == 0])


def replace_filled_bottles(taps: list, bottle_queue: list):
    """Function that replaces the bottles at the taps"""
    queue = bottle_queue.copy()
    for tap in taps:
        # if bottle is filled and more in the queue
        if tap['time_to_fill'] == 0 and len(queue) > 0:
            # replace bottle at tap with next in queue
            tap['time_to_fill'] = calculate_time_to_fill_for_ml(
                tap['flow_rate'], queue[0])
            if USE_WALK_TO_TAP_TIME:
                tap['time_to_fill'] += WALK_TIME

    return taps


def get_rest_of_time(taps: list) -> float:
    """Function to calculate the rest of the time required to 
    fill the remaining bottles"""

    return max(tap['time_to_fill'] for tap in taps)


def fill_bottles(taps: list, total_seconds: float):
    """Function for filling the bottles returns:
        - state of taps
        - total_seconds: by adding the time to fill the leas time consuming bottle
        - num_filled_bottles"""
    iter_time = calculate_min_time_to_fill(taps)
    total_seconds += iter_time
    taps = fill_all_current_bottles_for_time(taps, iter_time)
    num_filled_bottles = count_filled_bottles(taps)

    return taps, total_seconds, num_filled_bottles


def print_iteration_state(num_filled_bottles: int,
                          bottle_queue: list, total_seconds: float, taps: list):
    """Utility function for printing the state"""
    print(f"Number of filled bottles: {num_filled_bottles}")
    print(bottle_queue)
    print(f"Total seconds: {total_seconds}")
    print(json.dumps(taps, indent=3))


def print_iteration_stats(iteration: int, queue: list):
    """Function for printing the stats about the iteration"""
    print(f"\nIteration: {iteration}")
    print(f"Remaining Bottles: ")
    print(queue)


def print_final_fill_stats(taps: list,  queue: list):
    """Function for printing the stats for the final fill once queue is complete"""
    print(json.dumps(taps, indent=3))
    print(f"Finishing off rest of taps: + {get_rest_of_time(taps)} seconds")


def validate_inputs(bottles: list, num_of_taps: int):
    """Function for validating the inputs"""

    # validate types
    if not isinstance(bottles, list):
        error_msg = f"Bottles should be type list\nReceived type {type(bottles)}"
        raise TypeError(error_msg)
    if not isinstance(num_of_taps, int):
        error_msg = f"num_of_taps should be type int\nReceived type {type(num_of_taps)}"
        raise TypeError(error_msg)

    # validate number of args
    if len(bottles) < 1:
        error_msg = f"Too few bottles inputted to test"
        raise InsufficientArgsError(error_msg)
    if num_of_taps < 1:
        error_msg = f"Too few taps inputted to test"
        raise InsufficientArgsError(error_msg)

    # validate list is only integers
    if all(isinstance(bottle, int) for bottle in bottles) == False:
        error_msg = f"Not all bottles in list bottles are of type int"
        raise TypeError(error_msg)

    # validate list is filled with only positive integers above 0
    if all(bottle > 0 for bottle in bottles) == False:
        error_msg = f"One or more instances of bottles in queue are 0 or below"
        raise OutOfRangeError(error_msg)


def calculate_time(bottles: list, num_of_taps: int) -> str:
    """Function for calculate the amount of time it takes to fill up the queues bottles"""
    validate_inputs(bottles, num_of_taps)

    total_seconds = 0
    num_of_bottles = len(bottles)
    bottles_filled = 0
    bottle_queue = bottles[num_of_taps:]
    initial_bottles = bottles[:num_of_taps]
    taps = create_taps(num_of_taps, initial_bottles)
    iteration = 1

    while bottles_filled < num_of_bottles:

        print_iteration_stats(iteration, bottle_queue)

        # if there are still more bottles to fill since last iteration
        if len(bottle_queue) > 0:

            # fill bottles
            taps, total_seconds, num_filled_bottles = \
                fill_bottles(taps, total_seconds)

            # still more bottles to fill in queue
            if len(bottle_queue) > 0:

                # serve next in queue to empty taps ready for next iteration
                taps = replace_filled_bottles(taps, bottle_queue)
                bottle_queue = bottle_queue[num_filled_bottles:]

        # whole queue has been served / in process of being served by taps
        else:

            # calculate how long there is left to finish fill current bottles
            print_final_fill_stats(taps, bottle_queue)
            total_seconds += get_rest_of_time(taps)
            break

        print_iteration_state(num_filled_bottles,
                              bottle_queue, total_seconds, taps)
        bottles_filled += num_filled_bottles

        iteration += 1

    print(f"Total time = {total_seconds} seconds")
    return total_seconds


if __name__ == '__main__':

    calculate_time([100, 200, 100, 200, 200, 200, 300, 300, 300], 3)
    # calculate_time([100, 300, 100], 2)
