import time
import board
import digitalio
import supervisor

DATA_PIN = board.SDA
CLK_PIN = board.SCL

clock = digitalio.DigitalInOut(CLK_PIN)
data = digitalio.DigitalInOut(DATA_PIN)

def append_to_byte(byte, value):
    return (byte << 1) | (1 if value else 0)

def get_bit_from_byte(byte, bit_pos):
    return (byte >> (7-bit_pos)) & 1



def receive_data():
    data.direction = digitalio.Direction.INPUT
    clock.direction = digitalio.Direction.INPUT

    last_byte = 0b0
    bit_num = 0

    byte_arr = []

    last_clock_state = clock.value
    while True:
        if clock.value != last_clock_state:
            last_clock_state = not last_clock_state
            bit = data.value

            print("1" if bit else "0", end='')

            last_byte = append_to_byte(last_byte, bit)

            # last_byte[bit_num] = bit

            bit_num += 1

            if bit_num == 8:
                print('')
                if last_byte == 0:
                    break

                byte_arr.append(last_byte)

                bit_num = 0
                last_byte = 0
    return byte_arr

# print(byte_arr)
#
# for byte in byte_arr:
#     print(chr(byte), end='')

def send_data(send_text):
    data.direction = digitalio.Direction.OUTPUT
    clock.direction = digitalio.Direction.OUTPUT


    # send_text = 'This project was setup and tested using CircuitPython version 5 or higher. You will want to update your PyPortal and Libraries to match the version you are using.'
    send_bytes = [0b11111111, 0b11111111]

    for char in send_text:
        send_bytes.append(ord(char))

    send_bytes.append(0b0)

    clock_state = clock.value

    num = 0

    for byte in send_bytes:
        # print(bin(byte))
        for i in range(8):
            clock.value = clock_state
            clock_state = not clock_state

            bit = get_bit_from_byte(byte, i)

            data.value = bit

            # print(i, end='')
            print("1" if bit else "0", end='')
            num += 1
        print("")

    ## Fixes another weird bug
    for i in range(8):
        clock.value = clock_state
        clock_state = not clock_state
        data.value = False
        time.sleep(0.01)

print("Started!")

byte_arr = receive_data()

for byte in byte_arr:
    print(chr(byte), end='')