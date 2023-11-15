from database import execute_sql_query
import pandas as pd
from sqlalchemy import text

original_table = 'homecare_icecream_22_23'
condensed_table = 'homecare_icecream_condensed'
view_name=  'homecare_icecream_22_23_view'

create_view = """
    CREATE OR REPLACE VIEW public.homecare_view_updated
as select
	lower({original_table}.category) as category ,
	lower({original_table}.country) as country ,
	{original_table}.periodperiod ,
	replace(lower({original_table}.brand),'total' ,'merk') as brand ,
	{original_table}.gross_profit,
	{original_table}.turnover ,
	{original_table}.pbo ,
	{original_table}.media_costs_traditional ,
	{original_table}.uop ,
	{original_table}.deflated_cy_turnover ,
	{original_table}.deflated_acquisition_turnover ,
	{original_table}.turnover_py ,
	{original_table}.deflated_turnover_hyper_adjustment ,
	{original_table}.disposal_turnover ,
	{original_table}.advertising_cy ,
	{original_table}.promotions_cy ,
	{original_table}.distribution_costs,
	{original_table}.acquisition_turnover,
	{original_table}.supply_chain_cost ,
	{original_table}.material_costs,
	{original_table}.cy_sales_vol ,
	{original_table}.trade_terms,
	gross_sales_value_gsv ,
	{original_table}.brand_and_marketing_investment,
	{original_table}.point_of_sale_investment,
	{original_table}.controllable_cost
	   FROM {original_table}
  WHERE {original_table}."flow_name" = 'Month'::text
"""

create_table_from_view = f"""Select * into {condensed_table} from {view_name}"""

''' call only when the table column names need to be renamed to lower case column names '''
def alter_database_schema():
    column_names = [i[0] for i in execute_sql_query(text(f"select column_name  from information_schema.columns where table_name ='{table_name}'"),True)]
    for i in column_names:
        try:
            print(f'renaming column {i}')
            execute_sql_query(text(f"""alter table {table_name}  rename column "{i}" to "{i.lower()}" """))
        except Exception as e:
            print(e)
    execute_sql_query(text(create_view))
    execute_sql_query(text(create_table_from_view))

''' pushing file to database '''
def create_table_from_datasource(dir_name):
    df = []
    ''' delete table from db '''
    execute_sql_query(text('drop table {original_table}'))
    for i in os.listdir(dir_name):
        temp_df = pd.read_csv(f"{dir_name}/{i}")
        temp_df = temp_df[temp_df['Flow_Name']=='Month']
        df.append(temp_df)
    print('Combined temp dfs')
    combined_df = pd.concat(df)
    print('Combined dfs , starting push to database')
    combined_df.to_csv('homecare_22_23.csv',index=False)
    with engine.begin() as connection:
        combined_df.to_sql(table_name,con=connection,index=False)
    print('Created new table')
    alter_database_schema()

create_table_from_datasource('/home/vishnu/Downloads/compass_output_june_23')
