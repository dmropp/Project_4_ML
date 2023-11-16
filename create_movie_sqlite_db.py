# This file only serves to create the movie_ratings_db.sqlite file

import sqlite3
import pandas as pd

from pathlib import Path

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float

database_path = "movie_ratings_db.sqlite"

Path(database_path).touch()

conn = sqlite3.connect(database_path)
c = conn.cursor()


#This code creates an initial table to hold all data, imports the data from the csv files, creates a class with a second table, copies the
#desired columns into the new table, drops the original table, and then clears the empty space in the database via vacuum. The SQLite database was
#created via commands in the terminal. ONLY USE IF THE .SQLITE DATABASE NEEDS TO BE CREATED FROM SCRATCH.

# Before running the code blocks below, in the terminal enter the following commands to create the empty database:
# sqlite3 oregon_crashes.sqlite
# .save oregon_crashes.sqlite
# .quit

#Create the initial table for all columns in the csv files. Run this code block first.
# added IF NOT EXISTS to the query as an extra failsafe in case a table already exists
# https://www.geeksforgeeks.org/python-sqlite-create-table/?ref=lbp, referenced for table creation
# c.execute('''CREATE TABLE IF NOT EXISTS crashes (CRASH_ID	int, SER_NO int, CRASH_DT date, CRASH_MO_NO	int, CRASH_DAY_NO int, CRASH_YR_NO int,
#     CRASH_WK_DAY_CD	int, CRASH_HR_NO int, CRASH_HR_SHORT_DESC text, CNTY_ID	int, CNTY_NM text, CITY_SECT_ID	int, CITY_SECT_NM text,
#     URB_AREA_CD	int, URB_AREA_SHORT_NM text, FC_CD int, FC_SHORT_DESC text, NHS_FLG text, HWY_NO int, HWY_SFX_NO int,
#     HWY_MED_NM text, RDWY_NO int, HWY_COMPNT_CD	int, HWY_COMPNT_SHORT_DESC text, MLGE_TYP_CD int, MLGE_TYP_SHORT_DESC text,
#     RD_CON_NO int, LRS_VAL int, LAT_DEG_NO int, LAT_MINUTE_NO int, LAT_SEC_NO float, LONGTD_DEG_NO int, LONGTD_MINUTE_NO int,
#     LONGTD_SEC_NO float, LAT_DD float, LONGTD_DD float, SPECL_JRSDCT_ID int, SPECL_JRSDCT_SHORT_DESC text, JRSDCT_GRP_CD int,
#     JRSDCT_GRP_LONG_DESC text, AGY_ST_NO int, ST_FULL_NM text, RECRE_RD_NM text, ISECT_AGY_ST_NO text, ISECT_ST_FULL_NM text,
#     ISECT_RECRE_RD_NM text, ISECT_SEQ_NO int, FROM_ISECT_DSTNC_QTY int, CMPSS_DIR_CD int, MP_NO float, POST_SPEED_LMT_VAL int,
#     RD_CHAR_CD int, RD_CHAR_SHORT_DESC text, OFF_RDWY_FLG text, ISECT_TYP_CD int, ISECT_TYP_SHORT_DESC text, ISECT_REL_FLG text,
#     RNDABT_FLG text, DRVWY_REL_FLG text, LN_QTY int, TURNG_LEG_QTY int, MEDN_TYP_CD int, MEDN_TYP_SHORT_DESC text, IMPCT_LOC_CD	int,
#     CRASH_TYP_CD text, CRASH_TYP_SHORT_DESC text, COLLIS_TYP_CD int, COLLIS_TYP_SHORT_DESC text, CRASH_SVRTY_CD int,
#     CRASH_SVRTY_SHORT_DESC text, WTHR_COND_CD int, WTHR_COND_SHORT_DESC text, RD_SURF_COND_CD int, RD_SURF_SHORT_DESC text,
#     LGT_COND_CD	int, LGT_COND_SHORT_DESC text, TRAF_CNTL_DEVICE_CD int, TRAF_CNTL_DEVICE_SHORT_DESC text, TRAF_CNTL_FUNC_FLG text,
#     INVSTG_AGY_CD int, INVSTG_AGY_SHORT_DESC text, CRASH_EVNT_1_CD int, CRASH_EVNT_1_SHORT_DESC text, CRASH_EVNT_2_CD int,
#     CRASH_EVNT_2_SHORT_DESC text, CRASH_EVNT_3_CD int, CRASH_EVNT_3_SHORT_DESC text, CRASH_CAUSE_1_CD int, CRASH_CAUSE_1_SHORT_DESC text,
#     CRASH_CAUSE_2_CD int, CRASH_CAUSE_2_SHORT_DESC text, CRASH_CAUSE_3_CD int, CRASH_CAUSE_3_SHORT_DESC text, SCHL_ZONE_IND int,
#     WRK_ZONE_IND int, ALCHL_INVLV_FLG text, DRUG_INVLV_FLG text, MJ_INVLV_FLG text, CRASH_SPEED_INVLV_FLG text,
#     CRASH_HIT_RUN_FLG text, POP_RNG_CD int, POP_RNG_MED_DESC text, RD_CNTL_CD int, RD_CNTL_MED_DESC text, RTE_TYP_CD text,
#     RTE_ID text, RTE_NM text, REG_ID int, DIST_ID text, SEG_MRK_ID text, SEG_PT_LRS_MEAS float, UNLOCT_FLG text,
#     CRASH_LAST_UD_DT date, TOT_VHCL_CNT int, TOT_FATAL_CNT int, TOT_INJ_LVL_A_CNT int, TOT_INJ_LVL_B_CNT int, TOT_INJ_LVL_C_CNT int,
#     TOT_INJ_CNT int, TOT_UNINJD_AGE00_04_CNT int, TOT_UNINJD_PER_CNT int, TOT_PED_CNT int, TOT_PED_FATAL_CNT int,
#     TOT_PED_INJ_LVL_A_CNT int, TOT_PED_INJ_CNT int, TOT_PEDCYCL_CNT int, TOT_PEDCYCL_FATAL_CNT int, TOT_PEDCYCL_INJ_LVL_A_CNT int,
#     TOT_PEDCYCL_INJ_CNT int, TOT_UNKNWN_CNT int, TOT_UNKNWN_FATAL_CNT int, TOT_UNKNWN_INJ_CNT int, TOT_OCCUP_CNT int,
#     TOT_PER_INVLV_CNT int, TOT_SFTY_EQUIP_USED_QTY int, TOT_SFTY_EQUIP_UNUSED_QTY int, TOT_SFTY_EQUIP_USE_UNKNOWN_QTY int,
#     TOT_PSNGR_VHCL_OCC_UNRESTRND_FATAL_CNT int, TOT_MCYCLST_FATAL_CNT int, TOT_MCYCLST_INJ_LVL_A_CNT int, TOT_MCYCLST_INJ_CNT int,
#     TOT_MCYCLST_UNHELMTD_FATAL_CNT int, TOT_ALCHL_IMPAIRED_DRVR_INV_FATAL_CNT int, TOT_DRVR_AGE_01_20_CNT int,
#     LANE_RDWY_DPRT_CRASH_FLG text);'''
#     )

