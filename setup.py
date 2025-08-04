from setuptools import setup, find_packages

setup(
    name='code_gen_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'openpyxl',
        'pandas',
    ],
    author='Nida Amir',
    author_email='nida.amir0083@gmail.com',
    description='A project that performs data analysis and visualization from Excel files',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/Nidaamir083/Financial_Data_Project.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
