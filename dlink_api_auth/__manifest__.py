# Copyright 2019 Anvar Kildebekov <https://it-projects.info/team/fedoranvar>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": """DLink Api Auth""",
    "summary": """DLink Authentications for Odoo""",
    "category": "api",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version=13.0",
    "version": "1.0.0",
    "application": True,
    "author": "Arian Camejo Carrera",
    "support": "acarrera0897@gmail.com",
    "website": "",
    "license": "LGPL-3",
    "depends": ['base', 'dlink_api_utils'],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'security/ir.model.access.csv',
    ],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
    # "demo_title": "Api Auth",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "basic function and methods of API for openapi or XML-RPC",
    # "demo_images": [
    #    "images/MAIN_IMAGE",
    # ]
}
