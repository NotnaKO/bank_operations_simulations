import os
import pathlib


class SpacesInPathWithPyreverse(Exception):
    pass


def parse(dir_: str):
    with open("classes.puml") as f:
        lis = f.readlines()
    success = False
    while not success:
        try:
            for i in range(len(lis)):
                old_len = len(lis)
                if dir_ in lis[i] and lis[i].startswith("class "):
                    name = lis[i][lis[i].index(dir_):lis[i].index(" #")]
                    name_with_replace = name.replace(dir_, '')
                    j = 0
                    while j < len(lis):
                        if name_with_replace in lis[j] and name not in lis[j] and "--" in lis[j]:
                            print(f"Deleted {lis[j].rstrip()}")
                            del lis[j]
                        else:
                            j += 1
                    assert old_len == len(lis)
                    with_rep = lis[i].replace(dir_, '')
                    with_rep = with_rep[:with_rep.index('#')]
                    for first in range(len(lis)):
                        if with_rep in lis[first]:
                            for j in range(first + 1, len(lis)):
                                if lis[j].rstrip() == '}':
                                    lis = lis[:first] + lis[j + 1:]
                                    print(f"Deleted duplicate {with_rep}")
                                    assert False
        except AssertionError:
            pass
        else:
            success = True
    with open("classes.puml", 'w') as f:
        f.writelines(lis)


def make_uml():
    print("Starting creating UML file")
    f = []
    path = pathlib.Path(__file__).parent.resolve()
    path_with_code = path.parent / "src" / "python_code"
    os.chdir(path)
    for (root, _, filenames) in os.walk(path_with_code):
        for file in filenames:
            if file.endswith(".py"):
                full = str(pathlib.Path(root) / file)
                if ' ' in full:
                    ex = SpacesInPathWithPyreverse(
                        f"Spaces in the path is prohibited when using pyreverse: {full}")
                    s = (str(ex.__module__) + '.' if ex.__module__ != "__main__" else '') + str(
                        ex.__class__.__name__) + ': ' + str(ex.__str__())
                    sp_index = s.rfind(' ')
                    note = ' ' * sp_index + '^'
                    ex.add_note(note)
                    raise ex
                f.append(full)
    os.system(f"pyreverse -o puml {' '.join(f)} -A -S -f ALL --colorized")
    os.remove("packages.puml")
    print("Starting removing duplicates")
    parse("src.python_code.")
    parse("src.python_code.data.")
    parse("src.python_code.clients.")
    parse("src.python_code.accounts.")
    parse("src.python_code.session.")
    print("UML complete")


if __name__ == '__main__':
    make_uml()
