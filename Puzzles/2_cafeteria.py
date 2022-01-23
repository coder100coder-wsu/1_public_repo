from typing import List


# Write any import statements here

def getMaxAdditionalDinersCount(N: int, K: int, M: int, S: List[int]) -> int:
    # Write your code here
    total_seats_qty = N - 1
    # counting starts at 0 not 1, as in 0th (or index zero) seat is the first seat
    social_dist_offset_qty = K
    new_seats_required_qty = M
    S.sort(reverse=False)
    occupied_seats_index = S
    occupied_seats_qty = len(occupied_seats_index)
    available_seats_index = []  # index of available seats
    left_replaced_seats_index = []
    right_replaced_seats_index = []
    seat_labels = [i for i in range(1, total_seats_qty + 1)]  # assign seat labels

    for i in range(0, total_seats_qty):
        available_seats_index.append(1)  # initialize to zero, match length to total_seats_qty
        left_replaced_seats_index.append(1)
        right_replaced_seats_index.append(1)

    print("available_seats_index=  {}, total_seats_qty= {}, len(available_seats_index)= {}"
          .format(available_seats_index, total_seats_qty, len(available_seats_index))
          )

    # available_seats_qty = int(total_seats_qty - occupied_seats_qty
    #                           - 2 * social_dist_offset_qty * occupied_seats_qty)
    # print("available_seats_qty= {}, total_seats_qty= {}, occupied_seats_qty= {}, "
    #       "social_dist_offset_qty= {}".
    #       format(available_seats_qty, total_seats_qty, occupied_seats_qty,
    #              social_dist_offset_qty)
    #       )
    # min_occupied_seat_index = min(occupied_seats_index) - 1  # seat count starts at 0th seat
    # max_occupied_seat_index = max(occupied_seats_index) - 1  # seat count starts at 0th seat
    # min_available_index = min_occupied_seat_index - 2 * social_dist_offset_qty * occupied_seats_qty
    # max_available_index = max_occupied_seat_index + 2 * social_dist_offset_qty * occupied_seats_qty
    #
    # if min_available_index < 1:  # no seats to left of first occupied seat
    #     available_seats_qty -= 1  # reduce 1 from qty based on above index condition
    #
    # if max_available_index < 1:  # no seats to right of last occupied seat
    #     available_seats_qty -= 1  # reduce 1 from qty based on above index condition

    # print("min_occupied_seat_index= ", min_occupied_seat_index)
    # print("max_occupied_seat_index= ", max_occupied_seat_index)
    # print("NEW available_seats_qty= ", available_seats_qty)
    # 2*K because social distancing is BOTH left and right side
    # problem state table is row-like, not circular or other format
    def update_occupied_seats(occupied_seats_index):
        try:
            for item in occupied_seats_index:
                available_seats_index[item - 1] = 0
                left_replaced_seats_index[item - 1] = 0
                right_replaced_seats_index[item - 1] = 0
            return 0
        except:
            return -1

    print("occupied_seats_index=      ", occupied_seats_index)
    print("          seat_labels=     ", seat_labels)
    print("available_seats_index=     ", available_seats_index)

    def left_replace(available_seats_index, social_dist_offset_qty):
        for i in range(0, len(available_seats_index)):
            for j in range(1, social_dist_offset_qty + 1):
                try:
                    if available_seats_index[i] == 0:
                        left_replaced_seats_index[i - j] = 0
                        # print("left_replaced_seats_index= ", left_replaced_seats_index)
                    else:
                        continue
                    return 0
                except:
                    return -1
                    # break

    # print("          seat_labels=     ", seat_labels)
    # print("available_seats_index=     ", available_seats_index)
    def right_replace(available_seats_index, social_dist_offset_qty):
        for i in range(0, len(available_seats_index)):
            for j in range(1, social_dist_offset_qty + 1):
                try:
                    if available_seats_index[i] == 0:
                        right_replaced_seats_index[i + j] = 0
                        # print("right_replaced_seats_index=", right_replaced_seats_index)
                    else:
                        continue
                    return 0
                except:
                    return -1
                    # break

    def update_available_seats(available_seats_index):
        try:
            for i in range(0, len(available_seats_index)):
                available_seats_index[i] = min(available_seats_index[i],
                                               left_replaced_seats_index[i],
                                               right_replaced_seats_index[i])
            return 0
        except:
            return -1

    def calc_available_seat_qty():
        available_seats_qty = sum(
            available_seats_index[i] for i in range(0, len(available_seats_index)))
        print("available_seats_qty= ", available_seats_qty)
        return available_seats_qty

    print("          seat_labels= ", seat_labels)
    print("available_seats_index= ", available_seats_index)

    # seat additional people
    def add_people():
        for i in range(0, len(available_seats_index)):
            if available_seats_index[i] == 1:
                available_seats_index[i] = 0
        return 0

    a = update_occupied_seats(i for i in occupied_seats_index)
    b = left_replace(available_seats_index, social_dist_offset_qty)
    c = right_replace(available_seats_index, social_dist_offset_qty)
    update_available_seats(available_seats_index)
    result = calc_available_seat_qty()

    return result


print("result= ", getMaxAdditionalDinersCount(10, 1, 2, [2, 6]))
print("\n")
print("result= ", getMaxAdditionalDinersCount(15, 2, 3, [11, 6, 14]))
