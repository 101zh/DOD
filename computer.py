import cv2
import dlib
import serial
import time
from p_controller import PController

off_task: bool = False

controller : PController =  PController(0.1, 15)
SET_POINT : float = 160
last_servo_angle : float = 90

# Define the function to connect to Raspberry Pi Pico


def connect_pico():
    while True:
        try:
            # Find your Pico's COM port (check Device Manager on Windows)
            # Adjust COM port as necessary
            pico = serial.Serial('COM8', 115200)
            time.sleep(2)  # Give time for connection to establish
            print("Connected to Raspberry Pi Pico")
            return pico
        except serial.SerialException:
            print("Failed to connect to Pico. Retrying in 5 seconds...")
            time.sleep(5)

# Function to send X coordinate to Pico


def send_x_coordinate_to_pico(pico, x, frame_width):
    global last_servo_angle
    try:
        output, at_setpoint = controller.update(SET_POINT, x)
        print(x)
        # Convert X coordinate to servo angle (0-180 degrees)
        # Map X position (0 to frame_width) to servo angle (0 to 180)
        servo_angle = last_servo_angle + output

        # Clamp to valid servo range
        servo_angle = round(max(0, min(180, servo_angle)), 2)

        # Send angle to Pico
        command = f"~b{servo_angle}\n"
        pico.write(command.encode())
        # print(f"Sent X: {x} -> Servo Angle: {servo_angle}")
        last_servo_angle = servo_angle
    except serial.SerialException:
        print("Lost connection to Pico. Attempting to reconnect...")
        pico.close()
        pico = connect_pico()


# Initialize face cascade and parameters
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600


def detectAndTrackLargestFace():
    # Set camera index to 0 for the built-in webcam
    capture = cv2.VideoCapture(1)
    cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("base-image", 0, 100)
    cv2.moveWindow("result-image", 400, 100)
    cv2.startWindowThread()

    tracker = dlib.correlation_tracker()
    trackingFace = 0
    rectangleColor = (0, 165, 255)

    pico = connect_pico()  # Initialize Pico connection

    try:
        while True:
            global off_task
            with open("shared.info.txt", "r") as file:
                info: str = file.read()
                if info == "True" and (not off_task):
                    off_task = True
                    pico.write("~s\n".encode())
                elif info == "False" and (off_task):
                    off_task = False

            if pico.in_waiting > 0:
                response = pico.readline().decode().strip()
                print(f"Pico responded: {response}")

            rc, fullSizeBaseImage = capture.read()
            baseImage = cv2.resize(fullSizeBaseImage, (320, 240))
            frame_width = baseImage.shape[1]  # Get frame width for mapping

            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('Q'):
                cv2.destroyAllWindows()
                exit(0)

            resultImage = baseImage.copy()

            if not trackingFace:
                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)
                # print("Using the cascade detector to detect face")

                maxArea = 0
                x, y, w, h = 0, 0, 0, 0

                previousX = int(0)

                for (_x, _y, _w, _h) in faces:
                    if _w * _h > maxArea:
                        x, y, w, h = int(_x), int(_y), int(_w), int(_h)
                        maxArea = w * h

                if maxArea > 0:
                    tracker.start_track(baseImage,
                                        dlib.rectangle(x - 10,
                                                       y - 20,
                                                       x + w + 10,
                                                       y + h + 20))
                    trackingFace = 1

            if trackingFace:
                trackingQuality = tracker.update(baseImage)

                if trackingQuality >= 8.75:
                    tracked_position = tracker.get_position()
                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    cv2.rectangle(resultImage, (t_x, t_y),
                                  (t_x + t_w, t_y + t_h),
                                  rectangleColor, 2)

                    # Calculate center X position (ignore Y for horizontal tracking)
                    cX = int((t_x + t_x + t_w) / 2)
                    cY = int((t_y + t_y + t_h) / 2)
                    cv2.circle(resultImage, (cX, cY), 1, (0, 0, 255), -1)

                    # Draw "TARGET LOCKED" in red under the bounding box
                    font = cv2.FONT_HERSHEY_PLAIN
                    text_position = (t_x, t_y + t_h + 30)
                    cv2.putText(resultImage, "TARGET LOCKED",
                                text_position, font, 1, (0, 0, 255), 2, cv2.LINE_AA)

                    # Only send if X position changed significantly (ignore Y)
                    # if abs(cX - previousX) > 5:
                    #     previousX = cX
                    #     send_x_coordinate_to_pico(pico, cX, frame_width)

                    send_x_coordinate_to_pico(pico, cX, frame_width)

                else:
                    trackingFace = 0

            largeResult = cv2.resize(
                resultImage, (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))
            cv2.imshow("base-image", baseImage)
            cv2.imshow("result-image", largeResult)

    except KeyboardInterrupt as e:
        print(e.args)
        cv2.destroyAllWindows()
        pico.close()
        exit(0)


if __name__ == '__main__':
    detectAndTrackLargestFace()
