# -*- coding: utf-8 -*-
# © 2015 MATMOZ d.o.o. - Matjaž Mozetič
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class Project(models.Model):

    _inherit = 'project.project'

    notes = fields.Text('Notes')
    # project_scope_ids = fields.One2many(
    #     'project.scope',
    #     'project_id',
    # )
    project_outscope_ids = fields.One2many(
        'project.outscope',
        'project_id',
    )
    project_success_ids = fields.One2many(
        'project.success',
        'project_id'
    )
    # project_requirement_ids = fields.One2many(
    #     'project.requirement',
    #     'project_id'
    # )
    project_constraints_ids = fields.One2many(
        'project.constraints',
        'project_id',
    )


# class Project_scope(models.Model):
#     """Project Scope"""
#
#     _name = 'project.scope'
#     _description = __doc__
#
#     project_id = fields.Many2one('project.project', string='Projects')
#     scope = fields.Text(
#         'Scope',
#         help='''
# The scope is what the project contains or delivers (i.e. the
# products or services). When starting to plan the scope of the
# project think about the BIG PICTURE first! At this level it
# is best to concentrate on the major deliverables and not to
# get bogged down with detail.
# Examples of areas that could be examined and clarified
# include:
#
# * The type of deliverables that are in scope and out of scope
# * The major life-cycle processes that are in scope and out of
#    scope
# * The types of data that are in scope and out of scope
# * The data sources that are in scope or out of scope
# * The organisations that are in scope and out of scope
# * The major functionality that is in scope and out of scope
#         '''
#     )


class ProjectOutscope(models.Model):
    """Out of scope"""

    _name = 'project.outscope'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    out_scope = fields.Text(
        'Out of Scope',
        help='''
It is just as important to agree on what is OUT OF SCOPE as it
is to define what is IN SCOPE as stakeholders will often have
different ideas regarding what is supposed to be IN the
project and what IS NOT. Obtain agreement up front to avoid
unnecessary disputes later on.
This is a useful task to conduct with key stakeholders and
can help clarify issues at any time in the Initiation or
Planning Phases.
Examples of areas that could be examined and clarified
include:

* The type of deliverables that are in scope and out of scope
* The major life-cycle processes that are in scope and out of
   scope
* The types of data that are in scope and out of scope
* The data sources that are in scope or out of scope
* The organisations that are in scope and out of scope
* The major functionality that is in scope and out of scope
        '''
    )


class Success(models.Model):
    """Success"""

    _name = 'project.success'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    success = fields.Text(
        'Criteria',
        help='''
PROJECT OBJECTIVES
The success of your project will be defined by how well you
meet your objectives. The more explicitly you state your
objectives at the outset, the less disagreement there will
be at the end about whether you have met them. Remember
that at this early stage of the project, there are still
many “unknown factors”. Be prepared to revise your
objectives as you gather more information about what you
need to achieve.

WRITING PROJECT OBJECTIVES
Project objectives are concrete statements that describe
what the project is trying to achieve. Objectives should
be developed for time, cost, quality (or functionality)
and should:

* Be aligned to business objectives
* Be measurable
* Be achievable
* Be consistent
* Be readily understandable
* Be few in number
* Have the full support and commitment of key stakeholders

Examples:
* Maximum Deadline on ...
* Maximum Budget = ...
        '''
    )


# class Requirement(models.Model):
#     """Requirements"""
#
#     _name = 'project.requirement'
#     _description = __doc__
#
#     project_id = fields.Many2one('project.project', string='Projects')
#     partner_id = fields.Many2one(
#         'project.hr.stakeholder', string='Stakeholder'
#     )
#     issue_id = fields.Many2one('project.issue', string='Negotiation')
#     status = fields.Selection(
#         [('draft', 'Draft'), ('approved', 'Approved'), ('denied', 'Denied')],
#         'Status',
#     )

# REQUIREMENTS COMMENTED OUT - REQ. MANAGEMENT TRANSFERED TO CHANGE MANAGEMENT

#     requirements = fields.Text(
#         'Stakeholder Requirements',
#         help='''
# The user requirements of the project must be defined and
# documented. Approval and confirmation must be obtained
# before the project can proceed. To obtain agreement about
# needs:
#
# * Separate needs from wants
# * Group the needs that are similar
# * Prioritise needs (eg essential, nice to have)
# * Identify any conflicting needs
# * Negotiate agreement between stakeholders with
#    conflicting needs
#
# This process often requires a number of meetings with
# stakeholders. Stakeholders often express their needs in
# terms of a particular product or solution to the problem,
# which has created the need for the project in the first
# place. It is important to re-state the agreed needs in
# terms of “what the end product/service(s) of the project
# should do”.
# Stating the agreed needs in functional terms permits the
# project manager to offer a range of solutions to the client
# or key stakeholders. If the project outcomes are restricted
# to solutions offered by key stakeholders too early in the
# analysis process important alternative options might be
# overlooked. Document the final set of agreed requirements
# and obtain sign-off from all key stakeholders.
#         '''
#     )


class ProjectConstraint(models.Model):
    """Constraints"""

    _name = 'project.constraints'
    _description = __doc__

    project_id = fields.Many2one('project.project', string='Projects')
    constraints = fields.Text(
        string='Constraints',
        help='''
Project constraints are known facts that will influence how
the project is planned and managed. A constraint is a given
factor that is outside of the project planner’s scope of
control, which unless it is lifted or otherwise removed, will
force project actions to work around it.
        '''
    )
