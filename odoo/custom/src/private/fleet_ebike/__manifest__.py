# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Fleet Ebike",
    "version": "14.0.1.0.0",
    "category": "Fleet Ebike",
    "license": "AGPL-3",
    "author": "Ecosoft,Odoo Community Association (OCA)",
    # "website": "https://github.com/OCA/partner-contact",
    "depends": ["fleet"],
    "data": [
        "views/fleet_battery_views.xml",
        "views/fleet_vehicle_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
