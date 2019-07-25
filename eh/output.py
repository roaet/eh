import mdv

from prettytable import PrettyTable
from prettytable import PLAIN_COLUMNS, NONE

from eh import constants


class Output(object):
    def __init__(self, conf):
        self.conf = conf

    def _topic_table(self, topics):
        t = PrettyTable(
            ['Subject', 'Summary'],
            padding_width=0,
            style=PLAIN_COLUMNS,
            vertical_char=' ', horizontal_char=' ', junction_char=' ',
            hrules=NONE)
        t.align['Subject'] = 'l'
        t.align['Summary'] = 'l'
        for topic in topics:
            t.add_row([topic.key, topic.summary])
        return t

    def _parent_table(self, top_level, parents, manager):
        t = PrettyTable(
            ['Subtopics', 'Topics', 'Samples'],
            padding_width=0,
            style=PLAIN_COLUMNS,
            vertical_char=' ', horizontal_char=' ', junction_char=' ',
            hrules=NONE)
        t.align['Subtopics'] = 'l'
        t.align['Topics'] = 'l'
        t.align['Samples'] = 'l'
        for parent in parents:
            full_parent = parent
            if top_level:
                full_parent = constants.KEY_DIVIDE_CHAR.join([
                    top_level, parent])
            tops, subtops = manager.get_topics_for_parent(full_parent)
            tops_list = []
            for top in tops:
                tops_list.append("%s" % top.shortkey)
            top_str = ", ".join(tops_list)
            t.add_row(
                [full_parent, "%d" % len(tops), top_str])
        return t

    def output_list(self, top_level, topics, parents, manager):
        top_level_str = "" if not top_level else (
            "For topic %s " % top_level)
        findings = "I have found %d topics and %d subtopics:" % (
                len(topics), len(parents))
        table_str = str(self._topic_table(topics))

        out = "%s%s\n%s" % (top_level_str, findings, table_str)
        if parents:
            out += "\n" +  " " * 30
            out += "\n%s" % self._parent_table(top_level, parents, manager)
        return out


class MarkdownOutput(Output):
    def __init__(self, conf):
        super(MarkdownOutput, self).__init__(conf)
        self.conf = conf
        self.no_colors = False

    def output_topic(self, topic):
        pre_md = topic.text
        md = mdv.main(pre_md, no_colors=self.no_colors)
        lines = md.splitlines()
        lines = [line for line in lines if line.strip()]
        return "\n".join(lines)
