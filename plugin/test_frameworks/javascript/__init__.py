import json

from ...cache import cache
from .. import TestFramework as BaseTestFramework

PACKAGE_JSON = "package.json"


@cache
def get_package_json_content(root):
    package_json = root.file(PACKAGE_JSON)

    with open(package_json.path) as file:
        content = json.load(file)

        return content or {}


def has_package(package, root):
    content = get_package_json_content(root)

    return package in content.get("dependencies", {}) or package in content.get(
        "devDependencies", {}
    )


class TestFramework(BaseTestFramework):
    language = "javascript"
    test_patterns = (r'^\s*(?:it|test)\s*[\( ]\s*(?:"|\'|`)(.*)(?:"|\'|`)',)
    namespace_patterns = (
        r'^\s*(?:describe|suite|context)\s*[( ]\s*(?:"|\'|`)(.*)(?:"|\'|`)',
    )

    def has_package(self, package):
        return has_package(package, self.context.root)

    def _build_executable(self, executable):
        bin = self.file("node_modules", ".bin", executable)

        if bin.exists():
            return [bin.relpath]
        else:
            return [executable]
