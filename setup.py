# Process Inspector
#
# Contributors:
# - Aravind Sankaran


from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='process_inspector',
    version="1.0.0",
    description="The core library for synthesising event logs into visualisations for process inspection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='Aravind Sankaran',
    author_email='aravindsankaran22@gmail.com',
    packages= find_packages(), # finds packages inside current directory
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3",
    #Depends on graphviz and lxml
    install_requires=open("requirements.txt").read().splitlines(),

)
