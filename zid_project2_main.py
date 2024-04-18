""" zid_project2_main.py

"""
import csv


# ----------------------------------------------------------------------------
# Part 1: Read the documentation for the following methods:
#   – pandas.DataFrame.mean
#   - pandas.Series.concat
#   – pandas.Series.count
#   – pandas.Series.dropna
#   - pandas.Series.index.to_period
#   – pandas.Series.prod
#   – pandas.Series.resample
#   - ......
# Hint: you can utilize modules covered in our lectures, listed above and any others.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Part 2: import modules inside the project2 package
# ----------------------------------------------------------------------------
# Create import statements so that the module config.py and util.py (inside the project2 package)
# are imported as "cfg", and "util"
#
import numpy as np


# We've imported other needed scripts and defined aliases. Please keep using the same aliases for them in this project.
import zid_project2_etl as etl
import zid_project2_characteristics as cha
import zid_project2_portfolio as pf

import pandas as pd
import util
import config as cfg


# -----------------------------------------------------------------------------------------------
# Part 3: Follow the workflow in portfolio_main function
#         to understand how this project construct total volatility long-short portfolio
# -----------------------------------------------------------------------------------------------
def portfolio_main(tickers, start, end, cha_name, ret_freq_use, q):
    """
    Constructs equal-weighted portfolios based on the specified characteristic and quantile threshold.
    We focus on total volatility investment strategy in this project 2.
    We name the characteristic as 'vol'

    This function performs several steps to construct portfolios:
    1. Call `aj_ret_dict` function from etl script to generate a dictionary containing daily and
       monthly returns.
    2. Call `cha_main` function from cha script to generate a DataFrame containing stocks' monthly return
       and characteristic, i.e., total volatility, info.
    3. Call `pf_main` function from pf script to construct a DataFrame with
       equal-weighted quantile and long-short portfolio return series.

    Parameters
    ----------
    tickers : list
        A list including all tickers (can include lowercase and/or uppercase characters) in the investment universe

    start  :  str
        The inclusive start date for the date range of the price table imported from data folder
        For example: if you enter '2010-09-02', function in etl script will include price
        data of stocks from this date onwards.
        And make sure the provided start date is a valid calendar date.

    end  :  str
        The inclusive end date for the date range, which determines the final date
        included in the price table imported from data folder
        For example: if you enter '2010-12-20', function in etl script will encompass data
        up to and including December 20, 2010.
        And make sure the provided start date is a valid calendar date.

    cha_name : str
        The name of the characteristic. Here, it should be 'vol'

    ret_freq_use  :  list
        It identifies that which frequency returns you will use to construct the `cha_name`
        in zid_project2_characteristics.py.
        Set it as ['Daily',] when calculating stock total volatility here.

    q : int
        The number of quantiles to divide the stocks into based on their characteristic values.


    Returns
    -------
    dict_ret : dict
        A dictionary with two items, each containing a dataframe of daily and monthly returns
        for all stocks listed in the 'tickers' list.
        This dictionary is the output of `aj_ret_dict` in etl script.
        See the docstring there for a description of it.

    df_cha : df
        A DataFrame with a Monthly frequency PeriodIndex, containing rows for each year-month
        that include the stocks' monthly returns for that period and the characteristics,
        i.e., total volatility, from the previous year-month.
        This df is the output of `cha_main` function in cha script.
        See the docstring there for a description of it.

    df_portfolios : df
        A DataFrame containing the constructed equal-weighted quantile and long-short portfolios.
        This df is the output of `pf_cal` function in pf script.
        See the docstring there for a description of it.

    """

    # --------------------------------------------------------------------------------------------------------
    # Part 4: Complete etl scaffold to generate returns dictionary and to make ad_ret_dic function works
    # --------------------------------------------------------------------------------------------------------
    dict_ret = etl.aj_ret_dict(tickers, start, end)

    print("Dict return is:", dict_ret)
    # ---------------------------------------------------------------------------------------------------------
    # Part 5: Complete cha scaffold to generate dataframe containing monthly total volatility for each stock
    #         and to make char_main function work
    # ---------------------------------------------------------------------------------------------------------
    df_cha = cha.cha_main(dict_ret, cha_name,  ret_freq_use)

    print("Df cha is:", df_cha)
    # -----------------------------------------------------------------------------------------------------------
    # Part 6: Read and understand functions in pf scaffold. You will need to utilize functions there to
    #         complete some of the questions in Part 7
    # -----------------------------------------------------------------------------------------------------------
    df_portfolios = pf.pf_main(df_cha, cha_name, q)

    print("Df portfolios is:", df_portfolios)

    util.color_print('Portfolio Construction All Done!')

    return dict_ret, df_cha, df_portfolios


