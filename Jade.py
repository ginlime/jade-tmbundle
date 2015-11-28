import re
from sublime_plugin import TextCommand
import sublime


def isJade(view=None):
    if view is None:
        view = sublime.active_window().active_view()
    return 'text.jade' in view.scope_name(0)


class JadeIndentCommand(TextCommand):
    def is_enabled(self):
        return isJade(self.view)

    def is_visible(self):
        return False

    def is_scope(self, offset, scope):
        return self.view.score_selector(offset, scope) > 0

    def run(self, *args, **kwargs):
        indent = False
        sel = self.view.sel()
        if len(sel) == 1 and self.view.rowcol(sel[0].begin())[1] != 0:
            sel0 = sel[0]
            pos = sel0.begin() - 1
            if any(self.is_scope(pos, i) for i in ['entity.name.tag.jade', 'source.meta.function']):
                indent = True
        snippet = "\n"
        if indent:
            snippet = "\n\t"
        self.view.run_command('insert_snippet', { 'contents': snippet })
