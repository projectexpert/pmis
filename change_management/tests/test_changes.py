# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Enterprise Management Solution
#
#    Copyright (C) 2015 Matmoz d.o.o. (<http://www.matmoz.si>).
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
##############################################################################
from openerp.tests import common


class TestChanges(common.TransactionCase):

    def setup(self):

        """***setup change tests***"""
        super(TestChanges, self).setup()
        cr, uid, = self.cr, self.uid

        self.change_model = self.registry('change.management.change')
        self.project_model = self.registry('project.project')
        self.task_model = self.registry('project.task')
        self.user_model = self.registry('res.users')

        self.test_project_id = self.project_model.create(
            cr, uid, {'name': 'ChangeTestProject'}
        )
        self.change_owner_id = self.user_model.search(
            cr, uid, [('name', '=', 'Demo User')])[0]
        self.change_author_id = self.user_model.search(
            cr, uid, [('name', '=', 'Change User')])[0]
        self.change_second_author_id = self.user_model.search(
            cr, uid, [('login', '=', 'changemanager')])[0]

        self.test_change_id = self.change_model.create(
            cr, uid, {
                'name': 'ChangeTest0001',
                'description': 'TestChange_SkyPaintBlue',
                'change_category_id': 1,
                'project_id': self.test_project_id,
                'author_id': self.change_author_id,
                'change_owner_id': self.change_owner_id
            }
        )

    def test_change_owner_and_creator_added_to_followers_for_change(self):
        cr, uid = self.cr, self.uid
        change = self.change_model.browse(cr, uid, self.test_change_id)
        followers = [follower.name for follower in change.message_follower_ids]
        self.assertTrue(
            len(followers) == 3, msg='Expecting 3 followers - got:%s' % len(
                followers
            )
        )

        self.assertTrue(
            change.author_id.name in followers,
            msg='Change Author NOT in followers:%s' % change.author_id.name
        )
        self.assertTrue(
            change.change_owner_id.name in followers,
            msg='''
            Change Owner NOT in followers:%s
            ''' % change.change_owner_id.name
        )
        self.assertEqual(
            'ChangeTest0001', change.name, msg='Change name incorrect'
        )

    def test_saving_a_change_in_users_as_followers_works(self):
        cr, uid = self.cr, self.uid
        self.change_model.write(
            cr, uid, [self.test_change_id],
            {'author_id': self.change_second_author_id}
        )
        change = self.change_model.browse(cr, uid, self.test_change_id)
        followers = [follower.name for follower in change.message_follower_ids]
        self.assertTrue(
            len(followers) == 4,
            msg='Expecting 4 followers - got:%s' % len(followers)
        )
        self.assertTrue(
            change.author_id.name in followers,
            msg='Change Author NOT in followers:%s' % change.change_id.name
        )

    def test_adding_a_task_on_a_change(self):
        cr, uid = self.cr, self.uid
        change = self.change_model.read(
            cr, uid, self.test_change_id, ['message_follower_ids']
        )
        followers = change['message_follower_ids']
        self.change_model.write(
            cr, uid, [self.test_change_id],
            {'change_response_ids': [
                [0, False,
                 {'remaining_hours': 0,
                  'priority': '2',
                  'stage_id': 1,
                  'planned_hours': 0,
                  'user_id': uid,
                  'name': 'My New Task',
                  'date_deadline': False,
                  'sequence': 10,
                  'date_end': False,
                  'date_start': False,
                  'child_ids': [[6, False, []]],
                  'company_id': 1,
                  'work_ids': [],
                  'parent_ids': [[6, False, []]],
                  'message_follower_ids': followers,
                  'categ_ids': [[6, False, []]],
                  'project_id': 1,
                  'partner_id': False,
                  'message_ids': False,
                  'description': 'A new Task'
                  }
                 ]
            ]}
        )

        task_ids = self.change_model.read(
            cr, uid, self.test_change_id, ['change_response_ids']
        )
        tasks = self.task_model.read(
            cr, uid, task_ids['change_response_ids'], ['message_follower_ids']
        )
        for task in tasks:
            self.assertEqual(
                followers,
                task['message_follower_ids'],
                msg='Followers are not set on the associated action'
            )
