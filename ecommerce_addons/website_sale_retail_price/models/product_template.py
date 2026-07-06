from odoo import models, fields
from odoo.http import request

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1.0, uom_id=False, only_template=False):
        # 1. استدعاء الدالة الأصلية عبر super()
        res = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            uom_id=uom_id,
            only_template=only_template
        )
        
        # 2. الحصول على موقع الويب والشركة الحالية بشكل آمن
        website = self.env['website'].get_current_website()
        company = website.company_id
        
        # 3. التحقق من وجود قائمة أسعار التجزئة في إعدادات الشركة
        retail_pricelist = company.retail_pricelist_id
        if retail_pricelist:
            # حدد المنتج الفعلي (إذا كان هناك Variant نستخدمه، وإلا نستخدم الـ Template الحالي)
            product = self.env['product.product'].browse(res['product_id']) if res.get('product_id') else self
            uom = self.env['uom.uom'].browse(uom_id) or self.uom_id
            
            retail_price = retail_pricelist._get_product_price(
                product,
                quantity=add_qty or 1.0,
                uom=uom,
                currency=res.get('currency') or website.currency_id,
            )
            if res.get('product_taxes') is not None:
                retail_price = self._apply_taxes_to_price(
                    retail_price,
                    res.get('currency') or website.currency_id,
                    res.get('product_taxes'),
                    res.get('taxes'),
                    product,
                    website=website,
                )
            res['retail_price'] = retail_price
        else:
            res['retail_price'] = False
            
        return res
