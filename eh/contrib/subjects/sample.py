# Copyright (c) 2016 Justin L. Hammond
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from eh import base_subject as base

class SampleSubject(base.BaseSubject):
    keys = ['sample']
    versions = ['1.0']

    def output(self):
        output = """
This is an example of a subject for eh for other 
authors.
"""
        output += self.colored_bullet("colors supported")
        output += self.colored_bullet("overload the 'output' method")
        output += self.colored_bullet("create your own formatting with click")
        output += self.colored_bullet("or contribute to remindme core")
        return output
