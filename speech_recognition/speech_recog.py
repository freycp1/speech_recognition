from ssl import Purpose
import speech_recognition as sr

def create_function(name, purpose):
    if purpose == 'none': return f"def {name}():\n    pass\n{name}()\n"
    else: return f"def {name}():\n    {purpose}\n{name}()\n"
r = sr.Recognizer()

voice = sr.AudioFile('function_if_else 4 2.aif')
with voice as source:
    audio = r.record(source)

print(type(audio))
print(r.recognize_google(audio))
str = r.recognize_google(audio)

str = str.split(' ')

if "called" in str:
    index = str.index("called")
    name = str[(index + 1)]
elif "named" in str:
    index = str.index("named")
    name = str[(index + 1)]
else:
    name = "foo"
with open('function.py', 'r') as file:
        data = file.readlines()
data.append(create_function(name, 'none'))
with open('function.py', 'w') as file:
    file.writelines(data)


print(name)
