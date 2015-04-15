# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2015
#    Author scosist
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

class pdm_node(models.Model):
    _name = 'pdm.node'

    node_name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('rel_node_name_uniq', 'unique(node_name)', _('A node with the same name already exists [rel_node_name_uniq]')),
    ]

class pdm_category(models.Model):
    _name = 'pdm.category'

    cat_name = fields.Char('Name', required=True)
    cat_description = fields.Char('Description', required=True)
    track_version = fields.Boolean('Track Version', required=True)
    track_depends = fields.Boolean('Track Depends', required=True)

class pdm_directory(models.Model):
    _name = 'pdm.directory'

    @api.one
    @api.constrains('parent_id')
    def _check_parent_id(self):
        if self.parent_id is None and self.id != 0:
            raise ValidationError(_('Invalid Parent ID!'), _('Parent ID is required for a child directory'))

    parent_id = fields.Many2one('pdm.directory', 'Parent Directory', compute='eck_parent_id')
    dir_name = fields.Char('Name', required=True)
    default_cat = fields.Many2one('pdm.category', 'Category', required=True)

class pdm_type(models.Model):
    _name = 'pdm.type'

    #file_ext unique, case insensitive, force to lower
    file_ext = fields.Char('File Extension', required=True)
    default_cat = fields.Many2one('pdm.category', 'Category', required=True)
    icon = fields.Binary()
    type_regex = fields.Char('RegEx', required=True)
    description = fields.Char('Description', required=True)

class pdm_entry_name_filter(models.Model):
    _name = 'pdm.entry.name.filter'

    name_proto = fields.Char('Proto', required=True)
    name_regex = fields.Char('RegEx', required=True)
    description = fields.Char('Description', required=True)

class pdm_entry(models.Model):
    _name = 'pdm.entry'

    dir_id = fields.Many2one('pdm.directory', 'Directory', required=True)
    entry_name = fields.Char('Name', required=True)
    type_id = fields.Many2one('pdm.type', 'Type', required=True)
    cat_id = fields.Many2one('pdm.category', 'Category', required=True)
    checkout_user = fields.Many2one('', 'Checkout User')
    checkout_date = fields.DateTime()
    checkout_node = fields.Many2one('pdm.node', 'Checkout Node')

class pdm_version(models.Model):
    _name = 'pdm.version'

    entry_id = fields.Many2one('pdm.entry', 'Entry', required=True)
    file_size = fields.Integer(size=64, required=True)
    file_modify_stamp = fields.DateTime(required=True)
#    blob_ref = fields.oid
    md5sum = fields.Binary()
    preview_image = fields.Binary()
    release_user = fields.Many2one('', 'Release User')
    release_date = fields.DateTime()
    release_tag = fields.Char()

class pdm_property(models.Model):
    _name = 'pdm.property'
    
    @api.model
    def _prop_type_get(self):
        return [('text', 'date', 'number', 'yesno')]

    @api.one
    @api.constrains('prop_type')
    def _check_prop_type(self):
        types = _prop_type_get
        if self.prop_type not in types:
            raise ValidationError(_('Invalid Type!'), _('Property Type must be one of: %s') % types)

    prop_name = fields.Char('Name', required=True)
    prop_type = fields.Selection(_prop_type_get, 'Type', required=True, compute='_check_prop_type')

class pdm_version_property(models.Model):
    _name = 'pdm.version.property'

    version_id = fields.Many2one('pdm.version', 'Version', required=True)
    prop_id = fields.Many2one('pdm.property', 'Property', required=True)
    text_value = fields.Text()
    date_value = fields.DateTime()
    number_value = fields.Float()
    yesno_value = fields.Boolean()

class pdm_category_property(models.Model):
    _name = 'pdm.category.property'

    cat_id = fields.Many2one('pdm.category', 'Category', required=True)
    prop_id = fields.Many2one('pdm.property', 'Property', required=True)
    require = fields.Boolean()

class pdm_version_relationship(models.Model):
#class pdm_version_version_rel(models.Model):
#    _name = pdm.version.version.rel'
    _name = 'pdm.version.relationship'

    parent_id = fields.Many2one('pdm.version', 'Parent')
    child_id = fields.Many2one('pdm.version', 'Child', ondelete='cascade')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
