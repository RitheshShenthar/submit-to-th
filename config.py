# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

here = os.path.dirname(os.path.abspath(__file__))

config = {
    'test_types': {
        'functional': {
            'harness_config': os.path.join('firefox_ui_tests', 'qa_jenkins.py'),
            'harness_script': os.path.join('firefox_ui_tests', 'functional.py'),
            'treeherder': {
                'group_name': 'TUI',
                'group_symbol': 'TUIS',
                'job_name': 'Trial ({locale})',
                'job_symbol': '{locale}',
                'tier': 3,
                'log_reference': 'log_info.txt',
                #'artifacts': {
                #    'log_info.log': os.path.join(here, 'build', 'upload', 'logs', 'log_info.log'),
                #    'report.html': os.path.join(here, 'build', 'upload', 'reports', 'report.html'),
                #},
                #'log_references': 
                #{
                #    'url': 'http://pastebin.com/2nmPgqyb',
                #    'name': 'buildbot_text'
                #}
                #,
            },
        },
    },
}
