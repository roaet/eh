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
@click.option('--debug', is_flag=True, hidden=True)
@click.option(
    '--no-colors', is_flag=True,
    help='Do not display colors on output')
@click.option(
    '--repo', multiple=True,
    help='Limit to a repo; can be used multiple times',
    default=[])
@click.option(
    '--list', 'dolist', is_flag=True, default=False,
    help='List known subjects')
@click.option(
    '--update', is_flag=True, default=False,
    help='Update all repos, or those given with --repo option')
@click.option(
    '--min_score', default=50,
    help="Minimum match score (0 - 100) to consider matching: defaults to 50")
@click.option(
    '--search_score', default=35,
    help="Minimum search score (0 - 100) to show in list: defaults to 35")
@click.pass_context
def main(
        context, subject, debug, no_colors, repo,
        dolist, update, min_score, search_score):
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

    repo_list = [str(x) for x in list(repo)]
    do_list = dolist
    do_update = update

    conf = config.open_config()
    if config.is_true(conf.eh.show_default):
        conf[constants.CONF_TOPIC_STORE][
            'eh_default'] = constants.DEFAULT_STORE

    topic_key = constants.KEY_DIVIDE_CHAR.join(subject)
    manager = tm.TopicManager(conf, repo_list, search_score)
    out = output.MarkdownOutput(conf)

    if do_list:
        topics = manager.get_all_topics()
        topics.sort(key=lambda x: str(x[1].key))
        click.echo(out.output_list(topics))
    elif do_update:
        manager.update()
    else:
        meta_results = manager.meta_search(topic_key)
        if len(meta_results) == 0:
            click.echo("Did not find anything matching that")
        elif len(meta_results) == 1 and meta_results[0][0] >= min_score:
            topic = meta_results[0][2]
            print(topic)
            click.echo(out.output_topic(topic))
        elif len(meta_results) == 1 and meta_results[0][0] < min_score:
            topic = meta_results[0][2]
            click.echo("Did you mean to look up %s?" % topic.shortkey)
            click.echo("The summary of it is: %s" % topic.summary)
        elif(
                len(meta_results) > 1 and
                meta_results[0][0] - meta_results[1][0] > 20):
            topic = meta_results[0][2]
            click.echo(out.output_topic(topic))
        else:
            click.echo("I found things like that: ")
            click.echo(out.output_meta(meta_results))
