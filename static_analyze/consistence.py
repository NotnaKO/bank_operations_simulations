from os.path import exists


def check_uml():
    """Check if uml exists"""
    assert exists("../uml/packages.puml") and exists("../uml/classes.puml")


def check_data():
    """Check if data exists"""
    assert exists("../data/data.json")


def check_src():
    """Check if src exists"""
    assert exists("../src")


def check_tests():
    """Check if tests exists"""
    assert exists("../tests")


def check_readme_and_license():
    """Check if README.md exists and LICENSE by correctness"""
    assert exists("../README.md") and exists("../LICENSE")
    with open("../LICENSE") as file:
        lines = file.readlines()
        for line in lines:
            if "Kopanov Anton" in line:
                break
        else:
            assert False


def check_consistence():
    check_tests()
    check_src()
    check_data()
    check_uml()
    check_readme_and_license()


if __name__ == '__main__':
    check_consistence()
