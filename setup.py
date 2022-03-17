import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bw_activity_replacement',
    version='0.0.1',
    author='Fabian Lechtenberg',
    author_email='fabian.lechtenberg@upc.edu',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/UPC-FL/bw_activity_replacement.git',
    project_urls = {

    },
    license='UPC',
    packages=['bw_activity_replacement'],
    install_requires=[],
)