# Copyright © 2017,2018 STRG.AT GmbH, Vienna, Austria
# Copyright © 2018 Necdet Can Ateşman, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

from score.tpl import Renderer
import sass
import os
import hashlib


class SassRenderer(Renderer):
    """
    :class:`score.tpl.Renderer` for scss (and sass) files.
    """

    def __init__(self, sass_conf, *args, **kwargs):
        self._sass_conf = sass_conf
        super().__init__(*args, **kwargs)

    def render_string(self, string, variables, path=None):
        if path and self._sass_conf.cachedir:
            cached_result = self._load_cache(path, variables)
            if cached_result is not None:
                return cached_result
        functions = dict((name, value)
                         for name, value in variables.items()
                         if callable(value))
        functions.update((name, value)
                         for name, value, _ in self.filetype.globals
                         if callable(value))
        result = sass.compile(string=string,
                              include_paths=self._tpl_conf.rootdirs,
                              output_style='expanded',
                              source_comments=True,
                              custom_functions=functions)
        # Remove BOM from output:
        # https://github.com/dahlia/libsass-python/pull/52
        if result.startswith('\ufeff'):
            result = result[1:]
        if path and self._sass_conf.cachedir:
            self._cache(path, variables, result)
        return result

    def render_file(self, file, variables, path=None):
        if path and self._sass_conf.cachedir:
            cached_result = self._load_cache(path, variables)
            if cached_result is not None:
                return cached_result
        functions = dict((name, value)
                         for name, value in variables.items()
                         if callable(value))
        functions.update((name, value)
                         for name, value, _ in self.filetype.globals
                         if callable(value))
        result = sass.compile(filename=file,
                              include_paths=self._tpl_conf.rootdirs,
                              output_style='expanded',
                              source_comments=True,
                              custom_functions=functions)
        # Remove BOM from output:
        # https://github.com/dahlia/libsass-python/pull/52
        if result.startswith('\ufeff'):
            result = result[1:]
        if path and self._sass_conf.cachedir:
            self._cache(path, variables, result)
        return result

    def _cache(self, path, variables, content):
        cachefile = self._cache_file(path, variables)
        os.makedirs(os.path.dirname(cachefile), exist_ok=True)
        open(cachefile, 'w').write(content)

    def _load_cache(self, path, variables):
        cachefile = self._cache_file(path, variables)
        try:
            return open(cachefile).read()
        except FileNotFoundError:
            return None

    def _cache_file(self, path, variables):
        cachefile = os.path.join(self._sass_conf.cachedir, path)
        if variables:
            variables_hash = hashlib.sha256(str(variables)).hexdigest()
            cachefile = os.path.join(cachefile, variables_hash)
        return cachefile
