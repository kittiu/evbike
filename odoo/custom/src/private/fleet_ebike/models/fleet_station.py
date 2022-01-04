# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetStation(models.Model):
    _name = "fleet.station"
    _description = "Battery Station"

    name = fields.Char(
        string="Station",
    )
    address = fields.Text(
        string="Location",
    )
    image = fields.Image()
    locker_ids = fields.One2many(
        comodel_name="fleet.station.locker",
        inverse_name="station_id",
    )
    locker_count = fields.Integer(
        compute="_compute_locker",
        store=True,
    )
    state = fields.Selection(
        selection=[
            ("inactive", "Inactive"),
            ("active", "Active"),
        ],
        string="Status",
        default="inactive",
    )

    @api.depends("locker_ids")
    def _compute_locker(self):
        for rec in self:
            rec.update(
                {
                    "locker_count": len(rec.locker_ids),
                }
            )


class FleetStationLocker(models.Model):
    _name = "fleet.station.locker"
    _description = "Battery Locker"

    station_id = fields.Many2one(
        comodel_name="fleet.station",
        index=True,
    )
    name = fields.Char(
        string="Locker",
        required=True,
    )
    battery_ids = fields.One2many(
        comodel_name="fleet.battery",
        inverse_name="locker_id",
    )
    battery_id = fields.Many2one(
        comodel_name="fleet.battery",
        compute="_compute_battery",
        string="Battery S/N",
    )
    battery_soc = fields.Float(
        related="battery_id.soc",
    )
    charging = fields.Boolean(
        compute="_compute_battery",
    )

    def _compute_battery(self):
        for rec in self:
            rec.charging = len(rec.battery_ids) > 0
            rec.battery_id = rec.battery_ids[:1]
