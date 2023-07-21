# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
import random
import json
import werkzeug.urls
import werkzeug.utils
from werkzeug.exceptions import BadRequest

from odoo import api, http, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied
from odoo.http import request
from odoo import registry as registry_get

from odoo.addons.auth_signup.controllers.main import AuthSignupHome as Home
from odoo.addons.web.controllers.utils import _get_login_redirect_url
from odoo.addons.auth_oauth.controllers.main import fragment_to_query_string

import logging
_logger = logging.getLogger(__name__)

class OAuthLoginInherit(Home):
    def list_providers(self):
        res = super(OAuthLoginInherit, self).list_providers()
        for provider in res:
            if "microsoft" in provider["auth_endpoint"]:
                state = self.get_state(provider)
                params = {
                "client_id":provider['client_id'],
                "scope":provider['scope'],
                "state":json.dumps(state),
                "redirect_uri":request.httprequest.url_root + 'microsoft/auth_oauth/signin',
                "response_type":'id_token token',
                "prompt":'login',
                "nonce":random.randrange(100000,999999,3),
                }
                provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.url_encode(params))
        return res

class MicrosoftSSO(http.Controller):

    @http.route('/microsoft/auth_oauth/signin', type='http', auth='none')
    @fragment_to_query_string
    def microsoft_signin(self, **kw):
        state = json.loads(kw['state'])
        dbname = state['d']
        if not http.db_filter([dbname]):
            return BadRequest()
        provider = state['p']
        context = state.get('c', {})
        registry = registry_get(dbname)
        with registry.cursor() as cr:
            try:
                env = api.Environment(cr, SUPERUSER_ID, context)
                credentials = env['res.users'].sudo()._microsoft_auth_oauth(provider, kw)
                cr.commit()
                action = state.get('a')
                menu = state.get('m')
                redirect = werkzeug.url_unquote_plus(state['r']) if state.get('r') else False
                url = '/web'
                if redirect:
                    url = redirect
                elif action:
                    url = '/web#action=%s' % action
                elif menu:
                    url = '/web#menu_id=%s' % menu
                _logger.info("these are the credentials for the signup process %r",credentials)
                # resp = login_and_redirect(*credentials, redirect_url=url)
                pre_uid = request.session.authenticate(*credentials)
                resp = request.redirect(_get_login_redirect_url(pre_uid, url), 303)
                resp.autocorrect_location_header = False
                # Since /web is hardcoded, verify user has right to land on it
                if werkzeug.urls.url_parse(resp.location).path == '/web' and not request.env.user.has_group('base.group_user'):
                    resp.location = '/'
                return resp
            except AttributeError:
                # auth_signup is not installed
                _logger.error("auth_signup not installed on database %s: oauth sign up cancelled." % (dbname,))
                url = "/web/login?oauth_error=1"
            except AccessDenied:
                # oauth credentials not valid, user could be on a temporary session
                _logger.info('OAuth2: access denied, redirect to main page in case a valid session exists, without setting cookies')
                url = "/web/login?oauth_error=3"
                redirect = werkzeug.utils.redirect(url, 303)
                redirect.autocorrect_location_header = False
                return redirect
            except Exception as e:
                # signup error
                _logger.exception("OAuth2: %s" % str(e))
                url = "/web/login?oauth_error=2"
        
        redirect = request.redirect(url, 303)
        redirect.autocorrect_location_header = False
        return redirect
