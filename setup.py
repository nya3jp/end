# Copyright 2016 Shuhei Takahashi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools


setuptools.setup(
    name='end',
    version='1.3.1',
    author='Shuhei Takahashi',
    author_email='takahashi.shuhei@gmail.com',
    description='Introduces "end" keyword to Python.',
    url='https://github.com/nya3jp/end/',
    py_modules=['end'],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
