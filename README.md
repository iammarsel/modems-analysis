# Radio/Modem Capacity Utilization Analysis/Statistics for a monthly time period

## An analysis program in Python that takes microwave radio event log data and converts it to a user friendly graph system with alerts!

This project is part of my work at Williams Communcations as a Software Developer, assisting Networking Engineers in automation of daily tasks and analysis of devices that are part of our framework. This application is meant to be a way to input modem capacity utilization data throughout the year from a Microwave Radio and analyze where Modems Speeds had time sections of instability and how stable these devices and connections are. Here are some statistics that are shown as a result:
- Total time under the total speed threshold throughout a chosen month
- A dynamic graph showing specific speed changes in each modem and combined speeds
- A maximum of 3 different graphs showing different connections to diffent counties in Florida

## Here is a display of how the application requests user input and shows the graph analysis using Python and matplotlib

<p align = center>
<img src="/demo_content/pic2.PNG" alt="" width="350" height="250" border="10" />
<img src="/demo_content/pic1.PNG" alt="" width="350" height="250" border="10" />
</p>

## How to use this app properly

The way to test this project would be to clone this project, install dependencies for Python, and try out the log files in the test-files folder. You can also choose your own file to analyze, but the formatting needs to be a standard EventLog file from a Microwave Radio. Here is a step by step for the installation:

1. Clone this project
2. Install Python and required dependencing through pip, which are tkinter, matplotlib, numpy, customtkinter
3. Import your own EventLog or use one of provided test files
4. Run the application and input the required data, including month, year, ports for each graph, and combined threshold that would trigger an alarm

## How to tweak this project for your own uses

Using an EventLog file is the way to go!

## Find a bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, reference the issue you created!

## Known issues

None

## Like this project?

Please consider leaving a star and a follow!