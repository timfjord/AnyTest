import json

from .. import TestFramework as BaseTestFramework


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


class TestFramework(BaseTestFramework):
    language = 'javascript'
    test_patterns = (r'^\s*(?:it|test)\s*[\( ]\s*(?:"|\'|`)(.*)(?:"|\'|`)',)
    namespace_patterns = (
        r'^\s*(?:describe|suite|context)\s*[( ]\s*(?:"|\'|`)(.*)(?:"|\'|`)',
    )
