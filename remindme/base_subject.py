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
import click


class BaseSubject(object):

    def colored_bullet(self, words, color='green'):
        bullet = click.style(' - ', fg=color, bold=True)
        return "%s%s\n" % (bullet, words)

    def bullet2col(self, first, second, color='green'):
        bullet = click.style(' - ', fg=color, bold=True)
        firstcol = click.style(first, bold=True)
        secondcol = second
        return "%s%s\t%s\n" % (bullet, firstcol, secondcol)

    def output(self):
        return ""
