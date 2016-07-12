# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools.safe_eval import safe_eval as eval
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class ShopbasePp(models.Model):
    _name = "shop.pp"
    _description = u"品牌"
    _order = "code"
    name = fields.Char(u'品牌名称', required=True, translate=True)
    code= fields.Char(u'品牌代码', required=True, translate=True)
    com = fields.Many2one('res.company', required=True)



class ShopHtmb(models.Model):
    _name = "shopbase.htmb"
    _description = u"合同模板定义"
    _order = "code,name"
    name = fields.Char(u'模板名称', required=True, translate=True)
    ver = fields.Char(u'版本号', required=True, translate=True)
    com = fields.Many2one('res.company', required=True)


class ShopBase(models.Model):
    _name = "shop.base"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = u"商铺信息"
    _order = "code,name"
    name =  fields.Char(u'名称', required=True, translate=True)
    code= fields.Char(u'商铺编码', size=32, required=True)
    status= fields.Selection([('dz',u'待租'),('cz',u'已出租'),('zf',u'作废')], u'状态', required=True)
    kind=  fields.Selection([('shopgd',u'固定商铺'),('shopls',u'临时商铺'),('hdcz',u'活动场地'),('ggw',u'广告位')], u'商铺类型', required=True)
    jzarea=  fields.Float(u'建筑面积')
    zjarea=  fields.Float(u'出租面积')
    jyqy=fields.Many2one('csdm.shopbase.jyqy', string=u'经营区域', required=True)
    floor= fields.Selection([('b2',u'地下二楼'),('b1',u'地下一楼'),('1',u'一楼'),('2',u'二楼'),('3',u'三楼'),('4',u'四楼')], u'楼层', required=True)
    adlx= fields.Selection([('1',u'灯箱位'),('2',u'电梯广告'),('3',u'墙面喷绘'),('4',u'玻璃幕墙'),('5',u'景观展示'),('6',u'旗杆广告'),('7',u'包柱'),('8',u'LED广告')], u'广告位类型', required=True)
    source= fields.Selection([('init',u'定义'),('open',u'拆分'),('close',u'合并')], u'来源', required=True)
    address=fields.Text(u'地址')
    nr = fields.Html(u'内容')

    com=fields.Many2one('res.company',  required=True)
    _defaults = {
        'company_id': lambda self, cr, uid, ctx=None: self.pool.get('res.company')._company_default_get(cr, uid,'hr.job',  context=ctx),
    }



class ShopHt(models.Model):
    _name = "shop.ht"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = u"合同信息"
    _order = "code,name"
    name = fields.Char(u'合同标的', required=True, translate=True)
    htbh = fields.Char(u'合同编号', required=True, translate=True)
    htlx = fields.Selection(default='1', string=u'合同类型', required=True,selection=[('1', u'租赁'), ('2', u'租赁'),('3', u'联营'), ('4', u'联营管库存'), ('4', u'经销')])
    htzt = fields.Selection(default='1', string=u'合同状态', required=True, selection=[('1', u'草稿'), ('2', u'审批中'), ('3', u'已审批'), ('4', u'已生效'), ('5', u'已过期'), ('4', u'已终止')])
    htqsr = fields.Date(string=u'合同起始日', readonly=True, states={'draft': [('readonly', False)]}, index=True,copy=False)
    htzzr = fields.Date(string=u'合同终止日', readonly=True, states={'draft': [('readonly', False)]}, index=True, copy=False)
    jsbz =  fields.Integer(required=True, default=10)
    jfqrr= fields.Char('甲方', required=True, translate=True, select=True)
    yfqrr= fields.Char('乙方', required=True, translate=True, select=True)
    htmb= fields.Many2one('.htmb', string=u'Loss Account', domain=[('deprecated', '=', False)], help="Used to register a loss when the ending balance of a cash register differs from what the system computes")

class ShopHtzj(models.Model):
    _name = 'shop.htzj'
    _description = u"合同租金等信息"
    _order = ''

class ShopHtzqfy(models.Model):
    _name = 'shop.htzqfy'
    _description = u' 周期费用'
    _order = ''


class ShopHtfy(models.Model):
    _name = 'shop.htfy'
    _description = u'合同费用'
    _order = ''

