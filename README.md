# bw_activity_replacement

Apply the activity replacement in brightway 2.

## Usage

The documentation will be updated for a general example that can be applied without importing the hydrogen process.

```python
from bw_activity_replacement import perform_replacement

config = {
    'db': 'ecoinvent 3.8_cutoff_ecoSpold02',
    'project': 'Test',
    'activities': ["('ecoinvent 3.8_cutoff_ecoSpold02', 'bc08eb18034c14bba694e151a163982a')", # market for hydrogen, gaseous	hydrogen, gaseous	GLO
                   "('ecoinvent 3.8_cutoff_ecoSpold02', 'a834063e527dafabe7d179a804a13f39')", # market for hydrogen, liquid	hydrogen, liquid	RER
                   "('ecoinvent 3.8_cutoff_ecoSpold02', '9fed50977b761e7d6e212c93f8d4ab40')"  # market for hydrogen, liquid	hydrogen, liquid	RoW
                   ],
    'methods': ["('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Resources', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Human health', 'Aggregated', 'Egalitarian')",
                "('ReCiPe 2016', '1.1 (20180117)', 'Endpoint', 'Ecosystems', 'Aggregated', 'Egalitarian')",
                "('IPCC 2013', 'climate change', 'GWP 100a')"],
    #'new activity': 'H2_fromPE+PP+PS_with_CCS (OFC) | 99.91mole% purity | APOS, U | csalah',
    'new activity': 'H2_fromPE+PP+PS | 99.91mole% purity | APOS, U | csalah',
    'reference product': ["hydrogen, liquid",
                          "hydrogen, gaseous"],
    'folder': 'H2 without CCS'
}

perform replacement(config)
```


## Installation

`pip install git+https://github.com/UPC-FL/bw_activity_replacement.git


