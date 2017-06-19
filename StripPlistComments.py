import plistlib
import os
import sys

comment_prefix = "#"

def check_keys(a_dict):
    # Checks all keys recursively
    tempDict = {}
    for key in a_dict:
        if key.startswith(comment_prefix):
            # It's a comment
            continue
        elif type(a_dict[key]) is list:
            temp = check_array(a_dict[key])
            if len(temp):
                tempDict[key] = temp
        elif type(a_dict[key]) is plistlib._InternalDict:
            temp = check_keys(a_dict[key])
            if len(temp):
                tempDict[key] = temp
        elif type(a_dict[key]) is str:
            if a_dict[key].startswith(comment_prefix):
                continue
            else:
                tempDict[key] = a_dict[key]
        else:
            # Not a dict or array - pass it in
            tempDict[key] = a_dict[key]
    return tempDict

def check_array(an_array):
    # Checks arrays recursively
    tempArray = []
    for item in an_array:
        if type(item) is plistlib._InternalDict:
            temp = check_keys(item)
            if len(temp):
                tempArray.append(temp)
        elif type(item) is list:
            temp = check_array(item)
            if len(temp):
                tempArray.append(temp)
        elif type(item) is str:
            if item.startswith(comment_prefix):
                continue
            else:
                tempArray.append(item)
        else:
            tempArray.append(item)
    return tempArray

def grab(prompt):
    if sys.version_info >= (3, 0):
        return input(prompt)
    else:
        return str(raw_input(prompt))


file_input = grab("Please drag and drop the plist on the terminal:  ")

print(" ")

# Add os checks for path escaping/quote stripping
if os.name == 'nt':
	# Windows - remove quotes
	file_input = file_input.replace('"', "")
else:
	# Unix - remove quotes and space-escapes
	file_input = file_input.replace("\\", "").replace('"', "")
	

# Remove trailing space if drag and dropped
if file_input[len(file_input)-1:] == " ":
    file_input = file_input[:-1]

# Expand tilde
file_input = os.path.expanduser(file_input)

if not os.path.exists(file_input):
    print("That file doesn't exist!")
    exit(1)

# Let's load it as a plist
plist = None
plist = plistlib.readPlist(file_input)

# Check if we got anything
if plist == None:
    print("That plist either failed to load - or was empty!")
    exit(1)

# Iterate and strip comments
new_dict = check_keys(plist)

# Write the new file
plistlib.writePlist(new_dict, file_input)

print("Done!\n")

grab("Press [enter] to close the script...")