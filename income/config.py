NETWORKS = [
    {
        "name": "bostrom",
        "lcd_api": "https://lcd.bostrom.bronbro.io",
        "prefix": "bostrom",
        "coingecko_api": "bostrom",
        "addresses": ["bostrom1ydc5fy9fjdygvgw36u49yj39fr67pd9mv67ety"],
        "denom": "boot",
        "exponent": 0
    },
    {
        "name": "osmosis",
        "lcd_api": "https://lcd.osmosis-1.bronbro.io",
        "prefix": "osmo",
        "coingecko_api": "osmosis",
        "addresses": ["osmo1gmc3y8scyx9nemnuk8tj0678mn4w5l78343qvh", "osmo13tk45jkxgf7w0nxquup3suwaz2tx483xrsefl7"],
        "denom": "uosmo",
        "exponent": 6
    },
    {
        "name": "juno",
        "lcd_api": "https://lcd.juno-1.bronbro.io",
        "prefix": "juno",
        "coingecko_api": "juno",
        "addresses": ["juno1quqxfrxkycr0uzt4yk0d57tcq3zk7srmpdd4c7", "juno1gmc3y8scyx9nemnuk8tj0678mn4w5l780uptae"],
        "denom": "ujuno",
        "exponent": 6
    },
    {
        "name": "stargaze",
        "lcd_api": "https://lcd.stargaze-1.bronbro.io",
        "prefix": "stars",
        "coingecko_api": "stars",
        "addresses": ["stars1y58hfnm90r4efhlydx0gavz57lvm7k6uhpzu20"],
        "denom": "ustars",
        "exponent": 6
    },
    {
        "name": "gravity",
        "lcd_api": "https://lcd.gravity-bridge-3.bronbro.io",
        "coingecko_api": "graviton",
        "addresses": ["gravity1vyd4k5j636erx5y5kdqghdu3rfjtwc48axpqfw", "gravity1gmc3y8scyx9nemnuk8tj0678mn4w5l78a7sgld"],
        "prefix": "gravity",
        "denom": "ugraviton",
        "exponent": 6
    },
    {
        "name": "crescent",
        "lcd_api": "https://lcd.crescent-1.bronbro.io",
        "coingecko_api": "crescent-network",
        "addresses": ["cre1c96vvme4k42zlvkc56fslmdpa2qj6u80ycqpsk"],
        "prefix": "cre",
        "denom": "ucre",
        "exponent": 6
    },
    # {
    #     "name": "omniflix",
    #     "lcd_api": "https://lcd.omniflixhub-1.bronbro.io",
    #     "address": "omniflixvaloper1e8grpphncncw9hrutyvnlv77n5dejwcne58zk4",
    #     "coingecko_api": "omniflix-network",
    #     "prefix": "omniflix",
    #     "denom": "uflix",
    #     "exponent": 6
    # },
    {
        "name": "cosmoshub",
        "lcd_api": "https://lcd.cosmoshub-4.bronbro.io",
        "addresses": ["cosmos106yp7zw35wftheyyv9f9pe69t8rteumjxjql7m", "cosmos1gmc3y8scyx9nemnuk8tj0678mn4w5l78ewzs69"],
        "coingecko_api": "cosmos",
        "prefix": "cosmos",
        "denom": "uatom",
        "exponent": 6
    },
    {
        "name": "desmos",
        "lcd_api": "https://lcd.desmos-mainnet.bronbro.io",
        "addresses": ["desmos1sykf8q94l8q8mqstf64ptuvp74ueyehxl9s55g"],
        "coingecko_api": "desmos",
        "prefix": "desmos",
        "denom": "udsm",
        "exponent": 6
    },
    {
        "name": "evmos",
        "lcd_api": "https://lcd.evmos-9001-2.bronbro.io",
        "addresses": ["evmos1ce4vh0e5kanlgc7z0rhcemvd8erjnfzcf8kg7r"],
        "coingecko_api": "evmos",
        "prefix": "evmos",
        "denom": "aevmos",
        "exponent": 18
    },
    {
        "name": "stride",
        "lcd_api": "https://lcd.stride-1.bronbro.io",
        "addresses": ["stride1hl95uhecs4rwe0g432mknz2tsl84f0lt6n9755"],
        "coingecko_api": "stride",
        "prefix": "stride",
        "base_denom": "ustrd",
        "exponent": 6
    },
    {
        "name": "emoney",
        "lcd_api": "https://lcd.emoney-3.bronbro.io/",
        "addresses": ["emoney149vyxd36kxpg46rralaw6eejv4d9daqckn2wt8"],
        "coingecko_api": "e-money",
        "prefix": "emoney",
        "base_denom": "ungm",
        "exponent": 6
    },
]

APIs = [
    ("boot", "bostrom"),
    ("btsg", "bitsong"),
    ("osmo", "osmosis"),
    ("crbrus", "cerberus-2"),
    ("evmos", "evmos"),
    ("graviton", "graviton"),
    ("weth-wei", "ethereum"),
    ("ion", "ion"),
    ("atom", "cosmos"),
    ("juno", "juno-network"),
    ("usdc", "usd-coin"),
    ("bcre", "liquid-staking-crescent"),
    ("cre", "crescent-network"),
    ("dsm", "desmos"),
    ("strd", "stride"),
    ("ngm", "e-money"),
    ("stars", "stargaze")
]
