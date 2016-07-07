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
import inspect
import itertools
from stevedore import extension

from remindme import base_subject as base


SUBJECT_EP = 'remindme.subject_extensions'


command_settings = {
    'ignore_unknown_options': True,
}


class RemindMe(object):

    def __init__(self):
        self.subjects = {}
        self._register_extensions('1.0')

    def _load_subject_with_module(self, module, version):
        classes = inspect.getmembers(module, inspect.isclass)
        for cls_name, cls in classes:
            if hasattr(cls, 'versions'):
                if version not in cls.versions:
                    continue
            else:
                continue
            if issubclass(cls, base.BaseSubject):
                if hasattr(cls, "keys"):
                    subject = cls()
                    for key in cls.keys:
                        self.subjects[key] = subject

    def _discover_via_entrypoints(self):
        emgr = extension.ExtensionManager(SUBJECT_EP, invoke_on_load=False)
        return ((ext.name, ext.plugin) for ext in emgr)

    def _register_extensions(self, version):
        for name, module in itertools.chain(self._discover_via_entrypoints()):
            self._load_subject_with_module(module, version)

    def run(self, subject, **kwargs):
        if subject not in self.subjects:
            click.echo("I do not know anything about %s." % subject)
            exit(1)
        subobj = self.subjects[subject]
        substr = click.style(subject, bold=True)
        click.echo("Reminding you about %s." % substr)
        click.echo(subobj.output())


@click.command(context_settings=command_settings)
@click.argument('subject')
@click.pass_context
def main(context, subject):
    RemindMe().run(subject)
    exit(0)
