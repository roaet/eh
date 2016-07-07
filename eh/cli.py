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

from eh import base_subject as base


SUBJECT_EP = 'eh.subject_extensions'


command_settings = {
    'ignore_unknown_options': True,
}


class Eh(object):

    def __init__(self, debug):
        self.subjects = {}
        self.debug = debug
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

        def fail2load(manager, entrypoint, exception):
            if self.debug:
                click.echo("Failed to load a subject: %s" % entrypoint)
                click.echo("Error is:\n%s" % exception)
            else:
                click.echo("A subject failed to load, please run with --debug")

        emgr = extension.ExtensionManager(
            SUBJECT_EP, invoke_on_load=False,
            on_load_failure_callback=fail2load)
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

    def subject_list(self):
        click.echo("I know about: ")
        for subject in self.subjects:
            click.echo(subject)
        click.echo("list (this list)")


@click.command(context_settings=command_settings)
@click.argument('subject')
@click.option('--debug', is_flag=True)
@click.pass_context
def main(context, subject, debug):
    if subject == 'list':
        Eh(debug=debug).subject_list()
        exit(0)
    Eh(debug=debug).run(subject)
    exit(0)
