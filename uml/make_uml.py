import os


class SpacesInPathWithPyreverse(Exception):
    pass


f = []
for (root, _, filenames) in os.walk("../source/python"):
    for file in filenames:
        if file.endswith(".py"):
            full = os.path.join(root, file)
            if ' ' in full:
                ex = SpacesInPathWithPyreverse(
                    f"Spaces in the path is prohibited when using pyreverse: {full}")
                s = str(ex.__class__.__name__) + ': ' + str(ex.__str__())
                sp_index = s.rfind(' ')
                note = ' ' * sp_index + '^'
                ex.add_note(note)
                raise ex
            f.append(full)
os.system(f"pyreverse -o puml {' '.join(f)} -A -S -f ALL --colorized")
os.remove("packages.puml")
