# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
import re
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import AccessDenied

import dateutil.parser
try:
    import jwt
except Exception as e:
    _logger.info("Exception Found in PyJWT External Library : %r .", str(e))

from odoo import api, fields, models, _
import pprint
from odoo.fields import Datetime

def _get_user_details(id_token):
    #verify=Fasle in jwt version<2.0
    #options={"verify_signature": False} in jwt version>2.0
    #return jwt.decode(id_token, verify=False)
    _logger.info('jwt-----%r',jwt.__version__)
    if float(jwt.__version__[0]) <2.0:

        return jwt.decode(id_token, verify=False)
    else:
        return jwt.decode(id_token,options={"verify_signature": False})

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _microsoft_auth_oauth(self, provider, params):
        id_token = params.get('id_token')
        access_token = params.get('access_token')
        validation = _get_user_details(id_token)
        if validation.get('preferred_username'):
            validation['name'] = validation['preferred_username']
        # required check
        if validation.get('oid'):
            validation['user_id'] = validation['oid']
        else:
            raise AccessDenied()
        # retrieve and sign in user
        login = self.sudo()._auth_oauth_signin(provider, validation, params)
        if not login:
            raise AccessDenied()
        # return user credentials
        return (self.env.cr.dbname, login, access_token)
