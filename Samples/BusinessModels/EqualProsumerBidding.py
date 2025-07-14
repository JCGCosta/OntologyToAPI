import pandas as pd
import logging

async def EqualProsumerBidding(data):
    # Prices
    community_price = data['ProsumersCommunityBid_R'][0]['Prosumers_Community_Price']
    trading_company_price = data['TradingCompanySmallBid_R'][0]['Trading_Company_Small_Price']

    if community_price > trading_company_price:
        return "The prosumers community price is greater than the trading company price."

    # Prepare data
    lem_data = pd.DataFrame({
        'UTC_T': [item['UTC_T'] for item in data['UTCTimestamp_R']],
        'Member_ID': [item['Member_ID'] for item in data['HouseholderID_R']],
        'Electricity_Load': [item['Electricity_Load'] for item in data['ElectricityLoad_R']],
        'Residential_Solar_Generation': [item['Residential_Solar_Generation'] for item in data['ResidentialSolarGeneration_R']],
        'Residential_Wind_Generation': [item['Residential_Wind_Generation'] for item in data['ResidentialWindGeneration_R']]
    })

    # Only consider the earliest timestamp
    lem_data['UTC_T'] = pd.to_datetime(lem_data['UTC_T'])
    earliest_timestamp = lem_data['UTC_T'].min()
    early_lem_data = lem_data[lem_data['UTC_T'] == earliest_timestamp].copy()

    # Calculate individual and community production and consumption
    early_lem_data['Electricity_Produced'] = (
        early_lem_data['Residential_Solar_Generation'] + early_lem_data['Residential_Wind_Generation']
    )
    early_lem_data['Net_Balance'] = early_lem_data['Electricity_Produced'] - early_lem_data['Electricity_Load']

    total_produced = early_lem_data['Electricity_Produced'].sum()
    total_consumed = early_lem_data['Electricity_Load'].sum()
    community_balance = total_produced - total_consumed

    if total_produced == 0 or total_consumed == 0:
        return "No valid community transaction (zero production or consumption)."

    # Only portion of consumption covered by community
    used_energy_fraction = min(total_consumed / total_produced, 1.0)
    total_community_payment = community_price * total_produced * used_energy_fraction

    # Allocate to producers (positive net balance)
    producers = early_lem_data[early_lem_data['Net_Balance'] > 0].copy()
    total_producer_share = (producers['Electricity_Produced'] * used_energy_fraction).sum()
    if total_producer_share > 0:
        producers['Billing'] = (
            community_price * producers['Electricity_Produced'] * used_energy_fraction
        )
    else:
        producers['Billing'] = 0.0

    # Allocate to consumers (negative net balance)
    consumers = early_lem_data[early_lem_data['Net_Balance'] < 0].copy()
    consumers['Share'] = consumers['Electricity_Load'] / total_consumed
    consumers['Billing'] = -1 * consumers['Share'] * total_community_payment

    # Zero-balance members (e.g. Trading Company)
    neutrals = early_lem_data[early_lem_data['Net_Balance'] == 0].copy()
    neutrals['Billing'] = 0.0

    # Combine all members
    final_df = pd.concat([producers, consumers, neutrals], ignore_index=True)
    final_df['Billing'] = final_df['Billing'].round(4)

    inserted_id = await data['conn']['epbbm'][0].exec_insert(
        f"INSERT INTO lem_results (UTC_T, LEM_TOTAL_PRODUCED, LEM_TOTAL_CONSUMED) VALUES "
        f"(\"{earliest_timestamp}\", \"{round(total_produced, 4)}\", \"{round(total_consumed, 4)}\");")

    for index, row in final_df.iterrows():
        await data['conn']['epbbm'][0].exec_insert(
            f"INSERT INTO lem_billing (RESULTS_ID, MEMBER_ID, BILL) VALUES "
            f"(\"{inserted_id}\", \"{row['Member_ID']}\", \"{row['Billing']}\");")

    return {
        "UTC_T": earliest_timestamp,
        "Community_Total_Produced": round(total_produced, 4),
        "Community_Total_Consumed": round(total_consumed, 4),
        "Community_Balance": round(community_balance, 4),
        "Used_Energy_Fraction": round(used_energy_fraction, 4),
        "Total_Community_Payment": round(total_community_payment, 4),
        "Billing": final_df[['Member_ID', 'Electricity_Load', 'Electricity_Produced', 'Net_Balance', 'Billing']].to_dict(orient='records')
    }
