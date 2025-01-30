import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-akretion-business_intelligence_fields",
    description="Meta package for akretion-business_intelligence_fields Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-bi_invoice_company_currency',
        'odoo12-addon-bi_purchase_company_currency',
        'odoo12-addon-bi_sale_company_currency',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
