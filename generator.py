def int_to_base26(n, length):
    # The list of characters in base-26, with A = 0, B = 1, ..., Z = 25
    base26_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Handle zero case explicitly
    if n == 0:
        return 'A' * length
    
    # Convert integer to base-26 representation
    result = []
    while n > 0:
        result.append(base26_chars[n % 26])
        n //= 26
    
    # The result list now contains the base-26 characters but in reverse order, so reverse it
    result.reverse()
    
    # Convert the list into a string
    base26_str = ''.join(result)
    
    # Pad with 'A's to the left to match the required length
    # If the length is already long enough, no padding is added
    padded_result = base26_str.rjust(length, 'A')
    
    return padded_result

def generate_short_url():
    # Keep track of active pointers
    active_pointers = [True, True, True, True]  # start, end, middle, middle_plus_one
    lst = range(0, 11881376)

    start = 0
    end = len(lst) - 1
    middle = len(lst) // 2
    middle_plus_one = middle + 1
    width = 10
    while any(active_pointers):
        if active_pointers[0]:  # start pointer            
            if start > middle:  # When start surpasses middle, stop using start pointer
                active_pointers[0] = False
            else:
                yield int_to_base26(lst[start], 5)
                start += 1

        if active_pointers[1]:  # end pointer            
            if end < middle_plus_one:  # When end pointer crosses middle+1, stop using it
                active_pointers[1] = False
            else:
                yield int_to_base26(lst[end], 5)
                end -= 1

        if active_pointers[2]:  # middle pointer            
            if middle < start:  # Stop using middle pointer if it goes below start
                active_pointers[2] = False
            else:
                yield int_to_base26(lst[middle], 5)
                middle -= 1
        if active_pointers[3]:  # middle_plus_one pointer
            if middle_plus_one > end:  # Stop using middle_plus_one if it goes beyond end
                active_pointers[3] = False
            else:
                yield int_to_base26(lst[middle_plus_one], 5)
                middle_plus_one += 1

# Usage
def safe_next(gen, sentinel=None):
    try:
        return next(gen)
    except StopIteration:
        return sentinel

# Initialize the generator
short_url = generate_short_url()

# Function to get the next value when called
def get_next_value():
    return safe_next(short_url, sentinel=-1)
