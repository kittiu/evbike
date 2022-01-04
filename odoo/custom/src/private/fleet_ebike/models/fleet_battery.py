# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetBattery(models.Model):
    _name = "fleet.battery"
    _description = "Battery"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="S/N",
    )
    model = fields.Char(
        string="Model",
    )
    date_start = fields.Date(
        string="Start Date",
    )
    state = fields.Selection(
        selection=[
            ("inactive", "Inactive"),
            ("charging", "Charging"),
            ("inuse", "In-Use"),
        ],
        string="Status",
        compute="_compute_battery_move",
        store=True,
        tracking=True,
    )
    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        compute="_compute_battery_move",
        store=True,
    )
    locker_id = fields.Many2one(
        comodel_name="fleet.station.locker",
        compute="_compute_battery_move",
        store=True,
    )
    battery_move_ids = fields.One2many(
        comodel_name="fleet.battery.move",
        inverse_name="battery_id",
    )
    move_count = fields.Integer(
        compute="_compute_battery_move",
        store=True,
    )
    charging_cycle = fields.Integer(
        string="Charging Cycle",
        compute="_compute_battery_move",
        store=True,
    )
    soh = fields.Float(
        string="State of Health",
        compute="_compute_battery_soh",
        store=True,
        help="Health of battery, 0-100",
    )
    soh_count = fields.Integer(
        compute="_compute_battery_soh",
        store=True,
    )
    battery_soh_ids = fields.One2many(
        comodel_name="fleet.battery.soh",
        inverse_name="battery_id",
    )
    soc = fields.Float(
        string="State of Charge",
        compute="_compute_battery_soc",
        store=True,
        help="Charging status of batther, 0-100",
    )
    soc_count = fields.Integer(
        compute="_compute_battery_soc",
        store=True,
    )
    battery_soc_ids = fields.One2many(
        comodel_name="fleet.battery.soc",
        inverse_name="battery_id",
    )

    @api.depends("battery_move_ids")
    def _compute_battery_move(self):
        for rec in self:
            battery_move = rec.battery_move_ids[:1]
            state = "inactive"
            if battery_move.vehicle_id:
                state = "inuse"
            elif battery_move.locker_id:
                state = "charging"
            rec.update(
                {
                    "vehicle_id": battery_move.vehicle_id.id,
                    "locker_id": battery_move.locker_id.id,
                    "charging_cycle": len(rec.battery_move_ids.filtered("locker_id")),
                    "move_count": len(rec.battery_move_ids),
                    "state": state,
                }
            )

    @api.depends("battery_soh_ids")
    def _compute_battery_soh(self):
        for rec in self:
            battery_move = rec.battery_soh_ids[:1]
            rec.update(
                {
                    "soh": battery_move.soh,
                    "soh_count": len(rec.battery_soh_ids),
                }
            )

    @api.depends("battery_soc_ids")
    def _compute_battery_soc(self):
        for rec in self:
            battery_move = rec.battery_soc_ids[:1]
            rec.update(
                {
                    "soc": battery_move.soc,
                    "soc_count": len(rec.battery_soc_ids),
                }
            )

    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get("xml_id")
        if xml_id:

            res = self.env["ir.actions.act_window"]._for_xml_id(
                "fleet_ebike.%s" % xml_id
            )
            res.update(
                context=dict(
                    self.env.context, default_battery_id=self.id, group_by=False
                ),
                domain=[("battery_id", "=", self.id)],
            )
            return res
        return False


class FleetBatteryMove(models.Model):
    _name = "fleet.battery.move"
    _description = "Battery Movement"
    _order = "date_stamp desc"

    battery_id = fields.Many2one(
        comodel_name="fleet.battery",
        index=True,
    )
    date_stamp = fields.Datetime(default=fields.Datetime.now)
    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
    )
    locker_id = fields.Many2one(
        comodel_name="fleet.station.locker",
    )

    @api.onchange("vehicle_id")
    def _onchange_vehicle_id(self):
        self.locker_id = False

    @api.onchange("locker_id")
    def _onchange_locker_id(self):
        self.vehicle_id = False


class FleetBatterySOC(models.Model):
    _name = "fleet.battery.soc"
    _description = "Battery Charging Movement"
    _order = "date_stamp desc"

    battery_id = fields.Many2one(
        comodel_name="fleet.battery",
        index=True,
    )
    date_stamp = fields.Datetime(default=fields.Datetime.now)
    soc = fields.Float(
        string="State of Charge",
        group_operator="avg",
    )


class FleetBatterySOH(models.Model):
    _name = "fleet.battery.soh"
    _description = "Battery Health Movement"
    _order = "date_stamp desc"

    battery_id = fields.Many2one(
        comodel_name="fleet.battery",
        index=True,
    )
    date_stamp = fields.Datetime(default=fields.Datetime.now)
    soh = fields.Float(
        string="State of Health",
        group_operator="avg",
    )
