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

def get_function_purpose(transcript):
    if (any(['that','can'] == transcript[i:i+2] for i in range(len(transcript) - 1))) or (any(['that'] == transcript[i:i+i] for i in range(len(transcript) - 1))):
        has_purpose = True
    else:
        has_purpose = False
    return False, 'none'

def delete(transcript):
    with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'r') as file:
        data = file.readlines()

    # print(f"data = {data}")
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
    with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'w') as file:
        file.writelines(data)

def print_statement(transcript):
    try:
        location = transcript.index("Line")
    except:
        location = transcript.index("line")
    index = transcript[location+1:]
    print(f"index = {index}")
    index = list(filter(None, index))
    print(f"index = {index}")
    try:
        index = " ".join(index)
    except:
        pass
    print(f"index = {index}")
    try:
        index = int(WTN.parse(str(index)))
    except Exception as e:
        print(e)
    with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'r') as file:
        data = file.readlines()
    variable_line = data[index-1]
    variable = variable_line.split(' = ')
    variable = variable[0]
    print(f"variable = {variable}")
    spaces = []
    for char in range(len(variable)):
        if variable[char] == ' ':
            spaces.append(variable[char])
    print(f"variable = {variable}")
    variable = variable.replace(' ', '')
    print(f"variable = {variable}")
    print(f"spaces = {spaces}")
    space = ''
    space_num = len(spaces)
    space = space.rjust(space_num)
    print(f"space = {space}")
    try:
        spaces = spaces.join()
    except:
        pass
    print(f"spaces = {spaces}")
    spaces = spaces[0]
    print(f"spaces = {spaces}")
    data.insert(index, '%sprint(f"%s = {%s}")\n' % (space, variable, variable))
    with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'w') as file:
        file.writelines(data)


def get_string_purpose(transcript):
    fc = FunctionCreator()
    cc = ClassCreator()
    c = Comment()
    # print(f"transcript = {transcript}")
    function_has_purpose, function_purpose = get_function_purpose(transcript)
    make_function = any(['make','a', 'function'] == transcript[i:i+3] for i in range(len(transcript) - 1))
    delete_lines = any(['delete','lines'] == transcript[i:i+2] for i in range(len(transcript) - 1))
    make_class = any(['make','a', 'class'] == transcript[i:i+3] for i in range(len(transcript) - 1))
    delete_line = any(['delete','line'] == transcript[i:i+2] for i in range(len(transcript) - 1))
    add_print_statement = any(['print','line'] == transcript[i:i+2] for i in range(len(transcript) - 1))
    comment = True if any(['comment'] == transcript[i:i+1] for i in range(len(transcript) - 1)) or any(['comments'] == transcript[i:i+1] for i in range(len(transcript) - 1)) else False
    print(f"make function = {make_function}\ndelete_lines = {delete_lines}, {delete_line}\nmake class = {make_class}\nprint line = {add_print_statement}\ncomment line = {comment}")
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
    elif add_print_statement:
        print_statement(transcript)
    elif comment:
        c.determine_meaning(transcript)
        # create_class(name )


class FunctionCreator():
    def init(self):
        self.file = 'function.py'

    def create_function(self, name, is_purpose):
        if is_purpose == False:
            return f"""def {name}():
    pass\n"""
        else:
            purpose = self.get_function_purpose()
            return f"""def {name}():
    {purpose}\n"""

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


class ClassCreator():
    def init(self):
        self.file = 'function.py'

    def get_additional_variables(self, transcript):
        pass

    def get_additional_functions(self, transcript):
        pass

    def create_class(self, name, additional_functions, additional_variables):
        additional_variables = False
        additional_functions = False
        if additional_functions == False:
            if additional_variables == False:
                return f"""class {name}():
    def init(self):
        pass
    def foo(self):
        pass\n"""
            else:
                # variables = self.get_additional_variables()
                return f"""class {name}():
    def init(self):
        pass
    def foo(self):
        pass\n"""

    def write_class_to_file(self, name, purpose, transcript):
        additional_variables = self.get_additional_variables(transcript)
        additional_functions = self.get_additional_functions(transcript)
        location_specified, index = at_location(transcript)
        with open('function.py', 'r') as file:
            data = file.readlines()
        if location_specified:
            data.insert(int(index)-1, self.create_class(name, additional_functions, additional_variables))
        else:
            data.append(self.create_class(name, additional_functions, additional_variables))
        with open('function.py', 'w') as file:
            file.writelines(data)


class Comment():
    def init():
        pass
    def determine_meaning(self, transcript):
        comment_line = True if any(['comment', 'line'] == transcript[i:i+2] for i in range(len(transcript) - 1)) or any(['comments', 'line'] == transcript[i:i+2] for i in range(len(transcript) - 1)) else False
        comment_lines = True if any(['comment', 'lines'] == transcript[i:i+2] for i in range(len(transcript) - 1)) or any(['comments', 'lines'] == transcript[i:i+2] for i in range(len(transcript) - 1)) else False
        comment_print = True if any(['comment', 'print'] == transcript[i:i+2] for i in range(len(transcript) - 1)) or any(['comments', 'print'] == transcript[i:i+2] for i in range(len(transcript) - 1)) else False
        if comment_line or comment_lines:
            self.comment_line(transcript)
        if comment_print:
            self.comment_print_statements(transcript)

    def comment_line(self, transcript):
        try:
            location = transcript.index("Line")
        except:
            location = transcript.index("line")
        index = transcript[location+1:]
        print(f"index = {index}")
        index = list(filter(None, index))
        print(f"index = {index}")
        try:
            index = " ".join(index)
        except:
            pass
        print(f"index = {index}")
        try:
            index = int(WTN.parse(str(index)))
        except Exception as e:
            print(e)
        with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'r') as file:
            data = file.readlines()
        data_comment = data[index-1]
        if data_comment[0] == '#':
            comment_line = data_comment.replace('#', '')
        else:
            comment_line = f'#{data_comment}'
        data[index-1] = comment_line
        with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'w') as file:
            file.writelines(data)
    def comment_print_statements(self, transcript):
        with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'r') as file:
            data = file.readlines()
        for item in range(len(data)):
            if "print(f" in data[item] and "#" not in data[item]:
                data[item] = f"#{data[item]}"
            if "print(f" in data[item] and "#" in data[item]:
                un_comment = data[item].replace("#", '')
                data[item]
        with open('/Users/freycp1/Desktop/blamo_git/blamo_cfrey/blamo_irad_realistic_data/examples/ship_logistics/util.py', 'w') as file:
            file.writelines(data)