# ----------------------------------------------------------------------------
# Part 7: Complete the auxiliary functions
# ----------------------------------------------------------------------------
def get_avg(df: pd.DataFrame, year):
    """ Returns the average value of all columns in the given df for a specified year.

    This function will calculate the column average for all columns
    from a data frame `df`, for a given year `year`.
    The data frame `df` must have a DatetimeIndex or PeriodIndex index.

    Missing values will not be included in the calculation.

    Parameters
    ----------
    df : data frame
        A Pandas data frame with a DatetimeIndex or PeriodIndex index.

    year : int
        The year as a 4-digit integer.

    Returns
    -------
    ser
        A series with the average value of columns for the year `year`.

    Example
    -------
    For a data frame `df` containing the following information:

        |            | tic1 | tic2  |
        |------------+------+-------|
        | 1999-10-13 | -1   | NaN   |
        | 1999-10-14 | 1    | 0.032 |
        | 2020-10-15 | 0    | -0.02 |
        | 2020-10-16 | 1    | -0.02 |

        >> res = get_avg(df, 1999)
        >> print(res)
        tic1      0.000
        tic2      0.032
        dtype: float64

    """
    df_year = df[df.index.year == year]
    average_returns = df_year.mean(axis=0)
    return average_returns

def get_cumulative_ret(df):
    """ Returns cumulative returns for input DataFrame.

    Given a df with return series, this function will return the
    buy and hold return for the whole period.

    Parameters
    ----------
    df : DataFrame
        A Pandas DataFrame containing monthly portfolio returns
        with a PeriodIndex index.

    Returns
    -------
    df
        A df with the cumulative returns for portfolios, ignoring missing observations.

    Notes
    -----
    The buy and hold cumulative return will be computed as follows:

        (1 + r1) * (1 + r2) *....* (1 + rN) - 1
        where r1, ..., rN represents monthly returns

    """
    cumulative_ret = (1 + df).cumprod() - 1
    return cumulative_ret

# ----------------------------------------------------------------------------
# Part 8: Answer questions
# ----------------------------------------------------------------------------
# NOTES:
#
# - THE SCRIPTS YOU NEED TO SUBMIT ARE
#   zid_project2_main.py, zid_project2_etl.py, and zid_project2_characteristics.py
#
# - Do not create any other functions inside the scripts you need to submit unless
#   we ask you to do so.
#
# - For this part of the project, only the answers provided below will be
#   marked. You are free to create any function you want (IN A SEPARATE
#   MODULE outside the scripts you need to submit).
#
# - All your answers should be strings. If they represent a number, include 4
#   decimal places unless otherwise specified in the question description
#
# - Here is an example of how to answer the questions below. Consider the
#   following question:
#
#   Q0: Which ticker included in config.TICMAP starts with the letter "C"?
#   Q0_answer = '?'
#
#   You should replace the '?' with the correct answer:
#   Q0_answer = 'CSCO'
#
#
#     To answer the questions below, you need to run portfolio_main function in this script
#     with the following parameter values:
#     tickers: all tickers included in the dictionary config.TICMAP,
#     start: '2000-12-29',
#     end: '2021-08-31',
#     cha_name: 'vol'.
#     ret_freq_use: ['Daily',],
#     q: 3
#     Please name the three output files as DM_Ret_dict, Vol_Ret_mrg_df, EW_LS_pf_df.
#     You can utilize the three output files and auxiliary functions to answer the questions.


