import kautham_python_interface as kautham
import ktmpb_python_interface

from collections import defaultdict

global switch_turn
switch_turn = defaultdict(lambda: defaultdict(dict))

def SWITCH_TURN(node, switch_turn, info, Line):
    print("**************************************************************************")
    print("  SWITCH TURN ACTION  ")
    print("**************************************************************************")
    action = Line[0]
    current_robot = Line[1]
    next_robot = Line[2]

    print(action + " " + current_robot + " " + next_robot)

    # Indices of the robots
    current_robot_index = switch_turn['Rob']
    next_robot_index = switch_turn['Next']

    # Set the next robot control
    if next_robot_index == 0:
        next_robot_control = 'controls/ur3_robotniq_A.cntr'
    elif next_robot_index == 1:
        next_robot_control = 'controls/ur3_robotniq_B.cntr'
    else:
        print("Invalid robot index")
        return False

    print("Switching control to robot index:", next_robot_index)
    kautham.kSetRobControlsNoQuery(node, next_robot_control)

    # Log the switch in the task file
    info.taskfile.write(f"\t<Switch-turn from=\"{current_robot}\" to=\"{next_robot}\">\n")
    info.taskfile.write(f"\t\t<Rob>{current_robot_index}</Rob>\n")
    info.taskfile.write(f"\t\t<Next>{next_robot_index}</Next>\n")
    info.taskfile.write("\t</Switch-turn>\n")

    return True

def Switch_turn_read(action_element):
    for val in action_element.attrib:
        globals()[val] = action_element.attrib[val]

    switch_turn = {}

    for el in action_element:
        try:
            globals()[el.tag] = int(el.text)
        except:
            try:
                globals()[el.tag] = [float(f) for f in str(el.text).strip().split()]
            except:
                globals()[el.tag] = str(el.text).strip()
        switch_turn.update({el.tag: globals()[el.tag]})

    return switch_turn

# Example usage:
# Assuming the XML action elements are parsed into `action_element`
# switch_turn_config = Switch_turn_read(action_element)
# SWITCH_TURN(node, switch_turn_config, info, Line)
