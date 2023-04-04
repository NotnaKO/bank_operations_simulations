import os
import pathlib


class SpacesInPathWithPyreverse(Exception):
    pass


def check_dependencies(lis: list, name, name_with_replace):
    j = 0
    while j < len(lis):
        if name_with_replace in lis[j] and name not in lis[j] and "--" in lis[j]:
            rep = lis[j].replace(name_with_replace, name)
            print(f"Replaced {lis[j].rstrip()} to {rep.rstrip()}")
            lis[j] = rep
        else:
            j += 1
    success = False
    while not success:
        for i in range(len(lis)):
            if "--" in lis[i] and lis.count(lis[i]) > 1:
                print(f"Remove duplicate {lis[i]}")
                del lis[i]
                break
        else:
            success = True


def parse(dir_: str):
    print("Removing from", dir_)
    with open("classes.puml") as f:
        lis = f.readlines()
    success = False
    while not success:
        try:
            for i in range(len(lis)):
                if dir_ in lis[i] and lis[i].startswith("class "):
                    name = lis[i][lis[i].index(dir_):lis[i].index(" #")]
                    name_with_replace = name.replace(dir_, '')
                    check_dependencies(lis, name, name_with_replace)

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
                    # noinspection PyUnresolvedReferences
                    ex.add_note(note)
                    raise ex
                f.append(full)
    os.system(f"pyreverse -o puml {' '.join(f)} -A -S -f ALL --colorized")
    os.remove("packages.puml")
    print("Starting removing duplicates")
    parse("src.python_code.")
    for root, a, filenames in os.walk(path_with_code):
        for i in a:
            if "__" not in i:
                parse("src.python_code." + i.replace('\\', '.') + '.')
    print("UML complete")


if __name__ == '__main__':
    make_uml()
