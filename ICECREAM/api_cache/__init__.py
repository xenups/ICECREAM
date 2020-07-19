# -*- coding: utf-8 -*-
#
#    Copyright (C) 2016  Papavassiliou Vassilis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""`bottle-cache` package.
Cache plugin for bottle.py apps.
"""

__author__ = 'Papavassiliou Vassilis'
__date__ = '2015-12-10'
__version__ = '0.0.3'
__all__ = ['CachePlugin', 'cache_for']


from .plugin import CachePlugin, cache_for
