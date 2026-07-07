import { WebsiteSale } from "@website_sale/interactions/website_sale";
import { patch } from "@web/core/utils/patch";

patch(WebsiteSale.prototype, {
    _onChangeCombination(ev, parent, combination) {
        super._onChangeCombination(...arguments);
        const retailPrice = parent.querySelector('.oe_retail_price');
        if (retailPrice) {
            const currencyValueSpan = retailPrice.querySelector('.oe_currency_value');
            if (combination.retail_price) {
                const precision = combination.currency_precision;
                const priceVal = this._priceToStr(combination.retail_price, precision);
                if (currencyValueSpan) {
                    currencyValueSpan.textContent = priceVal;
                } else {
                    retailPrice.textContent = priceVal;
                }
                // تأكد من إظهار صف سعر التجزئة إذا كان مخفياً
                retailPrice.closest('.d-flex')?.classList.remove('d-none');
            } else {
                // إخفاء صف سعر التجزئة إذا لم يكن هناك سعر تجزئة للبديل الجديد
                retailPrice.closest('.d-flex')?.classList.add('d-none');
            }
        }
    }
});
