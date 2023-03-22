import random
import json

use_diff_fill_rates = False
use_walk_to_tap_time = False


def seconds_to_string(seconds: float) -> str:
    """Function for turning the seconds in the string"""
    return "x minutes y seconds"


def create_tap(bottle: int, random_fill_rate=False) -> dict:
    """Function for creating a tap with a fill rate using a random rate 
    or fixed rate = 100ml"""
    if random_fill_rate:
        return {"flow_rate": random.randint(100, 200),
                "bottle_ml": bottle}
    return {"flow_rate": 100, "bottle_ml": bottle}


def create_taps(num_of_taps: int, bottles: list) -> list:
    """Function for creating the taps"""
    print(bottles)
    taps = []
    for i in range(num_of_taps):
        taps.append(create_tap(bottles[i], use_diff_fill_rates,))
    print("Taps:")
    print(json.dumps(taps, indent=3))
    return taps


def calculate_min_time_to_fill(taps: list) -> float:
    """Function for finding the minimum time to fill any of the bottles"""

    min = calculate_time_to_fill(taps[0]['flow_rate'], taps[0]['bottle_ml'])
    for tap in taps:
        time = calculate_time_to_fill(tap['flow_rate'], tap['bottle_ml'])
        if time < min:
            min = time

    return min


def calculate_time_to_fill(flow_rate: float, amount_to_fill: float):
    """Function for returning the remaining amount of time to fill this bottle"""
    return amount_to_fill / flow_rate


def fill_bottle_for_time(seconds: float, tap: float) -> dict:
    """Function for filling the bottle for flow_rate for amount of seconds 
    returning the bottle"""

    tap['bottle_ml'] = tap['bottle_ml'] - (tap['flow_rate'] * seconds)
    return tap


def fill_all_current_bottles_for_time(taps: list, seconds: float) -> list:

    for tap in taps:
        tap = fill_bottle_for_time(seconds, tap)
    print(taps)
    return taps


def count_filled_bottles(taps):
    """Function for counting the number of filled bottles on this iteration"""
    count = 0
    for tap in taps:
        if tap['bottle_ml'] == 0:
            count += 1
    return count


def replace_filled_bottles(taps: list, bottle_queue):
    """"""
    index = 0
    for tap in taps:
        if tap['bottle_ml'] == 0 and (index < len(bottle_queue)):
            tap['bottle_ml'] += bottle_queue[index]
        index += 1
    return taps


def get_rest_of_time(taps: list) -> float:
    """Function to calculate the rest of the time required to 
    fill the remaining bottles"""
    max = calculate_time_to_fill(taps[0]['flow_rate'], taps[0]['bottle_ml'])
    for tap in taps:
        time = calculate_time_to_fill(tap['flow_rate'], tap['bottle_ml'])
        if time > max:
            max = time

    return max


def calculate_time(bottles: list, num_of_taps: int) -> str:
    """Function for calculate the amount of time it takes to fill up the queues bottles"""

    # validate types
    if type(bottles) != list and type(num_of_taps) != int:
        print("Input type error")
        return
    # validate lengths
    if len(bottles) < 1 or num_of_taps < 1:
        print("Too few variables to calculate time with")
        return
    # validate contents of list

    total_seconds = 0

    num_of_bottles = len(bottles)
    bottles_filled = 0
    bottle_queue = bottles[num_of_taps:]
    initial_bottles = bottles[:num_of_taps]
    taps = create_taps(num_of_taps, initial_bottles)
    iteration = 1

    while bottles_filled < num_of_bottles:

        print(f"\niteration: {iteration}")
        if len(bottle_queue) > 0:
            iter_time = calculate_min_time_to_fill(taps)
            print(f"time for: {iter_time}")

            total_seconds += iter_time
            taps = fill_all_current_bottles_for_time(taps, iter_time)
            num_filled_bottles = count_filled_bottles(taps)

            print(f"number of filled bottles: {num_filled_bottles}")

            if len(bottle_queue) > 0:
                taps = replace_filled_bottles(taps, bottle_queue)
                bottle_queue = bottle_queue[num_filled_bottles:]
        else:
            total_seconds += get_rest_of_time(taps)
            break

        print(json.dumps(taps, indent=3))
        bottles_filled += num_filled_bottles
        iteration += 1

    print(f"Total time = {total_seconds}")


calculate_time([100, 100, 100, 200, 200, 200, 300, 300, 300], 3)
