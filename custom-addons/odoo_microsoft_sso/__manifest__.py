# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Odoo Microsoft SSO",
  "summary"              :  """Odoo Microsoft SSO facilitates users to access Odoo website with single log-in credentials of Microsoft Website.""",
  "category"             :  "Website",
  "version"              :  "0.2",
  "license"              :  "Other proprietary",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "description"          :  """Odoo Microsoft Website Single Sign on
Odoo Microsoft SSO
Odoo Website SSO
Odoo Website Single Sign on
SSO
Single Sign-on
Website SSO
Website Single Sign-on
Website SSO in Odoo
SSO solution
Single Sign on solution
SSO in Odoo website
Single Sign-on in Odoo website
Multiple logins with a single credential
Microsoft SSO""",
  "depends"              :  [
                             'base',
                             'auth_oauth',
                            ],
  "data"                 :  ['data/microsoft_sso_data.xml'],
  "demo"                 :  [],
  "images"               :  ['static/description/microsoft-sso-v15.gif'],
  "price"                :  99,
  "currency"             :  "USD",
  "external_dependencies":  {'python': ['PyJWT'], 'bin': []},
}
