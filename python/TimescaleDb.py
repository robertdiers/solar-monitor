#!/usr/bin/env python

import psycopg2

conn = "unknown"


# write watts to TimescaleDB
def writeW(key, value):
    write('watts', key, value)


# write voltages to TimescaleDB
def writeV(key, value):
    write('voltages', key, value)


# write temps to TimescaleDB
def writeT(key, value):
    write('temps', key, value)


# write percentages to TimescaleDB
def writeP(key, value):
    write('percentages', key, value)


# write kilowatthours to TimescaleDB
def writeK(key, value):
    write('kilowatthours', key, value)


# write data to TimescaleDB
def write(table, key, value):
    try:
        global conn
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        sql = 'insert into ' + table + ' (time, key, value) values (now(), %s, %s)'
        cur.execute(sql, (key, value,))
        # commit the changes to the database
        conn.commit()
    except Exception as ex:
        print("ERROR: ", ex)
        cur.execute("rollback")
    finally:
        # close the communication with the PostgreSQL
        cur.close()


# write kilowatthours_total to TimescaleDB
def writeKT(key, value):
    write_day('kilowatthours_day', key, value)


# write kilowatthours_counter to TimescaleDB
def writeKTC(key, value):
    write_day('kilowatthours_day_counter', key, value)


# write data to TimescaleDB
def write_day(table, key, value):
    try:
        global conn
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        # sql = 'update '+table+' set value = %s where day = CURRENT_DATE and key = %s'
        sql = 'INSERT INTO ' + table + ' (day, key, value) VALUES (CURRENT_DATE, %s, %s)'
        sql += ' ON CONFLICT (day, key) DO UPDATE SET value = %s;'
        cur.execute(sql, (key, value, value))
        # commit the changes to the database
        conn.commit()
    except Exception as ex:
        print("ERROR: ", ex)
        cur.execute("rollback")
    finally:
        # close the communication with the PostgreSQL
        cur.close()


# read yesterday kilowatthours_total from TimescaleDB
def readKTYesterday(key):
    return read_yesterday('kilowatthours_day', key)


# read yesterday kilowatthours_total from TimescaleDB
def readKTCYesterday(key):
    return read_yesterday('kilowatthours_day_counter', key)


# read yesterday kilowatthours_total from TimescaleDB
def read_yesterday(table, key):
    try:
        global conn
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        sql = 'select coalesce((select value from ' + table + ' where day = (CURRENT_DATE - 1) and key = %s), 0)'
        cur.execute(sql, (key,))
        yesterday = cur.fetchmany(1)
        kwh = yesterday[0][0]
        return kwh
    except Exception as ex:
        print("ERROR: ", ex)
    finally:
        # close the communication with the PostgreSQL
        cur.close()


# exec in db
def exec(sql):
    try:
        global conn
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
    except Exception as ex:
        print("ERROR: ", ex)
        cur.execute("rollback")
    finally:
        # close the communication with the PostgreSQL
        cur.close()


def connect(timescaledb_ip, timescaledb_username, timescaledb_password):
    try:

        # init Timescaledb
        global conn
        conn = psycopg2.connect(
            host=timescaledb_ip,
            database="postgres",
            user=timescaledb_username,
            password=timescaledb_password)

    except Exception as ex:
        print("ERROR: ", ex)


def close():
    global conn
    conn.close()
