# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging

from xivo_agid import agid
from xivo_dao import incall_dao
from xivo_dao import user_dao

logger = logging.getLogger(__name__)


_REVERSE_ENTITY_TO_PROFILE = {
    'pcm-dev': 'default',
}

_REVERSE_CONTEXT_TO_PROFILE = {
    'pcmdev': 'highly_custom',
}


def prepare_reverse_lookup(agi, cursor, args):
    incall_id = agi.get_variable('XIVO_INCALL_ID')
    incall = incall_dao.get(incall_id)

    if incall.action == 'user':
        agi.set_variable('XIVO_REVERSE_ID', incall.actionarg1)

    entity, context = _get_entity_context(incall.action, incall.actionarg1)

    # The context profile has a higher priority than the entity profile
    profile = _REVERSE_CONTEXT_TO_PROFILE.get(context, _REVERSE_ENTITY_TO_PROFILE.get(entity, ''))

    agi.set_variable('XIVO_REVERSE_PROFILE', profile)


def _get_entity_context(dest_type, dest_id):
    logger.debug('Finding entity and context for %s %s', dest_type, dest_id)
    if dest_type == 'user':
        return user_dao.get_entity_context(int(dest_id))
    else:
        logger.warning('Could not get a reverse profile for %s %s', dest_type, dest_id)


agid.register(prepare_reverse_lookup)
