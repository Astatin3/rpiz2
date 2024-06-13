import time
import RPi.GPIO as GPIO
import random


DATA_PIN = 3
CLK_PIN = 5

GPIO.setmode(GPIO.BOARD)

def append_to_byte(byte, value):
    return (byte << 1) | (1 if value else 0)


def get_bit_from_byte(byte, bit_pos):
    return (byte >> bit_pos) & 1


def send_data(send_text):
    GPIO.setup(DATA_PIN, GPIO.OUT)
    GPIO.setup(CLK_PIN, GPIO.OUT)

    send_bytes = []

    for char in send_text:
        send_bytes.append(ord(char))

    send_bytes.append(0b0)

    clock_state = True
    num = 0

    for byte in send_bytes:
        for i in range(8):
            GPIO.output(CLK_PIN, clock_state)
            clock_state = not clock_state

            bit = get_bit_from_byte(byte, i)

            GPIO.output(DATA_PIN, bit)

            print("1" if bit else "0")
            time.sleep(0.1)
            num += 1

    ## Fixes another weird bug
    for i in range(8):
        GPIO.output(CLK_PIN, clock_state)
        clock_state = not clock_state

        GPIO.output(DATA_PIN, False)
        time.sleep(0.1)


def recieve_data():
    GPIO.setup(DATA_PIN, GPIO.IN)
    GPIO.setup(CLK_PIN, GPIO.IN)

    last_byte = 0b0
    bit_num = 0

    byte_arr = []

    last_clock_state = GPIO.input(CLK_PIN)

    ## Due to a problem when the pyportal switches to output mode, it sends a clock signal, which needs to be ignored

    while last_clock_state == GPIO.input(CLK_PIN):
        pass
    last_clock_state = GPIO.input(CLK_PIN)

    while True:
        clock = GPIO.input(CLK_PIN)
        if clock != last_clock_state:
            last_clock_state = not last_clock_state

            bit = GPIO.input(DATA_PIN)
            print(bit, end='')

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

                # print("### " + str(len(byte_arr)))

    return byte_arr


send_text = input(">")

send_data(send_text)
#
# byte_arr = recieve_data()
# for byte in byte_arr:
#     print(chr(byte), end='')



print('\n\n')