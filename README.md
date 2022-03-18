# bw_activity_replacement

Apply the activity replacement in brightway 2.

## Usage

Below you can find 3 examples that should compile properly if you have created a database called "Test" and imported the 'ecoinvent 3.8_cutoff_ecoSpold02' dataset.

```python
from market_penetration import perform_replacement

''' Methanol Example '''

config = {
    'db': 'ecoinvent 3.8_cutoff_ecoSpold02',
    'project': 'Test',
    'activities': ["('ecoinvent 3.8_cutoff_ecoSpold02', '0a0cd0ce99d930cc1a22a4b98a1cefe9')",  # market for methanol	methanol	GLO
                   ],
    'methods': ["('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Resources', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Human health', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Ecosystems', 'Aggregated', 'Egalitarian')",
                "('IPCC 2013', 'climate change', 'GWP 100a')"],
    'new activity': "('ecoinvent 3.8_cutoff_ecoSpold02', 'a8091dd717a1f179635d35cce1d6511c')", # methanol production, from synthetic gas	methanol, from biomass	RoW
    'reference product': ["methanol"],
    'folder': 'Methanol_from_Biomass',
    'level': 2,
    'n_top': 20
}


''' Spain Electricity Example '''
'''
config = {
    'db': 'ecoinvent 3.8_cutoff_ecoSpold02',
    'project': 'Test',
    'activities': ["('ecoinvent 3.8_cutoff_ecoSpold02', '473d4bb488e8f903b58203f3e5161636')",  # market for electricity, high voltage	electricity, high voltage	ES
                   ],
    'methods': ["('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Resources', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Human health', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Ecosystems', 'Aggregated', 'Egalitarian')",
                "('IPCC 2013', 'climate change', 'GWP 100a')"],
    'new activity': "('ecoinvent 3.8_cutoff_ecoSpold02', '306de5beb6b3f4f770057eceabcd7ae1')", # electricity production, solar thermal parabolic trough, 50 MW	electricity, high voltage	ES
    'reference product': ["electricity, high voltage"],
    'folder': 'Electricity_from_CSP_ES',
    'level': 2,
    'n_top': 20
}
'''

''' Diesel Example '''
'''
config = {
    'db': 'ecoinvent 3.8_cutoff_ecoSpold02',
    'project': 'Test',
    'activities': ["('ecoinvent 3.8_cutoff_ecoSpold02', 'd268c770c9a0de5ee694b8e3b9bcaf9a')",  # market for diesel, low-sulfur	diesel, low-sulfur	Europe without Switzerland
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '7b7a4924797fd35fcdd5882e002c43a6')",  # market for diesel, low-sulfur	diesel, low-sulfur	PE
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '9346ab267ad2c0ae46b0b02419d92e87')",  # market for diesel, low-sulfur	diesel, low-sulfur	IN
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '509afdd65aa82305d4a86c76dd7fe459'",  # market for diesel, low-sulfur	diesel, low-sulfur	CH
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '454563ec7c59b46d34ce2d0a72099615')",  # market for diesel, low-sulfur	diesel, low-sulfur	CO
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '1772b4b7346b1b9acb7d0b572a9e75bf')",  # market for diesel, low-sulfur	diesel, low-sulfur	RoW
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '695a2c9ad1032e2156559c803d9af82f')",  # market for diesel, low-sulfur	diesel, low-sulfur	BR
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '4b07d818e70ec505c01c92640634a8d7')",  # market for diesel, low-sulfur	diesel, low-sulfur	ZA

                   ],
    'methods': ["('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Resources', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Human health', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Ecosystems', 'Aggregated', 'Egalitarian')",
                "('IPCC 2013', 'climate change', 'GWP 100a')"],
    'new activity': "('ecoinvent 3.8_cutoff_ecoSpold02', '204d878220d042ce59dd0e3463976ec3')", # esterification of soybean oil	fatty acid methyl ester	BR
    'reference product': ["diesel, low-sulfur"],
    'folder': 'Diesel from Soy',
    'level': 2,
    'n_top': 50
}
'''

perform_replacement(config)
```


## Installation

`pip install git+https://github.com/UPC-FL/bw_activity_replacement.git


