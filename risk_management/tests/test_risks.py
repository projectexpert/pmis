# __author__ = 'valdec'

from openerp.tests import common


class TestRisks(common.TransactionCase):

    def setup(self):

        """***setup risk tests***"""
        super(TestRisks, self).setup()
        cr, uid, = self.cr, self.uid

        self.risk_model = self.registry('risk.management.risk')
        self.project_model = self.registry('project.project')
        self.task_model = self.registry('project.task')
        self.user_model = self.registry('res.users')

        self.test_project_id = self.project_model.create(cr, uid, {
            'name': 'RiskTestProject'
        })
        self.risk_owner_id = self.user_model.search(
            cr, uid, [('name', '=', 'Demo User')]
        )[0]
        self.risk_author_id = self.user_model.search(
            cr, uid, [('name', '=', 'Risk User')]
        )[0]
        self.risk_second_author_id = self.user_model.search(
            cr, uid, [('login', '=', 'riskmanager')]
        )[0]

        self.test_risk_id = self.risk_model.create(
            cr, uid, {
                'name': 'RiskTest0001',
                'description': 'TestRisk_SkyFallsIn',
                'risk_category_id': 1,
                'project_id': self.test_project_id,
                'author_id': self.risk_author_id,
                'risk_owner_id': self.risk_owner_id
            }
        )

    def test_risk_owner_and_creator_added_to_followers_for_risk(self):
        cr, uid = self.cr, self.uid
        risk = self.risk_model.browse(cr, uid, self.test_risk_id)
        followers = [follower.name for follower in risk.message_follower_ids]
        self.assertTrue(
            len(followers) == 3,
            msg='Expecting 3 followers - got:%s' % len(followers)
        )

        self.assertTrue(
            risk.author_id.name in followers,
            msg='Risk Author NOT in followers:%s' % risk.author_id.name
        )
        self.assertTrue(
            risk.risk_owner_id.name in followers,
            msg='Risk Owner NOT in followers:%s' % risk.risk_owner_id.name
        )
        self.assertEqual(
            'RiskTest0001', risk.name, msg='Risk name incorrect'
        )

    def test_saving_a_change_in_users_as_followers_works(self):
        cr, uid = self.cr, self.uid
        self.risk_model.write(
            cr, uid,
            [self.test_risk_id],
            {'author_id': self.risk_second_author_id}
        )
        risk = self.risk_model.browse(cr, uid, self.test_risk_id)
        followers = [follower.name for follower in risk.message_follower_ids]
        self.assertTrue(
            len(followers) == 4,
            msg='Expecting 4 followers - got:%s' % len(followers)
        )
        self.assertTrue(
            risk.author_id.name in followers,
            msg='Risk Author NOT in followers:%s' % risk.author_id.name
        )

    def test_adding_a_task_on_a_risk(self):
        cr, uid = self.cr, self.uid
        risk = self.risk_model.read(
            cr, uid, self.test_risk_id, ['message_follower_ids']
        )
        followers = risk['message_follower_ids']
        self.risk_model.write(
            cr,
            uid,
            [self.test_risk_id],
            {
                'risk_response_ids': [
                    [
                        0, False,
                        {
                            'remaining_hours': 0,
                            'priority': '2',
                            'stage_id': 1,
                            'planned_hours': 0,
                            'user_id': uid,
                            'name': 'My New Task',
                            'date_deadline': False,
                            'sequence': 10,
                            'date_end': False,
                            'date_start': False,
                            'child_ids': [
                                [6, False, []]
                            ],
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
                ]
            }
        )

        task_ids = self.risk_model.read(
            cr, uid, self.test_risk_id, ['risk_response_ids']
        )
        tasks = self.task_model.read(
            cr, uid, task_ids['risk_response_ids'], ['message_follower_ids']
        )
        for task in tasks:
            self.assertEqual(
                followers,
                task['message_follower_ids'],
                msg='Followers are not set on the associated action'
            )
