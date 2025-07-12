import serial
import time


def connect_pico():
    while True:
        try:
            # Find your Pico's COM port (check Device Manager on Windows)
            pico = serial.Serial('COM7', 115200)  # Adjust COM port as necessary
            time.sleep(3)  # Give time for connection to establish
            print("Connected to Raspberry Pi Pico")
            return pico
        except serial.SerialException:
            print("Failed to connect to Pico. Retrying in 5 seconds...")
            time.sleep(5)

def send_pico_message(pico : serial.Serial):
    try:
        print("attempt message")
        msg = f"Hello Pico!\n"
        pico.write(msg.encode())
        print("Sent hello")
        
    except serial.SerialException:
        print("Lost connection to Pico. Attempting to reconnect...")
        pico.close()
        pico = connect_pico()


orpheus_pico = connect_pico()

try:
    while True:
        time.sleep(1)
        send_pico_message(orpheus_pico)

except KeyboardInterrupt as e:
    print(str(e))
    orpheus_pico.close()
    exit(0)

    