# Q1: Which stock in your sample has the lowest average daily return for the
#     year 2008 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q1_ANSWER = 'NVDA'


# Q2: What is the daily average return of the stock in question 1 for the year 2008.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q2_ANSWER = '-0.004240838144502279'


# Q3: Which stock in your sample has the highest average monthly return for the
#     year 2019 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q3_ANSWER = 'AAPL'


# Q4: What is the average monthly return of the stock in question 3 for the year 2019.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q4_ANSWER = '0.05663463742976457'


# Q5: What is the average monthly total volatility for stock 'TSLA' in the year 2010?
#     Use the output dataframe, Vol_Ret_mrg_df, and auxiliary function in this script
#     to do the calculation.
Q5_ANSWER = '0.041407897077777645'


# Q6: What is the ratio of the average monthly total volatility for stock 'V'
#     in the year 2008 to that in the year 2018? Keep 1 decimal places.
#     Use the output dataframe, Vol_Ret_mrg_df, and auxiliary function in this script
#     to do the calculation.
Q6_ANSWER = '2.6'


# Q7: How many effective year-month for stock 'TSLA' in year 2010. An effective year-month
#     row means both monthly return in 'tsla' column and total volatility in 'tsla_vol'
#     are not null.
#     Use the output dataframe, Vol_Ret_mrg_df, to do the calculation.
#     Answer should be an integer
Q7_ANSWER = '122'


# Q8: How many rows and columns in the EW_LS_pf_df data frame?
#     Answer should be two integer, the first represent number of rows and the two numbers need to be
#     separated by a comma.
Q8_ANSWER = '234, 4'


# Q9: What is the average equal weighted portfolio return of the quantile with the
#     lowest total volatility for the year 2019?
#     Use the output dataframe, EW_LS_pf_d, and auxiliary function in this script
#     to do the calculation.
Q9_ANSWER = '0.019546444313242817'


# Q10: What is the cumulative portfolio return of the total volatility long-short portfolio
#      over the whole sample period?
#      Use the output dataframe, EW_LS_pf_d, and auxiliary function in this script
#     to do the calculation.
Q10_ANSWER = '1.0184698615759582'

# ----------------------------------------------------------------------------
# Part 9: Add t_stat function
# ----------------------------------------------------------------------------
# We've outputted EW_LS_pf_df file and save the total volatility long-short portfolio
# in 'ls' column from Part 8.

# Please add an auxiliary function called ‘t_stat’ below.
# You can design the function's parameters and output table.
# But make sure it can be used to output a DataFrame including three columns:
# 1.ls_bar, the mean of 'ls' columns in EW_LS_pf_df
# 2.ls_t, the t stat of 'ls' columns in EW_LS_pf_df
# 3.n_obs, the number of observations of 'ls' columns in EW_LS_pf_df

# Notes:
# Please add the function in zid_project2_main.py.
# The name of the function should be t_stat and including docstring.
# Please replace the '?' of ls_bar, ls_t and n_obs variables below
# with the respective values of the 'ls' column in EW_LS_pf_df from Part 8,
# keep 4 decimal places if it is not an integer:
ls_bar = '0.0061'
ls_t = '1.1837'
n_obs = '234'


def t_stat():
    """
    Auxiliary function to calculate the mean, t-statistic, and number of observations for the 'ls' column in the
    EW_LS_pf_df DataFrame.

    Returns
    -------
    result
        A DataFrame with columns 'ls_bar', 'ls_t', and 'n_obs' representing the mean, t-statitistic and number of
        observations respectively.
    """
    ew_ls_pf_df = pd.read_csv('EW_LS_pf_df.csv', index_col=0)
    ew_ls_pf_df.index = pd.to_datetime(ew_ls_pf_df.index)

    ls_bar = ew_ls_pf_df['ls'].mean()
    ls_std = ew_ls_pf_df['ls'].std()
    n_obs = len(ew_ls_pf_df['ls'].dropna())
    ls_t = ls_bar / (ls_std / np.sqrt(n_obs))

    result = pd.DataFrame({'ls_bar': [ls_bar], 'ls_t': [ls_t], 'n_obs': [n_obs]})

    return result

