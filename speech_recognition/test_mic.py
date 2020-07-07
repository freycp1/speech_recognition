from ssl import Purpose
import speech_recognition as sr

interpretation_dictionary = {
    "multiply": "*",
    "multiplies": "*",
    "add": "+",
    "adds": "+",
    "subtracts": "-",
    "subtract": "-",

}
def write_function(name, purpose):
    if purpose == 'none': return f"def {name}():\n    pass\n{name}()\n"
    else: return f"def {name}():\n    {purpose}\n{name}()\n"

def create_function(name, purpose):
    location_specified, index = at_location(str)
    with open('function.py', 'r') as file:
        data = file.readlines()
    if location_specified:
        data.insert(int(index)-1, write_function(name, 'none'))
    else:
        data.append(write_function(name, 'none'))
    with open('function.py', 'w') as file:
        file.writelines(data)

def get_name(string):
    if "called" in str:
        index = str.index("called")
        name = str[(index + 1)]
    elif "named" in str:
        index = str.index("named")
        name = str[(index + 1)]
    else:
        name = "foo"
    return name

def delete(string):
    with open('function.py', 'r') as file:
        data = file.readlines()

    print(f"data = {data}")
    try:
        through_index = string.index("through")
        start_line = int(string[through_index - 1])
        end_line = int(string[through_index + 1])
        print(f"start line = {start_line}, end_line = {end_line}")
        try:
            for x in range(start_line-1, end_line):
                print(x)
                del data[start_line-1]
        except:
            pass
    except:
        line_index = string.index('line')
        line_to_delete = string[line_index+1]
        print(f"data")
        del data[line_to_delete-1]

    print(f"data = {data}")
    with open('function.py', 'w') as file:
        file.writelines(data)

def get_function_purpose(string):
    if (any(['that','can'] == string[i:i+2] for i in range(len(string) - 1))) or (any(['that'] == string[i:i+i] for i in range(len(string) - 1))):
        has_purpose = True
    else:
        has_purpose = False
    return False, 'none'

def get_string_purpose(string):
    name = get_name(string)
    function_has_purpose, function_purpose = get_function_purpose(string)
    make_function = any(['make','a', 'function'] == string[i:i+3] for i in range(len(string) - 1))
    delete_lines = any(['delete','lines'] == string[i:i+2] for i in range(len(string) - 1))
    delete_line = any(['delete','line'] == string[i:i+2] for i in range(len(string) - 1))
    print(f"make function = {make_function}, delete_lines = {delete_lines, delete_line}")
    if make_function:
        create_function(name, 'none')
        # if function_has_purpose:
        #     create_function(name, function_purpose)
        # else:
        # create_function(name, 'none')
    if delete_lines or delete_line:
        delete(string)

def at_location(string):
    line_specified = any(['at','Line'] == string[i:i+2] for i in range(len(string) - 1))
    if line_specified:
        location = string.index("Line")
        index = string[location+1]
        return True, index
    else:
        return False, None


while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something")
        audio=r.listen(source)
    try:
        print(r.recognize_google(audio),"\n")
        str = r.recognize_google(audio)
        str = str.split(' ')
        get_string_purpose(str)

    except:
        print("didnt understand")
