from words_to_num import WordsToNumbers
from ssl import Purpose
import speech_recognition as sr
# import words_to_num as wtn
WTN = WordsToNumbers()

#pinnyskenis
interpretation_dictionary = {
    "multiply": "*",
    "multiplies": "*",
    "add": "+",
    "adds": "+",
    "subtracts": "-",
    "subtract": "-",
}

def at_location(transcript):
    if any(['at','Line'] == transcript[i:i+2] for i in range(len(transcript) - 1)) or any(['at','line'] == transcript[i:i+2] for i in range(len(transcript) - 1)):
        try:
            location = transcript.index("Line")
        except:
            location = transcript.index("line")
        index = transcript[location+1]
        index = int(WTN.parse(str(index)))
        return True, index
    else:
        return False, None

def get_name(transcript):
    name = transcript[transcript.index("called") + 1] if "called" in transcript else transcript[transcript.index("named") + 1] if "named" in transcript else "foo"
    # if "called" in transcript:
    #     index = transcript.index("called")
    #     name = transcript[(index + 1)]
    # elif "named" in transcript:
    #     index = transcript.index("named")
    #     name = transcript[(index + 1)]
    # else:
    #     name = "foo"
    return name

def get_string_purpose(transcript):
    fc = functionCreator()
    cc = classCreator()
    print(f"transcript = {transcript}")
    function_has_purpose, function_purpose = get_function_purpose(transcript)
    make_function = any(['make','a', 'function'] == transcript[i:i+3] for i in range(len(transcript) - 1))
    delete_lines = any(['delete','lines'] == transcript[i:i+2] for i in range(len(transcript) - 1))
    make_class = any(['make','a', 'class'] == transcript[i:i+3] for i in range(len(transcript) - 1))
    delete_line = any(['delete','line'] == transcript[i:i+2] for i in range(len(transcript) - 1))
    print(f"make function = {make_function}, delete_lines = {delete_lines}, {delete_line}")
    if make_function and function_has_purpose:
        name = get_name(transcript)
        fc.write_function_to_file(name, function_purpose, transcript)
    elif make_function and not function_has_purpose:
        name = get_name(transcript)
        fc.write_function_to_file(name, False, transcript)
    elif delete_lines or delete_line:
        delete(transcript)
    elif make_class:
        name = get_name(transcript)
        cc.write_class_to_file(name, False, transcript)
        # create_class(name )

class functionCreator():
    def init(self):
        self.file = 'function.py'

    def create_function(self, name, is_purpose):
        if is_purpose == False:
            return f"""
def {name}():
    pass\n
"""
        else:
            purpose = self.get_function_purpose()
            return f"""
def {name}():
    {purpose}\n
"""

    def write_function_to_file(self, name, purpose, transcript):
        location_specified, index = at_location(transcript)
        with open('function.py', 'r') as file:
            data = file.readlines()
        if location_specified:
            data.insert(int(index)-1, self.create_function(name, purpose))
        else:
            data.append(self.create_function(name, purpose))
        with open('function.py', 'w') as file:
            file.writelines(data)


class classCreator():
    def init(self):
        self.file = 'function.py'

    def get_additional_variables(self):
        pass
    def create_class(self, name, additional_functions, additional_variables):
        if additional_functions == False:
            if additional_variables == False:
                return f"""class {name}():
    def init(self):
        pass
    def foo(self):
        pass
"""
            else:
                vars = self.get_additional_variables()
                return f"""class {name}():
    def init(self):
        pass
    def foo(self):
        pass\n
"""

    def write_class_to_file(self, name, purpose, transcript):
        location_specified, index = at_location(transcript)
        with open('function.py', 'r') as file:
            data = file.readlines()
        if location_specified:
            data.insert(int(index)-1, self.create_class(name, False, False))
        else:
            data.append(self.create_class(name, False, False))
        with open('function.py', 'w') as file:
            file.writelines(data)







def delete(transcript):
    with open('function.py', 'r') as file:
        data = file.readlines()

    print(f"data = {data}")
    try:
        through_index = transcript.index("through")
        try:
            line_index = transcript.index('lines')
        except Exception as e:
            line_index = transcript.index('line')
        start_line = transcript[line_index+1:through_index]
        end_line = transcript[through_index + 1:]
        try:
            start_line = int(start_line[0])
            end_line = int(end_line[0])
        except Exception as e:
            print(e)
            try:
                start_line = filter(None, start_line)
                end_line = filter(None, end_line)
                start_line = " ".join(start_line)
                end_line = " ".join(end_line)
            except Exception as e:
                print(e)
                pass
            start_line = WTN.parse(str(start_line))
            end_line = WTN.parse(str(end_line))
        try:
            for x in range(start_line-1, end_line):
                print(x)
                del data[start_line-1]
        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        line_index = transcript.index('line')
        line_to_delete = transcript[line_index+1:]
        try:
            line_to_delete = line_to_delete.join(line_to_delete)
        except Exception as e:
            print(e)
            pass
        try:
            line_to_delete = int(WTN.parse(str(line_to_delete[0])))
        except Exception as e:
            print(e)
            line_to_delete = int(line_to_delete[0])
        print(f"data")
        del data[line_to_delete-1]

    print(f"data = {data}")
    with open('function.py', 'w') as file:
        file.writelines(data)

def get_function_purpose(transcript):
    if (any(['that','can'] == transcript[i:i+2] for i in range(len(transcript) - 1))) or (any(['that'] == transcript[i:i+i] for i in range(len(transcript) - 1))):
        has_purpose = True
    else:
        has_purpose = False
    return False, 'none'


