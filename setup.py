from setuptools import setup

setup(name='take_me_to_develop',
      version='0.1',
      description='Take me to develop!',
      url='https://github.com/wat-izz/take_me_to_develop',
      author='Adam Narkunski',
      author_email='adamnarkunski@gmail.com',
      license='MIT',
      packages=['take_me_to_develop'],
      install_requires=['gitdb2==2.0.0',
                        'GitPython==2.1.0',
                        'smmap2==2.0.1',
                        'wheel==0.24.0', ],
      test_requires=['pytest'],
      entry_points={
          'console_scripts': ['take-me-to-develop=take_me_to_develop.take_me_to_develop:main'],
      },
      zip_safe=False)


def readme():
    with open('README.md') as f:
        return f.read()
