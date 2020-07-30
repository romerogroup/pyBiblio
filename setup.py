from distutils.core import setup

setup(
    name="pyBiblio",
    version="1.0.1",
    author="Marie Dumaz,Aldo Romero",
    author_email="mcd0029@mix.wvu.edu,alromero@mail.wvu.edu",
    url="https://github.com/romerogroup/pyBiblio",
    packages=["pybiblio"],
    license="LICENSE",
    data_files=[("", ["LICENSE"])],
    package_data={"pybiblio": ["FU.csv"]},
    description="A Python library for basic bibliometic measures.",
    install_requires=["pandas", "numpy", "nltk",],
)
