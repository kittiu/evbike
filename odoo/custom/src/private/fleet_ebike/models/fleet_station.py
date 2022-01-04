# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetStation(models.Model):
    _name = "fleet.station"
    _description = "Battery Station"

    name = fields.Char(
        string="Station",
    )
    address = fields.Text(
        string="Address",
    )
    # image = fields.Image()
    # locker_ids = fields.One2many(
    #     comodel_name="fleet.station.locker",
    #     inverse_name="station_id",
    # )
    # locker_count = fields.Integer(
    #     compute="_compute_locker",
    #     store=True,
    # )
    # state = fields.Selection(
    #     selection=[
    #         ("inactive", "Inactive"),
    #         ("active", "Active"),
    #     ],
    #     string="Status",
    #     tracking=True,
    # )

    # @api.depends("locker_ids")
    # def _compute_locker(self):
    #     for rec in self:
    #         rec.update({
    #             "locker_count": len(rec.locker_ids),
    #         })


class FleetStationLocker(models.Model):
    _name = "fleet.station.locker"
    _description = "Battery Locker"

    # station_id = fields.Many2one(
    #     comodel_name="fleet.station",
    #     index=True,
    # )
    name = fields.Char(
        string="Locker",
    )
    # battery_ids = fields.One2many(
    #     comodel_name="fleet.battery",
    #     inverse_name="locker_id",
    # )
    # charging = fields.Boolean(
    #     compute="_compute_charging",
    # )
    # state = fields.Selection(
    #     selection=[
    #         ("inactive", "Inactive"),
    #         ("inuse", "Inuse"),
    #         ("broken", "Broken"),
    #     ],
    #     string="Status",
    #     tracking=True,
    # )

    # def _compute_charging(self):
    #     for rec in self:
    #         rec.charging = len(rec.battery_ids) > 1
