from setuptools import find_packages, setup

setup(name='viaa-chassis',
      version='0.0.5',
      url='https://github.com/viaacode/chassis.py',
      license='GPL',
      author='Rudolf',
      author_email='rudolf.degeijter@viaa.be',
      description='VIAA Chassis',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md', encoding="utf8").read(),
      zip_safe=False,
      setup_requires=['wheel'],
      install_requires=['structlog>=19.2.0', 'pyyaml>=5.1.2', 'python-json-logger>=0.1.11'],
      entry_points={
         'console_scripts': ['openshift-create-pipeline=viaa.create_openshift_pipe:__main__',
                             'openshift-create-template=viaa.create_openshift_template:__main__'
                             ],
    },
      include_package_data=True,
)
