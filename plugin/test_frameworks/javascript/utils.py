import json


PACKAGE_JSON = 'package.json'


def has_package(package, root):
    package_json = root.file(PACKAGE_JSON)

    if not package_json.exists():
        return False

    with open(package_json.path) as file:
        content = json.load(file)

        return package in content.get('dependencies', {}) or package in content.get(
            'devDependencies', {}
        )
