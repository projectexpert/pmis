# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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

from datetime import datetime, date, timedelta
from openerp.tools.translate import _
from openerp.osv import fields, osv
from dijkstra import shortestPath
from itertools import count
from dateutil.rrule import rrule
from dateutil.rrule import DAILY, MO, TU, WE, TH, FR, HOURLY
import logging


_logger = logging.getLogger(__name__)


class task(osv.osv):
    _inherit = 'project.task'
    _description = "Activity"

    _columns = {
        'duration': fields.integer(
            'Activity duration', help='Duration in calendar hours'
        ),
        'date_early_start': fields.datetime(
            'Early Start Date', select=True
        ),
        'date_early_finish': fields.datetime(
            'Early Finish Date', select=True
        ),
        'date_late_start': fields.datetime(
            'Late Start Date', select=True
        ),
        'date_late_finish': fields.datetime(
            'Late Finish Date', select=True
        ),
        'is_critical_path': fields.boolean(
            'Critical Path'
        ),
        'date_earliest_start': fields.datetime(
            'Earliest Start Date', select=True
        ),
        'date_latest_finish': fields.datetime(
            'Latest Finish Date', select=True
        ),
        'total_float': fields.integer(
            'Total float',
            help='''
Number of hours that the activity can be delayed without delaying the project.
            '''
        ),
        'free_float': fields.integer(
            'Free float',
            help='''
Number of hours that the activity can be delayed without delaying the next
subsequent activity.
            '''
        ),
    }

    def onchange_duration(self, cr, uid, ids, duration):
        result = {}

        if duration < 0:
            raise osv.except_osv(
                _('Error'),
                _("The task duration cannot be set to a value less than zero.")
            )

        return result

    def get_network(self, cr, uid, ids, d_activities, *args):

        read_data = []
        read_data = self.read(
            cr,
            uid,
            ids[0],
            [
                'duration', 'child_ids', 'parent_ids', 'date_earliest_start',
                'date_latest_finish', 'date_start', 'date_end', 'stage_id'
            ]
        )
        task_stage_obj = self.pool.get('project.task.type')
        closed = True
        if read_data['stage_id']:
            stage_data = task_stage_obj.read(
                cr, uid, read_data['stage_id'][0], ['fold']
            )
            closed = stage_data['fold']

        if closed:
            replan_duration = 0
        else:
            replan_duration = read_data['duration']

        child_ids = read_data['child_ids']
        parent_ids = read_data['parent_ids']

        # If task has started we consider it a start restriction

        if read_data['date_end'] and closed:
            date_earliest_start = read_data['date_end']
        else:
            date_earliest_start = read_data['date_earliest_start']

        # If task has finish we consider it a finish restriction
        if read_data['date_end'] and closed:
            date_latest_finish = read_data['date_end']
        else:
            date_latest_finish = read_data['date_latest_finish']

        d_activities[ids[0]] = network_activity(
            ids[0], replan_duration, date_earliest_start, date_latest_finish
        )

        if not child_ids:
            d_activities[ids[0]].add_successor(d_activities['stop'])
            d_activities['stop'].add_predecessor(d_activities[ids[0]])

        if not parent_ids:
            d_activities[ids[0]].add_predecessor(d_activities['start'])
            d_activities['start'].add_successor(d_activities[ids[0]])

        for child_id in child_ids:
            if child_id in d_activities:
                pass
            else:
                lchild_id = []
                lchild_id.append(child_id)
                d_activities.update(
                    self.get_network(
                        cr, uid, lchild_id, d_activities
                    )
                )

            d_activities[ids[0]].add_successor(d_activities[child_id])

        for parent_id in parent_ids:
            if parent_id in d_activities:
                pass
            else:
                lparent_id = []
                lparent_id.append(parent_id)
                d_activities.update(
                    self.get_network(
                        cr, uid, lparent_id, d_activities
                    )
                )

            d_activities[ids[0]].add_predecessor(d_activities[parent_id])

        return d_activities

    def calculate_network(self, cr, uid, ids, context, *args):

        d_activities = {}
        d_activities['start'] = network_activity(None, 0, None, None)
        d_activities['start'].is_start = True
        d_activities['start'].activity_id = 'start'
        d_activities['stop'] = network_activity(None, 0, None, None)
        d_activities['stop'].is_stop = True
        d_activities['stop'].activity_id = 'stop'

        d_activities = self.get_network(cr, uid, ids, d_activities)

        self.get_critical_activities(d_activities)
        self.update_tasks(cr, uid, ids, d_activities)

    def get_critical_activities(self, d_activities):
        # warning = {}

        # Read the activity details
        activities = d_activities.values()

        for start_activity in activities:
            if start_activity.is_start:
                break

        l_successor_date_earliest_start = []
        for successor in start_activity.successors:
            if successor.date_earliest_start:
                l_successor_date_earliest_start.append(
                    successor.date_earliest_start
                )

        if l_successor_date_earliest_start:
            start_activity.date_early_start = min(
                l_successor_date_earliest_start
            )
        else:
            start_activity.date_early_start = network_activity.next_work_day(
                datetime.today()
            )

        network_activity.walk_list_ahead(start_activity)

        for stop_activity in activities:
            if stop_activity.is_stop:
                break

        stop_activity.date_late_finish = stop_activity.date_early_finish

        stop_activity.date_late_start = network_activity.sub_work_days(
            stop_activity.date_late_finish, stop_activity.replan_duration
        )

        network_activity.walk_list_aback(stop_activity)

        start_activity.date_late_finish = start_activity.date_early_finish
        start_activity.date_late_start = network_activity.sub_work_days(
            start_activity.date_late_finish, start_activity.replan_duration
        )

        # Calculate Float
        for act in activities:

            l_successor_date_early_start = []
            for successor in act.successors:
                l_successor_date_early_start.append(successor.date_early_start)
            if l_successor_date_early_start:
                [act.free_float, rr] = network_activity.work_days_diff(
                    act.date_early_finish, min(l_successor_date_early_start)
                )
            [act.total_float, rr] = network_activity.work_days_diff(
                act.date_early_start, act.date_late_start
            )

        # Calculate shortest path
        C_INFINITE = 9999
        d_graph = {}
        for act in d_activities.keys():
            d_neighbours = {}
            for other_act in d_activities.keys():
                if other_act != act:
                    d_neighbours[other_act] = C_INFINITE
                    for pred_act in d_activities[act].predecessors:
                        if other_act == pred_act.activity_id:
                            d_neighbours[other_act] = pred_act.total_float
                    for succ_act in d_activities[act].successors:
                        if other_act == succ_act.activity_id:
                            d_neighbours[other_act] = succ_act.total_float
            d_graph[act] = d_neighbours

        l_spath = []
        try:
            l_spath = shortestPath(d_graph, 'start', 'stop')
        except Exception:
            _logger.warning(
                """Could not calculate the critical path due to existing negative floats
                in one or more of the network activities."""
            )

        for act in activities:
            item = next((i for i in l_spath if i == act.activity_id), None)
            if item is not None:
                act.is_critical_path = True

    def update_tasks(self, cr, uid, ids, d_activities, context=None):
        if context is None:
            context = {}
        task_obj = self.pool.get('project.task')
        context.update({'calculate_network': True})
        for task_id in d_activities.keys():
            if (not task_id == 'start') and (not task_id == 'stop'):
                task_obj.write(cr, uid, task_id, {
                    'date_early_start': d_activities[
                        task_id].date_early_start,
                    'date_early_finish': d_activities[
                        task_id].date_early_finish,
                    'date_late_start': d_activities[
                        task_id].date_late_start,
                    'date_late_finish': d_activities[
                        task_id].date_late_finish,
                    'is_critical_path': d_activities[
                        task_id].is_critical_path,
                    'total_float': d_activities[
                        task_id].total_float,
                    'free_float': d_activities[
                        task_id].free_float,
                }, context=context)

    def create(self, cr, uid, vals, context=None):
        res = super(task, self).create(cr, uid, vals, context)
        self.calculate_network(cr, uid, [res], context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        res = super(task, self).write(cr, uid, ids, vals, context)
        if not context.get('calculate_network') and ids and (
            vals.get('duration') or
            vals.get('stage_id') or
            vals.get('date_latest_finish') or
            vals.get('date_earliest_start') or
            vals.get('parent_ids') or
            vals.get('child_ids')
        ):
            if not isinstance(ids, list):
                ids = [ids]
            self.calculate_network(cr, uid, ids, context)
        return res

task()


class network_activity(object):
    'Activity in network diagram'

    def __init__(
        self, activity_id, duration, date_earliest_start, date_latest_finish
    ):

        # DATE_FORMAT = "%Y-%m-%d"
        DATE_INIT = datetime(1900, 01, 01, 9, 0)

        self.activity_id = activity_id

        self.replan_duration = int(duration)
        self.total_duration = int(duration)

        if date_earliest_start:
            self.date_earliest_start = datetime.strptime(
                date_earliest_start, "%Y-%m-%d %H:%M:%S"
            )
        else:
            self.date_earliest_start = None

        if date_latest_finish:
            self.date_latest_finish = datetime.strptime(
                date_latest_finish, "%Y-%m-%d %H:%M:%S"
            )
        else:
            self.date_latest_finish = None

        self.date_early_start = DATE_INIT
        self.date_early_finish = DATE_INIT
        self.date_late_start = DATE_INIT
        self.date_late_finish = DATE_INIT

        self.total_float = timedelta(days=0)
        self.free_float = timedelta(days=0)

        self.is_start = False
        self.is_stop = False
        self.is_critical_path = False
        self.successors = []
        self.predecessors = []

    @staticmethod
    def work_days(dtstart, until):

        work_days = count(
            rrule(
                DAILY,
                byweekday=(MO, TU, WE, TH, FR),
                dtstart=date,
                until=until
            )
        )
        return work_days

    @staticmethod
    def work_days_diff(start_date, end_date):
        if end_date > start_date:
            rr = rrule(
                HOURLY,
                byweekday=(MO, TU, WE, TH, FR),
                byhour=range(9, 17),
                dtstart=start_date,
                until=end_date
            )
            return [rr.count(), rr]
        elif start_date > end_date:
            rr = rrule(
                HOURLY,
                byweekday=(MO, TU, WE, TH, FR),
                byhour=range(9, 17),
                dtstart=end_date,
                until=start_date
            )
            return [-(rr.count()), rr]
        else:
            return [0, None]

    @staticmethod
    def next_work_day(date):
        rr = rrule(
            HOURLY,
            byweekday=(MO, TU, WE, TH, FR),
            byhour=range(9, 17),
            dtstart=date
        )
        return rr.after(date, inc=True)

    @staticmethod
    def add_work_days(date, duration):
        if duration:
            l_days = []
            l_days = list(
                rrule(
                    HOURLY,
                    count=duration + 1,
                    byweekday=(MO, TU, WE, TH, FR),
                    byhour=range(9, 17),
                    dtstart=date
                )
            )
            return l_days[-1]
        else:
            return date

    @staticmethod
    def sub_work_days(date, duration):
        DATE_INIT = date - timedelta(hours=duration)
        if duration:
            correct_date_init = False
            while correct_date_init is False:
                [rr_count, rr] = network_activity.work_days_diff(
                    DATE_INIT, date
                )
                if rr_count < duration:
                    DATE_INIT -= timedelta(hours=duration + 1 - rr_count)
                else:
                    correct_date_init = True
            l_days = list(rr)
            return l_days[0]
        else:
            return date

    def add_successor(self, activity):
        self.successors.append(activity)

    def add_predecessor(self, activity):
        self.predecessors.append(activity)

    @staticmethod
    def walk_list_ahead(position):

        # Start No Earlier Than Milestone
        # A "Start No Earlier Than" milestone fixes the start of an activity
        #   to begin no earlier than the date provided.
        # The start milestone's impact is on the forward pass only.
        # When the activity with the start milestone is reached in the forward
        #   pass, then the milestone date is considered in the calculation.
        # If the milestone start date is later than the calculated early start
        #   date, then the milestone date is substituted for the calculated
        #   early start date.
        # If the calculated date is later than the early start date, then the
        #   calculated date is used.

        if position.date_earliest_start:
            position.date_early_start = position.date_earliest_start

        if position.is_start:
            position.date_early_finish = network_activity.add_work_days(
                position.date_early_start, position.replan_duration
            )

        # Earliest start of successor task = Latest of the early finish dates
        #   of all predecessors
        for successor in position.successors:

            if successor.date_earliest_start:
                successor.date_early_start = successor.date_earliest_start

            for predecessor in successor.predecessors:
                if successor.date_early_start < predecessor.date_early_finish:

                    successor.date_early_start = predecessor.date_early_finish

            successor.date_early_finish = network_activity.add_work_days(
                successor.date_early_start, successor.replan_duration
            )

        for successor in position.successors:
            network_activity.walk_list_ahead(successor)

    @staticmethod
    def walk_list_aback(activity):

        DATE_INIT = datetime(1900, 01, 01, 9, 0)

        if activity.date_latest_finish:
            if activity.date_late_finish > activity.date_latest_finish:
                activity.date_late_finish = activity.date_latest_finish

        if activity.is_stop:
            activity.date_late_start = network_activity.sub_work_days(
                activity.date_late_finish, activity.replan_duration
            )

        # In calculating backward through the finish-to-start network,
        # we use the earliest of the "latest start" dates of a successor task
        # as the latest finish for a predecessor task
        for predecessor in activity.predecessors:
            if predecessor.date_latest_finish:
                predecessor.date_late_finish = predecessor.date_latest_finish

            for successor in predecessor.successors:
                if predecessor.date_late_finish <= DATE_INIT:
                    predecessor.date_late_finish = successor.date_late_start
                elif predecessor.date_late_finish > successor.date_late_start:
                    predecessor.date_late_finish = successor.date_late_start

            predecessor.date_late_start = network_activity.sub_work_days(
                predecessor.date_late_finish, predecessor.replan_duration
            )

        for predecessor in activity.predecessors:
            network_activity.walk_list_aback(predecessor)
