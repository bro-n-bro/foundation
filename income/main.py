from config import NETWORKS, APIs
from tqdm import tqdm
import requests
import pandas as pd
import aiohttp
import asyncio


async def get_final_df():
    res = []
    for network in tqdm(NETWORKS):
        for address in network['addresses']:
            temp = await get_data(network, address)
            temp = fix_balances(temp)
            res.append(temp)
    df = pd.concat(res, ignore_index=True)
    df = get_prices(df)
    df['usd_value'] = df['amount'] * df['price']

    denom_df = df[['denom', 'usd_value']].groupby('denom').sum().sort_values(by='usd_value', ascending=False)
    denom_df.plot.pie(x='denom', y='usd_value', legend=False).get_figure().savefig('./denom_group.png')
    denom_df.to_csv('./denom_group.csv')

    acc_df_df = df[['address', 'usd_value']].groupby('address').sum().sort_values(by='usd_value', ascending=False)
    acc_df_df.plot.pie(x='address', y='usd_value', legend=False).get_figure().savefig('./address_group.png')
    acc_df_df.to_csv('./address_group.csv')

    df.loc['Liquid'] = df['usd_value'][df['status'] == 'liquid'].sum()
    df.loc['Staked'] = df['usd_value'][df['status'] == 'staked'].sum()
    df.loc['Unbonding'] = df['usd_value'][df['status'] == 'unbonding'].sum()
    df.loc['Rewards'] = df['usd_value'][df['status'] == 'rewards'].sum()
    df.loc['Total'] = df['usd_value'].iloc[:-4].sum()
    df.to_csv('./balances.csv')


def get_prices(df):
    prices = []
    tokens = list(df['denom'].unique())
    for token in tokens:
        try:
            api_id = [item[1] for item in APIs if item[0] == token][0]
            res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={api_id}&vs_currencies=usd").json()
            price = res[api_id]['usd']
        except Exception as e:
            print(e)
            price = 0.0
        temp = (token, price)
        prices.append(temp)
    for index, row in df.iterrows():
        df.loc[index, 'price'] = [item[1] for item in prices if item[0] == row['denom']][0]
    return df


def fix_balances(df):
    for index, row in df.iterrows():
        if row['denom'].startswith('u'):
            df.loc[index, 'denom'] = row['denom'][1:]
            df.loc[index, 'amount'] = row['amount'] / 1_000_000
        elif row['denom'].startswith('a'):
            df.loc[index, 'denom'] = row['denom'][1:]
            df.loc[index, 'amount'] = row['amount'] / 1_000_000_000_000_000_000
        elif row['denom'] == 'weth-wei':
            df.loc[index, 'amount'] = row['amount'] / 1_000_000_000_000_000_000
        else:
            pass
    return df


async def get_data(network, address):
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            asyncio.ensure_future(get_liquid_balance(network, address, session)),
            asyncio.ensure_future(get_staked_balance(network, address, session)),
            asyncio.ensure_future(get_unbonding_balance(network, address, session)),
            asyncio.ensure_future(get_rewards_balance(network, address, session))
        ]
        res = await asyncio.gather(*tasks)
    df = pd.concat(res, ignore_index=True)
    return df


async def get_ibc_denoms(network, df, session):
    tasks = []
    for index, row in df.iterrows():
        if row['denom'].startswith('ibc/'):
            tasks.append(asyncio.ensure_future(get_network_denoms(network, row['denom'], session)))
    token_registry = await asyncio.gather(*tasks)
    token_registry_dict = {}
    [token_registry_dict.update(i) for i in token_registry]
    if token_registry != {}:
        for index, row in df.iterrows():
            if row['denom'].startswith('ibc/'):
                df.loc[index, 'denom'] = token_registry_dict[row['denom']]
            else:
                pass
    else:
        pass
    return df


async def get_network_denoms(network, ibc_denom, session):
    ibc_denom_hash = ibc_denom[4:]
    url = f"{network['lcd_api']}/ibc/apps/transfer/v1/denom_traces/{ibc_denom_hash}"
    try:
        async with session.get(url) as resp:
            resp = await resp.json()
        return {ibc_denom: resp['denom_trace']['base_denom']}
    except Exception as e:
        print(e, url)
        return {ibc_denom: "unknown"}


async def get_liquid_balance(network, address, session):
    url = f"{network['lcd_api']}/cosmos/bank/v1beta1/balances/{address}"
    try:
        async with session.get(url) as resp:
            resp = await resp.json()
            balances = resp['balances']
            # gamm_tokens_df = await get_gamm_tokens_df(balances)
            balances = [b for b in balances if 'gamm' not in b['denom']]
            [b.update({"amount": int(b['amount'])}) for b in balances]
            df = pd.DataFrame.from_records(balances)
            df['network'] = network['name']
            df['status'] = 'liquid'
            df['address'] = address
            df = await get_ibc_denoms(network, df, session)
            return df
    except Exception as e:
        print(e, url)
        return pd.DataFrame()


async def get_gamm_tokens_df(balances):
    return 0


async def get_staked_balance(network, address, session):
    url = f"{network['lcd_api']}/cosmos/staking/v1beta1/delegations/{address}"
    try:
        async with session.get(url) as resp:
            resp = await resp.json()
            delegation_responses = resp['delegation_responses']
            delegations = sum([int(d['balance']['amount']) for d in delegation_responses])
            delegations = [{"denom": network['denom'], "amount": delegations}]
            df = pd.DataFrame.from_records(delegations)
            df['network'] = network['name']
            df['status'] = 'staked'
            df['address'] = address
            return df
    except Exception as e:
        print(e, url)
        return pd.DataFrame()


async def get_unbonding_balance(network, address, session):
    url = f"{network['lcd_api']}/cosmos/staking/v1beta1/delegators/{address}/unbonding_delegations"
    try:
        async with session.get(url) as resp:
            resp = await resp.json()
            delegation_responses = resp['unbonding_delegations']
            delegations = sum([int(d['balance']['amount']) for d in delegation_responses])
            delegations = [{"denom": network['denom'], "amount": delegations}]
            df = pd.DataFrame.from_records(delegations)
            df['network'] = network['name']
            df['status'] = 'unbonding'
            df['address'] = address
            return df
    except Exception as e:
        print(e, url)
        return pd.DataFrame()


async def get_rewards_balance(network, address, session):
    url = f"{network['lcd_api']}/cosmos/distribution/v1beta1/delegators/{address}/rewards"
    try:
        async with session.get(url) as resp:
            resp = await resp.json()
            rewards = int(float(resp['total'][0]['amount']))
            rewards = [{"denom": network['denom'], "amount": rewards}]
            df = pd.DataFrame.from_records(rewards)
            df['network'] = network['name']
            df['status'] = 'rewards'
            df['address'] = address
            return df
    except Exception as e:
        print(e, url)
        return pd.DataFrame()


asyncio.run(get_final_df())