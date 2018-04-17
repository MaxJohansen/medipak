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

    moving = []
    for nums in zip(an_x, an_x[1:], an_x[2:], an_x[3:]):
        moving.append(sum(nums) / 4)

    # Continue on line 117
