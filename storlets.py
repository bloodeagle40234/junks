"""Implementation of magic functions for interaction with the OS.

Note: this module is named 'osm' instead of 'os' to avoid a collision with the
builtin.
"""
from __future__ import print_function
#-----------------------------------------------------------------------------
#  Copyright (c) 2012 The IPython Development Team.
#
#  Distributed under the terms of the Modified BSD License.
#
#  The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Stdlib
import io
import os
import re
import sys
from pprint import pformat
from swiftclient.client import Connection

# Our own packages
from IPython.core import magic_arguments
from IPython.core import oinspect
from IPython.core import page
from IPython.core.alias import AliasError, Alias
from IPython.core.error import UsageError
from IPython.core.magic import  (
    Magics, compress_dhist, magics_class, line_magic, cell_magic, line_cell_magic
)
from IPython.testing.skipdoctest import skip_doctest
from IPython.utils.openpy import source_to_unicode
from IPython.utils.process import abbrev_cwd
from IPython.utils import py3compat
from IPython.utils.py3compat import unicode_type
from IPython.utils.terminal import set_term_title

#-----------------------------------------------------------------------------
# Magic implementation classes
#-----------------------------------------------------------------------------
@magics_class
class StorletMagics(Magics):
    """Magics to interact with OpenStack Storlets 
    """

    def _uploadfile(self, container, obj, content, headers):
        """Submethod to upload content to Swift.
        """
        # host, username, key
        try:
            auth_url = os.environ['ST_AUTH']
            auth_user = os.environ['ST_USER']
            auth_password = os.environ['ST_KEY']
        except KeyError:
            print("You need to set ST_AUTH, ST_USER, ST_KEY for"
                  "Swift authentication")

        conn = Connection(auth_url, auth_user, auth_password)

        conn.put_object(
            container, obj, content,
            headers=headers)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'container_obj', type=unicode_type,
        help='container/object path to upload'
    )
    @cell_magic
    def uploadfile(self, line, cell):
        """Upload fthe contents of the cell to OpenStack Swift.
        """
        args = magic_arguments.parse_argstring(self.uploadfile, line)
        container, obj = args.container_obj.split('/', 1)
        self._uploadfile(continer, obj, cell,
                         {'Content-Type': 'application/python'})

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        'module_class', type=unicode_type,
        help='module and class name to upload'
    )
    @magic_arguments.argument(
        '-c', '--container', type=unicode_type, default='storlet',
        help='Storlet container name, "storlet" in default'
    )
    @magic_arguments.argument(
        '-d', '--dependencies', type=unicode_type, default='storlet',
        help='Storlet container name, "storlet" in default'
    )
    @cell_magic
    def uploadstorlet(self, line, cell):
        args = magic_arguments.parse_argstring(self.uploadstorlet, line)
        module_path = args.module_class
        assert module_path.count('.') == 1
        headers = {
            'X-Object-Meta-Storlet-Language': 'python',
            'X-Object-Meta-Storlet-Interface-Version': '1.0',
            'X-Object-Meta-Storlet-Object-Metadata': 'no',
            'X-Object-Meta-Storlet-Main': module_path,
            'Content-Type': 'application/octet-stream',
        }
        obj_name = '%s.py' % module_path.split('.')[0]
        self._uploadfile(args.container, obj_name, cell, headers)
