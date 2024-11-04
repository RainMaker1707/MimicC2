# Mimic Server
Mimic is basically a tweaked flask server. It is a website that can hide commands in its page to communicate with the implant that is on the infected device.
Mimic get its name from its faculty to blend itself in the natural HTTP traffic has it send real webpage in the HTTP response.

The server has also an operator interface that allows the operator to send command to the implant.

Server keep a trace of each implant connected.

### Available Commands
- **kill** kill the implant and all communications
- **ls <arg>** ls the directory passed as argument. By default it list the current directory
- **create <arg>** create a file at the path in <arg>
- **screen** take a screenshot of the infected device