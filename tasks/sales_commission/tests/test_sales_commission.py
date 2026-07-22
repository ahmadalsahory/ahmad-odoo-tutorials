# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSalesCommission(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.salesperson = cls.env['res.users'].create({
            'name': 'Test Salesperson',
            'login': 'test_salesperson',
            'email': 'test_salesperson@example.com',
        })

        cls.commission_plan = cls.env['sales.commission.plan'].create({
            'name': 'Test Commission Plan',
            'user_ids': [(4, cls.salesperson.id)],
            'line_ids': [
                (0, 0, {'amount_from': 0.0, 'amount_to': 1000.0, 'rate': 10.0}),
                (0, 0, {'amount_from': 1001.0, 'amount_to': 5000.0, 'rate': 20.0}),
            ]
        })

    def test_commission_rate_calculation(self):
        """Test getting commission rate for different net sales amounts."""
        rate_500 = self.commission_plan.get_commission_rate(500.0)
        self.assertEqual(rate_500, 10.0, "Rate for $500 should be 10%")

        rate_3000 = self.commission_plan.get_commission_rate(3000.0)
        self.assertEqual(rate_3000, 20.0, "Rate for $3000 should be 20%")

        rate_10000 = self.commission_plan.get_commission_rate(10000.0)
        self.assertEqual(rate_10000, 0.0, "Unmatched range should return 0%")

    def test_res_users_commission_plan_assignment(self):
        """Test assigning commission plan directly on res.users record."""
        self.assertEqual(self.salesperson.commission_plan_id, self.commission_plan)
        self.assertIn(self.salesperson, self.commission_plan.user_ids)

    def test_invalid_range_constraints(self):
        """Test that invalid ranges raise ValidationError."""
        with self.assertRaises(ValidationError):
            self.env['sales.commission.plan.line'].create({
                'plan_id': self.commission_plan.id,
                'amount_from': 1000.0,
                'amount_to': 500.0,
                'rate': 15.0,
            })



