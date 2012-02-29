# -*- coding: utf-8 -*-

# Copyright 2012 Universidad Politécnica de Madrid

# This file is part of Wirecloud.

# Wirecloud is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Wirecloud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Wirecloud.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.utils.translation import ugettext as _

class Market(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    options = models.TextField(_('Options'))

    class Meta:
        app_label = 'wirecloud'

class MarketType(models.Model):
    label = models.CharField(_('Label'),max_length=50)
    display_name = models.CharField(_('Display_Name'),max_length=50)
    
    class Meta:
        app_label = 'wirecloud'