#Import csv data to initial table. Run this code block second.
#modified to work with my machines file directory. Will need to change to be more general at some point
# links_data = pd.read_csv("ml-latest-small/links.csv")
# links_data.to_sql("links", conn, if_exists='append', index=False)
# movies_data = pd.read_csv("ml-latest-small/movies.csv")
# movies_data.to_sql("movies", conn, if_exists='append', index=False)
# ratings_data = pd.read_csv("ml-latest-small/ratings.csv")
# ratings_data.to_sql("ratings", conn, if_exists='append', index=False)
# tags_data = pd.read_csv("ml-latest-small/tags.csv") 
# tags_data.to_sql("tags", conn, if_exists='append', index=False)

# Copy data from the original table into new table. Run this code block fourth.
# c.execute('''INSERT INTO oregon_crashes(CRASH_ID, CRASH_DT, CRASH_YR_NO, HWY_MED_NM, LAT_DD, LONGTD_DD, CRASH_TYP_CD, CRASH_TYP_SHORT_DESC,
#   CRASH_SVRTY_CD, CRASH_SVRTY_SHORT_DESC, CRASH_EVNT_1_CD, CRASH_EVNT_1_SHORT_DESC,
#   CRASH_EVNT_2_CD, CRASH_EVNT_2_SHORT_DESC, CRASH_EVNT_3_CD,
#   CRASH_EVNT_3_SHORT_DESC, CRASH_CAUSE_1_CD, CRASH_CAUSE_1_SHORT_DESC, CRASH_CAUSE_2_CD, 
#   CRASH_CAUSE_2_SHORT_DESC, CRASH_CAUSE_3_CD, CRASH_CAUSE_3_SHORT_DESC) 
#   SELECT CRASH_ID, CRASH_DT, CRASH_YR_NO, HWY_MED_NM, LAT_DD, LONGTD_DD, CRASH_TYP_CD, CRASH_TYP_SHORT_DESC,
#   CRASH_SVRTY_CD, CRASH_SVRTY_SHORT_DESC, CRASH_EVNT_1_CD, CRASH_EVNT_1_SHORT_DESC,
#   CRASH_EVNT_2_CD, CRASH_EVNT_2_SHORT_DESC, CRASH_EVNT_3_CD,
#   CRASH_EVNT_3_SHORT_DESC, CRASH_CAUSE_1_CD, CRASH_CAUSE_1_SHORT_DESC, CRASH_CAUSE_2_CD, 
#   CRASH_CAUSE_2_SHORT_DESC, CRASH_CAUSE_3_CD, CRASH_CAUSE_3_SHORT_DESC FROM crashes''')

