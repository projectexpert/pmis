# -*- coding: utf-8 -*-
# Copyright 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.change_management.tests import test_changes


class TestChangeManagementOwnProject(
        test_changes.TestChanges):

    def setUp(cls):
        super(TestChangeManagementOwnProject, cls).setUp()

    def test_change_project(cls):
        cls.test_change_id.button_create_change_project()
        ch_project = cls.test_change_id.change_project_id
        cls.assertEqual(
            ch_project.parent_id,
            cls.test_project_id.analytic_account_id, "Bad parent project")
