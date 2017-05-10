from score.tpl import Renderer
import sass


class SassRenderer(Renderer):
    """
    :class:`score.tpl.TemplateConverter` for scss files.
    """

    def __init__(self, sass_conf, *args, **kwargs):
        self._sass_conf = sass_conf
        super().__init__(*args, **kwargs)

    def render_string(self, string, variables, path=None):
        functions = dict((name, value)
                         for name, value in variables.items()
                         if callable(value))
        functions.update((name, value)
                         for name, value, _ in self.filetype.globals
                         if callable(value))
        result = sass.compile(string=string,
                              include_paths=self._tpl_conf.rootdirs,
                              output_style='expanded',
                              source_comments='line_numbers',
                              custom_functions=functions)
        # Remove BOM from output:
        # https://github.com/dahlia/libsass-python/pull/52
        if result.startswith('\ufeff'):
            result = result[1:]
        return result

    def render_file(self, file, variables, path=None):
        functions = dict((name, value)
                         for name, value in variables.items()
                         if callable(value))
        functions.update((name, value)
                         for name, value, _ in self.filetype.globals
                         if callable(value))
        result = sass.compile(filename=file,
                              include_paths=self._tpl_conf.rootdirs,
                              output_style='expanded',
                              source_comments='line_numbers',
                              custom_functions=functions)
        # Remove BOM from output:
        # https://github.com/dahlia/libsass-python/pull/52
        if result.startswith('\ufeff'):
            result = result[1:]
        return result
