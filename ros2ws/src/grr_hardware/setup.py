from setuptools import setup
import os, glob

package_name = 'grr_hardware'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'hardware_map.yaml']),
        ('share/' + package_name + '/launch/', ['launch/teleop.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='philip',
    maintainer_email='philip@randomsmiths.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot = grr_hardware.robot:main',
            'drive = grr_hardware.drive:main',
            'teleop = grr_hardware.teleop:main'
        ],
    },
)
