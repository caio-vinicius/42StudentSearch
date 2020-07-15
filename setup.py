import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name="student-search",
	version="0.0.1",
	author="Caio Vinicius",
	author_email="csouza-f@student.42sp.org.br",
	description="CLI 42 Student",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="#",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
