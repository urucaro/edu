#
# -*- coding: iso-8859-1 -*-
# Description: System assembly file for Education Proj
# Authors: Carolina Rodriguez
# $Date: $
# $LastChangedBy: $

{'src_root': '../..',
 'components': [
    {'name': 'core',
     'major_number': '1',
     'minor_number': '0',
     'patch_level': '0',
     'files': [
	{'from': 'src/modules/setup_myseries.py', 'to': ''},
	{'from': 'src/modules/myseries/__init__.py', 'to': 'myseries'},
	{'from': 'src/scripts/addic7ed.py', 'to': 'scripts'},
	{'from': 'src/app/myseries.wsgi.py', 'to': 'wsgi'},
	{'from': 'src/tpl/firstpage.tpl', 'to': 'tpl'},
	{'from': 'src/tpl/serieslist.tpl', 'to': 'tpl'},
	{'from': 'src/tpl/seasonslist.tpl', 'to': 'tpl'},
	{'from': 'src/tpl/list.tpl', 'to': 'tpl'},
	{'from': 'src/tpl/mystyle.css', 'to': 'tpl'},
	{'from': 'img/favicon.ico', 'to': 'img'},
	{'from': 'img/vallmo.jpg', 'to': 'img'},
	{'from': 'ins/model/install.sh', 'to': '../', 'chmod':'0775'},
	{'from': 'ins/model/www.carolina.com', 'to': '../'}
	
    ]
    }
]}

