import sys
import re

def parse_ibis(file_path):
    """Parse the IBIS file to extract component and pin data."""
    component_data = {}
    pin_data = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    component_capacitance = None
    parsing_pins = False

    for line in lines:
        line = line.strip()

        # Check for component capacitance
        if line.startswith("C_comp"):
            component_capacitance = line.split()[-1]
        
        # Check for start of pin section
        if line.startswith("[Pin]"):
            parsing_pins = True
            continue

        # Check for end of pin section
        if line.startswith("["):
            parsing_pins = False

        # Parse pin data
        if parsing_pins and not line.startswith("|") and line:
            parts = re.split(r'\s+', line)
            pin_name = parts[0]
            inductance = parts[4]
            capacitance = parts[5]
            pin_data[pin_name] = {
                'inductance': inductance,
                'capacitance': capacitance
            }
    
    return component_capacitance, pin_data

def format_engineering_notation(value):
    """Convert a value into engineering notation."""
    value = float(value)
    exp = 0
    prefixes = {12: 'T', 9: 'G', 6: 'M', 3: 'k', 0: '', -3: 'm', -6: 'u', -9: 'n', -12: 'p'}
    
    while abs(value) >= 1000 and exp < 12:
        value /= 1000
        exp += 3
    while abs(value) < 1 and exp > -12:
        value *= 1000
        exp -= 3
    
    return f"{value:.3f} {prefixes[exp]}"

def print_pin_data(component_capacitance, pin_data, pins):
    """Print the component and pin data."""
    print(f"Component Capacitance: {format_engineering_notation(component_capacitance)}F\n")
    
    for pin in pins:
        if pin in pin_data:
            inductance = format_engineering_notation(pin_data[pin]['inductance']) + "H"
            capacitance = format_engineering_notation(pin_data[pin]['capacitance']) + "F"
            print(f"Pin: {pin}")
            print(f"    Inductance: {inductance}")
            print(f"    Capacitance: {capacitance}\n")
        else:
            print(f"Pin: {pin} not found in IBIS file.\n")

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        pins = sys.argv[2].strip("()").split(",")
    else:
        file_path = input("Enter the path to the IBIS file: ")
        pins = input("Enter the list of pins (comma-separated, e.g., M13,M19,M16,A20,AB44): ").strip().split(",")

    pins = [pin.strip() for pin in pins]
    
    component_capacitance, pin_data = parse_ibis(file_path)
    print_pin_data(component_capacitance, pin_data, pins)

if __name__ == "__main__":
    main()
