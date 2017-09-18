# Copyright 2017 Matmoz d.o.o. (<http://www.matmoz.si>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestChanges(common.TransactionCase):

    def setUp(self):

        """***setup change tests***"""
        super(TestChanges, self).setUp()

        self.change_model = self.env['change.management.change']
        self.project_model = self.env['project.project']
        self.task_model = self.env['project.task']
        self.user_model = self.env['res.users']

        self.test_project_id = self.project_model.create(
            {'name': 'ChangeTestProject'}
        )
        self.change_owner_id = self.user_model.search(
            [('name', '=', 'Demo User')])[0]
        self.change_author_id = self.user_model.search(
            [('name', '=', 'Change User')])[0]
        self.change_second_author_id = self.user_model.search(
            [('login', '=', 'changemanager')])[0]

        self.test_change_id = self.change_model.create({
            'name': 'ChangeTest0001',
            'description': 'TestChange_SkyPaintBlue',
            'change_category_id': 1,
            'project_id': self.test_project_id.id,
            'author_id': self.change_author_id.id,
            'change_owner_id': self.change_owner_id.id
        })

    def test_change_owner_and_creator_added_to_followers_for_change(self):
        change = self.test_change_id
        followers = [follower.id for follower in change.message_follower_ids]
        self.assertTrue(
            len(followers) == 1,
            msg='Expecting 3 followers - got:%s' % len(followers)
        )

    def test_saving_a_change_in_users_as_followers_works(self):
        self.test_change_id.write(
            {'author_id': self.change_second_author_id.id}
        )
        change = self.test_change_id
        followers = [follower.id for follower in change.message_follower_ids]
        self.assertTrue(
            len(followers) == 2,
            msg='Expecting 4 followers - got:%s' % len(followers)
        )

    def test_adding_a_task_on_a_change(self):
        change = self.test_change_id.read(['message_follower_ids'])
        followers = self.env['mail.followers'
                             ].browse(change[0]['message_follower_ids'])
        self.test_change_id.write({
            'change_response_ids': [(0, 0,
                                     {'remaining_hours': 0,
                                      'stage_id': 1,
                                      'planned_hours': 0,
                                      'user_id': self.uid,
                                      'name': 'My New Task',
                                      'date_deadline': False,
                                      'sequence': 10,
                                      'date_end': False,
                                      'date_start': False,
                                      'company_id': 1,
                                      'message_follower_ids':
                                      [(4, followers.id)],
                                      'project_id': 1,
                                      'partner_id': False,
                                      'message_ids': False,
                                      'description': 'A new Task'})]
        })
        self.assertNotEqual(
            followers,
            self.test_change_id.change_response_ids[0].message_follower_ids,
            msg='Followers are not set on the associated action'
        )
