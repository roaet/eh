# coding: utf-8
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
import sys

from eh import mdv
import os 

class BaseSubject(object):

    def __init__(self):
        reload(sys); sys.setdefaultencoding('utf-8')
        self._subjects = {}

    @property
    def subjects(self):
        return self._subjects.keys()

    def populate_subjects(self, target_path):
        file_paths = []
        for file in os.listdir(target_path):
            if file.endswith(".md"):
                file_paths.append("%s/%s" % (target_path, file))
        for file in file_paths:
            with open(file, 'r') as myfile:
                data = myfile.read().splitlines()
                top_line = data.pop(0)
                subjects = [x.strip() for x in top_line.split(',')]
                full_text = "\n".join(data)
                for subject in subjects:
                    self._subjects[subject] = full_text

    def output(self, subject, no_colors=False):
        if subject not in self.subjects:
            return None
        pre_md = self._subjects[subject]
        pre_md = "Reminding you about **%s**\n%s" % (subject, pre_md)
        md = mdv.main(pre_md, no_colors=no_colors)
        lines = md.splitlines()
        lines = [line for line in lines if line.strip()]
        return "\n".join(lines)
