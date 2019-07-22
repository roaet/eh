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
import os

import click 
import ConfigObject as conf

from eh import config
from eh import constants
from eh import git_store as gs
from eh import output
from eh import topic_manager as tm


command_settings = {
    'ignore_unknown_options': True,
}


@click.command(context_settings=command_settings)
@click.argument('subject', nargs=-1)
@click.option('--debug', is_flag=True)
@click.option('--no-colors', is_flag=True)
@click.pass_context
def main(context, subject, debug, no_colors):
    """
    Eh is a terminal program that will provide you with
    quick reminders about a subject.

    To get started run: eh help

    To figure out what eh knows about run: eh list

    To update the list of subjects: eh update

    Note:

    Eh will make a directory in your userhome called .eh
    where it will store downloaded subjects.
    """

    conf = config.open_config()
    if config.is_true(conf.eh.show_default):
        conf[constants.CONF_TOPIC_STORE][
            'eh_default'] = constants.DEFAULT_STORE


    topic_key = constants.KEY_DIVIDE_CHAR.join(subject)
    manager = tm.TopicManager(conf)
    out = output.MarkdownOutput(conf)

    test_git = gs.GitTopicStore(
            conf, "https://github.com/roaet/eh_subjects", 
            "/home/jhammond/.eh/eh_subjects")

    if topic_key == "list" or len(subject) == 0:
        topics, parents = manager.get_root_list()
        click.echo(out.output_list("", topics, parents, manager))
    elif topic_key == "update":
        manager.update()
    else:
        if manager.has_topic(topic_key):
            topic = manager.get_topic(topic_key)
            click.echo(out.output_topic(topic))
        elif manager.has_parent(topic_key):
            topics, parents = manager.get_topics_for_parent(topic_key)
            click.echo(out.output_list(
                topic_key, topics, parents, manager))