#Drop the original table. Run this code block fifth.
# c.execute('''DROP TABLE crashes''')

#Deletes all empty space in the database. Run this code block sixth.
#c.execute("VACUUM") # https://stackoverflow.com/questions/4712929/how-to-use-sqlite-3s-vacuum-command-in-python, how to use vacuum to clear unused space from database

conn.commit()

conn.close()

#Create oregon_crashes class and new table with desired columns. Run this code block third.
# class Oregon_crashes(Base):
#     __tablename__ = "oregon_crashes"
#     CRASH_ID = Column(Integer, primary_key=True)
#     CRASH_DT = Column(String)
#     CRASH_YR_NO = Column(Integer)
#     HWY_MED_NM = Column(String)
#     LAT_DD = Column(Float)
#     LONGTD_DD = Column(Float)
#     CRASH_TYP_CD = Column(String)
#     CRASH_TYP_SHORT_DESC = Column(String)
#     CRASH_SVRTY_CD = Column(Integer)
#     CRASH_SVRTY_SHORT_DESC = Column(String)
#     CRASH_EVNT_1_CD = Column(Integer)
#     CRASH_EVNT_1_SHORT_DESC = Column(String)
#     CRASH_EVNT_2_CD = Column(Integer)
#     CRASH_EVNT_2_SHORT_DESC = Column(String)
#     CRASH_EVNT_3_CD = Column(Integer)
#     CRASH_EVNT_3_SHORT_DESC = Column(String)
#     CRASH_CAUSE_1_CD = Column(Integer)
#     CRASH_CAUSE_1_SHORT_DESC = Column(String)
#     CRASH_CAUSE_2_CD = Column(Integer) 
#     CRASH_CAUSE_2_SHORT_DESC = Column(String)
#     CRASH_CAUSE_3_CD = Column(Integer)
#     CRASH_CAUSE_3_SHORT_DESC = Column(String)
# from sqlalchemy import create_engine
# engine = create_engine("sqlite:///oregon_crashes.sqlite")
# connection = engine.connect()
# Base.metadata.create_all(engine)
# from sqlalchemy.orm import Session
# session = Session(bind=engine)
# session.commit()
# session.close()