# ----------------------------------------------------------------------------
# Part 10: project 2 mini-presentation
# ----------------------------------------------------------------------------
# In this part, you are going to record and present a strictly less than 15 minutes long presentation.
# You should seek to briefly describe:
# 1.	What are the null and alternative hypotheses that the project 2 is testing
# 2.	What’s the methodology of the portfolio construction
#       and how is it implemented in Project 2 codebase?
# 3.	What inferences can we draw from the output of Part 9,
#       including the average return and t-stats of the long-short portfolio?
# 4.	Do you think the results are reliable? Why or why not?
# 5.	Is there any further work you would like to pursue based on Project 2?
#       Share your to-do list.
#
# For this mini-presentation, it is up to the group to decide whether all the members
# are in the presentation video or not.
# Please use Zoom to record it. The final submission should be a zoom recording link.

# Please replace the '?' with your team's presentation video zoom link and its password:
Presentation_zoom_link = '?'
Password_of_your_video = '?'


def _test_get_avg():
    """ Test function for `get_avg`
    """
    # Made-up data
    ret = pd.Series({
        '2019-01-01': 1.0,
        '2019-01-02': 2.0,
        '2020-10-02': 4.0,
        '2020-11-12': 4.0,
    })
    df = pd.DataFrame({'some_tic': ret})
    df.index = pd.to_datetime(df.index)

    msg = 'This is the test data frame `df`:'
    util.test_print(df, msg)

    res = get_avg(df,  2019)
    to_print = [
        "This means `res =get_avg(df, year=2019) --> 1.5",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


def _test_get_cumulative_ret():
    """ Test function for `get_ann_ret`

    To construct this example, suppose first that holding the stock for 400
    trading days gives a total return of 1.5 (so 50% over 400 trading days).

    The annualised return will then be:

        (tot_ret)**(252/N) - 1 = 1.5 ** (252/400) - 1 = 0.2910

    Create an example data frame with 400 copies of the daily yield, where

        daily yield = 1.5 ** (1/400) - 1

    """
    # Made-up data
    idx_m = pd.to_datetime(['2019-02-28',
                            '2019-03-31',
                            '2019-04-30',]).to_period('M')
    stock1_m = [0.063590, 0.034290, 0.004290]
    stock2_m = [None, 0.024390, 0.022400]
    monthly_ret_df = pd.DataFrame({'stock1': stock1_m, 'stock2': stock2_m, }, index=idx_m)
    monthly_ret_df.index.name = 'Year_Month'
    msg = 'This is the test data frame `monthly_ret_df`:'
    util.test_print(monthly_ret_df, msg)

    res = get_cumulative_ret(monthly_ret_df)
    to_print = [
        "This means `res =get_cumulative_ret(monthly_ret_df)",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


# Function to help solve questions using the output files from portfolio_main and auxiliary functions
def solve_questions():

    # Q1: Which stock in your sample has the lowest average daily return for the year 2008 (ignoring missing values)?
    #     Your answer should include the ticker for this stock.
    dm_ret_df_daily = pd.read_csv('DM_Ret_dict_daily.csv', index_col=0)
    dm_ret_df_daily.index = pd.to_datetime(dm_ret_df_daily.index)
    q1_df_daily_ret = get_avg(dm_ret_df_daily, 2008)
    q1_answer = q1_df_daily_ret.idxmin()
    print("Answer to q1 is:", q1_answer)

    # Q2: What is the daily average return of the stock in question 1 for the year 2008.
    q2_answer = q1_df_daily_ret.min()
    print("Answer to q2 is:", q2_answer)

    # Alternate way to check Q2:
    stock_q1 = dm_ret_df_daily[q1_answer]
    q2_answer = get_avg(stock_q1, 2008)
    print("Answer to q2 (second try) is:", q2_answer)

    # Q3: Which stock in your sample has the highest average monthly return for the year 2019 (ignoring missing values)?
    #     Your answer should include the ticker for this stock.
    dm_ret_df_monthly = pd.read_csv('DM_Ret_dict_monthly.csv', index_col=0)
    dm_ret_df_monthly.index = pd.to_datetime(dm_ret_df_monthly.index)
    q3_df_monthly_ret = get_avg(dm_ret_df_monthly, 2019)
    q3_answer = q3_df_monthly_ret.idxmax()
    print("Answer to q3 is:", q3_answer)

    # Q4: What is the average monthly return of the stock in question 3 for the year 2019.
    q4_answer = q3_df_monthly_ret.max()
    print("Answer to q4 is:", q4_answer)

    # Alternate way to check Q4:
    stock_q3 = dm_ret_df_monthly[q3_answer]
    q4_answer = get_avg(stock_q3, 2019)
    print("Answer to q4 (second try) is:", q4_answer)

    # Q5: What is the average monthly total volatility for stock 'TSLA' in the year 2010?
    vol_ret_mrg_df = pd.read_csv('Vol_Ret_mrg_df.csv', index_col=0)
    vol_ret_mrg_df.index = pd.to_datetime(vol_ret_mrg_df.index)
    tsla_vol = vol_ret_mrg_df['tsla_vol']
    q5_answer = get_avg(tsla_vol, 2010)
    print("Answer to q5 is:", q5_answer)

    # Q6: What is the ratio of the average monthly total volatility for stock 'V'
    #     in the year 2008 to that in the year 2018? Keep 1 decimal place.
    v_vol = vol_ret_mrg_df['v_vol']
    v_vol_2008 = get_avg(v_vol, 2008)
    v_vol_2018 = get_avg(v_vol, 2018)
    q6_answer = round(v_vol_2008 / v_vol_2018, 1)
    print("Answer to q6 is:", q6_answer)

    # Q7: How many effective year-month for stock 'TSLA' in year 2010.
    #     An effective year-month row means both monthly return in 'tsla' column
    #     and total volatility in 'tsla_vol' are not null.
    tsla_effective_2010 = vol_ret_mrg_df['tsla'].notnull() & vol_ret_mrg_df['tsla_vol'].notnull()
    q7_answer = tsla_effective_2010.sum()
    print("Answer to q7 is:", q7_answer)

    # Q8: How many rows and columns in the EW_LS_pf_df data frame?
    ew_ls_pf_df = pd.read_csv('EW_LS_pf_df.csv', index_col=0)
    ew_ls_pf_df.index = pd.to_datetime(ew_ls_pf_df.index)
    q8_answer = f"Rows: {ew_ls_pf_df.shape[0]}, Columns: {ew_ls_pf_df.shape[1]}"
    print("Answer to q8 is:", q8_answer)

    # Q9: What is the average equal weighted portfolio return of the quantile with the
    #     lowest total volatility for the year 2019?
    q9_answer = get_avg(ew_ls_pf_df['ewp_rank_1'], 2019)
    print("Answer to q9 is:", q9_answer)

    # # Q10: What is the cumulative portfolio return of the total volatility long-short portfolio
    # #      over the whole sample period?
    q10_answer = get_cumulative_ret(ew_ls_pf_df['ls']).iloc[-1]
    print("Answer to q10 is:", q10_answer)


if __name__ == "__main__":
    # Testing auxiliary functions
    # print("Testing 6A:")
    # _test_get_avg()
    #
    # print("\nTesting 6B:")
    # _test_get_cumulative_ret()

    # Creating files for Q1
    # tickers = list(cfg.TICMAP.keys())
    # start = '2000-12-29'
    # end = '2021-08-31'
    # cha_name = 'vol'
    # ret_freq_use = ['Daily', ]
    # q = 3
    # dict_ret, df_cha, df_portfolios = portfolio_main(tickers, start, end, cha_name, ret_freq_use, q)
    #
    # dict_ret['Daily'].to_csv('DM_Ret_dict_daily.csv')
    # dict_ret['Monthly'].to_csv('DM_Ret_dict_monthly.csv')
    # df_cha.to_csv('Vol_Ret_mrg_df.csv')
    # df_portfolios.to_csv('EW_LS_pf_df.csv')

    # solve_questions()
    # t_stat()





