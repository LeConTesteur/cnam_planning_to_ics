import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

KEYWORDS = ('')
DESCRIPTION = ''
CLASSIFIERS = []

requirements = [
    "pydantic",
    "ics"
]

requirements_tests = [
]

extras = {
    'tests': requirements_tests,
}

NAME = 'cnam_planning_to_ics'
MODULE = NAME.replace("-", "_")
setuptools.setup(
    name=NAME,
    version="0.0.1",
    author="LeConTesteur",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/LeConTesteur/{NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/LeConTesteur/{NAME}/issues",
    },
    classifiers=CLASSIFIERS,
    package_dir={NAME: MODULE},
    packages={"": MODULE},
    python_requires=">=3.8",
    install_requires = requirements,
    tests_require = requirements_tests,
    extras_require = extras,
    keywords=KEYWORDS,
)
