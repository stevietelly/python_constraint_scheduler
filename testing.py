l = {"hello": "", "two": "he"}

print(any([value == False for key, value in l.items()]))