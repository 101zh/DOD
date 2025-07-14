# Duck Off Doomscrolling

## Project Overview
This project was made as a part of [Highway Undercity](https://highway.hackclub.com), a 4 day in person Hackathon hosted by [Hack Club](https://hackclub.com) and Github. The goal of this project is to provide a funny way to discourage distractions while you are trying to be productive. The idea is to have a rubber duck on your desk that will spray water at you whenever you go on an unproductive app or website, such as Instagram Reels, Youtube Shorts, or Tiktok.

## Technical Details
The base of the design is a cheap water gun powered by a servo motor, servo motors to pivot the duck towards the user, allowing for accuracy even in situations where the user is moving. The position of the user is attained using an hd webcam running OpenCV for facetracking. The base of doomscrolling detection is Apple Shortcuts, which ping a webserver whenever a non-desired app is opened.

##BOM
| Quantity | Name                    | Description                                                       | Source                                                                        |
|----------|-------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------------------|
| 3        | MG 996R Servo Motor     | Used for trigger, pitch and yaw control                           |                                                                               |
| 1        | Orpheus Pico            | Used for servo control, Hack Club version of Raspberry Pi Pico    |                                                                               |
| 1        | Water Pistol            | Used for shooting water, disassembled to basic components         | https://www.target.com/p/tidal-storm-hydro-storm-5pk/-/A-91989016#lnk=sametab |
| 1        | Breadboard              | Used for Circuit connections, could use perfboard instead         |                                                                               |
| 1        | Breadboard Power Supply | Powers 5V to servos from the 9V battery, any Buck Converter works |                                                                               |
| 1        | 9V battery              | Powers the servos                                                 |                                                                               |
| ~10      | Jumper Cables           | Circuit connections                                               |                                                                               |
| 1        | HD Webcam               | Used for face tracking                                            |                                                                               |
| 6        | 3D Printed Parts        | Packaging/Mounting                                                |                                                                               |
| 10       | Hot Glue Sticks         | Mounting and sealing                                              |                                                                               |
| Idk      | M3 screws               | For servo mounting and other                                      |                                                                               |
| Idk      | M3 Heatset Inserts      | Fort servo mounting and other                                     |                                                                               |

