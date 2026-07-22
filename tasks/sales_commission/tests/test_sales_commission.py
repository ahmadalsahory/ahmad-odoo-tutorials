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
        """Test getting commission rate for different net sales amounts including gaps."""
        plan = self.env['sales.commission.plan'].create({
            'name': 'Gap Test Plan',
            'line_ids': [
                (0, 0, {'amount_from': 1000.0, 'amount_to': 5000.0, 'rate': 10.0}),
                (0, 0, {'amount_from': 10000.0, 'amount_to': 20000.0, 'rate': 20.0}),
            ]
        })

        # Below lowest tier ($500) -> 0.0%
        self.assertEqual(plan.get_commission_rate(500.0), 0.0, "Rate below lowest tier should be 0%")

        # Direct match inside tier 1 ($3000) -> 10.0%
        self.assertEqual(plan.get_commission_rate(3000.0), 10.0, "Rate for $3000 should be 10%")

        # Gap between tier 1 and tier 2 ($7000) -> lower tier rate (10.0%)
        self.assertEqual(plan.get_commission_rate(7000.0), 10.0, "Rate for $7000 in gap should fall back to tier 1 rate 10%")

        # Direct match inside tier 2 ($15000) -> 20.0%
        self.assertEqual(plan.get_commission_rate(15000.0), 20.0, "Rate for $15000 should be 20%")

        # Exceeding max tier ($25000) -> highest tier rate (20.0%)
        self.assertEqual(plan.get_commission_rate(25000.0), 20.0, "Exceeding max tier should return highest tier rate 20%")

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

    def test_overlapping_range_constraints(self):
        """Test that overlapping ranges or shared exact boundaries raise ValidationError."""
        with self.assertRaises(ValidationError):
            self.env['sales.commission.plan.line'].create({
                'plan_id': self.commission_plan.id,
                'amount_from': 5000.0,
                'amount_to': 10000.0,
                'rate': 25.0,
            })

        with self.assertRaises(ValidationError):
            self.env['sales.commission.plan.line'].create({
                'plan_id': self.commission_plan.id,
                'amount_from': 500.0,
                'amount_to': 800.0,
                'rate': 15.0,
            })

    def test_report_wizard_plan_id(self):
        """Test that commission report lines properly link the salesperson's commission plan."""
        wizard = self.env['sales.commission.report.wizard'].create({
            'date_from': '2026-01-01',
            'date_to': '2026-12-31',
            'user_ids': [(4, self.salesperson.id)],
        })
        wizard.action_generate_report()
        self.assertEqual(len(wizard.line_ids), 1)
        self.assertEqual(wizard.line_ids.plan_id, self.commission_plan)
