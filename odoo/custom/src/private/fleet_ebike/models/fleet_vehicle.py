# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    battery_ids = fields.One2many(
        comodel_name="fleet.battery",
        inverse_name="vehicle_id",
    )
    vehicle_move_ids = fields.One2many(
        comodel_name="fleet.vehicle.move",
        inverse_name="vehicle_id",
    )
    move_count = fields.Integer(
        compute="_compute_vehicle_move",
        store=True,
    )

    @api.depends("vehicle_move_ids")
    def _compute_vehicle_move(self):
        for rec in self:
            rec.update(
                {
                    "move_count": len(rec.vehicle_move_ids),
                }
            )

    def return_ebike_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get("xml_id")
        if xml_id:
            res = self.env["ir.actions.act_window"]._for_xml_id(
                "fleet_ebike.%s" % xml_id
            )
            res.update(
                context=dict(
                    self.env.context, default_vehicle_id=self.id, group_by=False
                ),
                domain=[("vehicle_id", "=", self.id)],
            )
            return res
        return False


class FleetVehicleMove(models.Model):
    _name = "fleet.vehicle.move"
    _description = "Vehicle Movement"
    _order = "date_stamp desc"

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        index=True,
    )
    date_stamp = fields.Datetime(default=fields.Datetime.now)
    latitude = fields.Float("Latitude", digits=(16, 5))
    longitude = fields.Float("Geo Longitude", digits=(16, 5))
    speed = fields.Float("Speed (km/h)")
