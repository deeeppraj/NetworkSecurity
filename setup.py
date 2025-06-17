'''
the setup py is used to ppackage and distriute python projects
used to define the configurations of your project such as dependencies metadata  etc
'''

from setuptools import find_packages , setup


def get_requ(file_name):
    requirements = []
    try:
        with open (file_name , "r") as file:
            
            pack = file.readlines()
            for i in range(len(pack)):
                line = pack[i].strip()
                if(line == '-e .'):
                    pass
                else:
                    requirements.append(line)

       
    
    except Exception as  e:
        print(e)
    
    return requirements


            

           

setup(
    name='Network Security',
    version= "0.0.0.1",
    author= "Deepraj",
    author_email="work.deepraj@gmail.com",
    packages= find_packages(),
    install_requires = get_requ("requirements.txt")
    
    )