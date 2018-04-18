"""Algorithm module to calculate heartrate from 
pulse sensor - RD117."""

def max_heart_rate_and_oxygen_sat(ir_buffer, red_buffer):
    """Calculate heart rate and Sp02 level. Keeping close to the original
    horror of 'algorithm.cpp' until we know what it does...
    ir_buffer - list()
    red_buffer - list()
    return 
    """
    # calculate DC mean and subtract DC from ir
    ir_mean = sum(ir_buffer) / len(ir_buffer)

    # remove DC and invert signal so that we can
    # use peak detector as valley detector
    an_x = [ir_mean - num for num in ir_buffer]

    # Calculate 4 point moving average
    # OSB! This ignores the last three values!?
    moving = []
    for nums in zip(an_x, an_x[1:], an_x[2:], an_x[3:]):
        moving.append(sum(nums) / 4)

    # Calculate threshold based on the moving average
    n_th1 = sum(moving) / len(ir_buffer)
    
    # Clamp threshold between 30 and 60 because...?!
    n_th1 = max(min(n_th1, 60), 30)

    # Use peak detector as valley-detector
    ir_valley_locs = [0] * 15
    maxim_find_peaks()
