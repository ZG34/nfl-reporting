import sqlite3
import pandas as pd
import sqlite3 as sql



# class used for initial generation of data.
class GenerateDatabase:
    def __init__(self, *args, **kwargs):
        self.connection = sql.connect("database_1.db")
        self.cursor = self.connection.cursor()

    def restart_process(self):
        query3 = """CREATE TABLE  IF NOT EXISTS backup_combined AS SELECT * FROM combined2_copy"""
        query4 = """CREATE TABLE IF NOT EXISTS backup_hidden AS SELECT * FROM hidden_factors"""
        query0 = """DROP TABLE IF EXISTS combined2"""
        query1 = """DROP TABLE IF EXISTS combined"""
        query2 = """DROP TABLE IF EXISTS combined2_copy"""
        query5 = """DROP TABLE IF EXISTS hidden_factors"""
        query6 = """DROP TABLE IF EXISTS combined3"""
        self.cursor.execute(query3)
        self.cursor.execute(query4)
        self.cursor.execute(query0)
        self.cursor.execute(query1)
        self.cursor.execute(query2)
        self.cursor.execute(query5)
        self.cursor.execute(query6)

    def excel_to_database(self):
        workbook_2020 = r"D:\Pycharm\NFL_Analysis\excel_data\2020 Charts.xlsx"
        workbook = pd.read_excel(workbook_2020, sheet_name="ALL")
        workbook.to_sql(
            name="2020_all",
            con=self.connection,
            if_exists="replace",
            index=True,
            index_label="play_id",
        )
        self.cursor.execute("""ALTER TABLE '2020_all' ADD COLUMN year DEFAULT '2020'""")

        workbook_2019 = r"D:\Pycharm\NFL_Analysis\excel_data\2019 Charts.xlsx"
        workbook = pd.read_excel(workbook_2019, sheet_name="ALL")
        workbook.to_sql(
            name="2019_all",
            con=self.connection,
            if_exists="replace",
            index=True,
            index_label="play_id",
        )
        self.cursor.execute("""ALTER TABLE '2019_all' ADD COLUMN year DEFAULT '2019'""")

        self.connection.commit()

    def distinct_test(self):
        # this selects columns unique to 2020, which are not included in 2019
        compare1 = """
        SELECT name FROM pragma_table_info('2020_all')
        WHERE name NOT IN 
        (SELECT name FROM pragma_table_info('2019_all'))"""
        # WK, QT, SET, L/R, FS TAG, FS Routes, BS Routes, BS TAG

        compare2 = """
        SELECT name FROM pragma_table_info('2019_all')
        WHERE name NOT IN 
        (SELECT name FROM pragma_table_info('2020_all'))"""
        # OFF. SET, OFF. CALL, B/S is BS Routes

        compare3 = """
                SELECT name FROM pragma_table_info('combined2_copy')
                WHERE name NOT IN 
                (SELECT name FROM pragma_table_info('combined2'))"""

        print(pd.read_sql_query(compare3, con=self.connection))

    def adjust_tables(self):
        # adjusting tables to have columns matched as closely as possible for merge
        try:
            add_2019_quarters = """ALTER TABLE '2019_all' ADD COLUMN QT DEFAULT 1"""
            self.cursor.execute(add_2019_quarters)
            alter_2019_set = (
                """ALTER TABLE '2019_all' RENAME COLUMN "OFF. SET" TO 'SET'"""
            )
            self.cursor.execute(alter_2019_set)
            add_2019_bstag = (
                """ALTER TABLE '2019_all' ADD COLUMN "BS TAG" DEFAULT "N/A" """
            )
            self.cursor.execute(add_2019_bstag)
            add_2019_weeks = """ALTER TABLE '2019_all' ADD COLUMN WK DEFAULT "N/A" """
            self.cursor.execute(add_2019_weeks)
            alter_2019_call = (
                """ALTER TABLE '2019_all' RENAME COLUMN "OFF. CALL" TO "MAIN TAG" """
            )
            self.cursor.execute(alter_2019_call)
            alter_2019_bsroute = (
                """ALTER TABLE '2019_all' RENAME COLUMN "B/S" TO "BS Routes" """
            )
            self.cursor.execute(alter_2019_bsroute)
            add_2019_fsroutes = (
                """ALTER TABLE '2019_all' ADD COLUMN "FS Routes" DEFAULT "N/A" """
            )
            self.cursor.execute(add_2019_fsroutes)
            add_2019_lr = """ALTER TABLE '2019_all' ADD COLUMN "L/R" DEFAULT "N/A" """
            self.cursor.execute(add_2019_lr)

            alter_2020_call = (
                """ALTER TABLE '2020_all' RENAME COLUMN "FS TAG" TO "MAIN TAG" """
            )
            self.cursor.execute(alter_2020_call)

        except sqlite3.OperationalError as e:
            print(e)

        self.connection.commit()

    def merge_tables(self):
        create = """CREATE TABLE IF NOT EXISTS combined2 AS
        SELECT 
        WK, TEAM, "OPP TM", QT, TIME, "D&D", POS, GAIN, "PERS.O", "SET", "OFF. FORM", FIB, MOTN, "PLAY TYPE", TREE, 
        "MAIN TAG", "FS Routes", "BS TAG",
        "BS Routes", "L/R", "TARGET", "D/S", "PERS.D", FRONT, SHELL, COVERAGE, RUSH, BLITZ, GAMES, RESULT,
        YEAR 
        FROM '2019_all'"""

        append = """
        INSERT INTO combined2
        SELECT
        WK, TEAM, "OPP TM", QT, TIME, "D&D", POS, GAIN, "PERS.O", "SET", "OFF. FORM", FIB, MOTN, "PLAY TYPE", TREE, 
        "MAIN TAG", "FS Routes", "BS TAG",
        "BS Routes", "L/R", "TARGET", "D/S", "PERS.D", FRONT, SHELL, COVERAGE, RUSH, BLITZ, GAMES, RESULT,
        YEAR 
        FROM '2020_all'
                """

        self.cursor.execute(create)
        self.cursor.execute(append)
        self.connection.commit()

    def remove_old_tables(self):
        query1 = """DROP TABLE IF EXISTS "2019_all" """
        query2 = """DROP TABLE IF EXISTS "2020_all" """
        self.cursor.execute(query1)
        self.cursor.execute(query2)

    def clean_data(self):
        dropcombined = """DROP TABLE IF EXISTS combined2"""
        # self.cursor.execute(dropcombined)

        query0 = """
        CREATE TABLE IF NOT EXISTS combined2_copy
        AS SELECT * FROM combined2"""
        self.cursor.execute(query0)

        try:
            pos_zone = """ALTER TABLE combined2 ADD COLUMN "pos zone" """
            self.cursor.execute(pos_zone)
        except sqlite3.OperationalError as e:
            print(e)

        def add_positionquery():
            query2 = """
            UPDATE combined2
            SET "pos zone" = ("Red Zone")
            WHERE ("POS" BETWEEN '0' and '20')"""

            query3 = """
            UPDATE combined2
            SET "pos zone" = ("Green Zone") 
            WHERE ("POS" BETWEEN '-25' and '-1')"""

            query4 = """
            UPDATE combined2
            SET "pos zone" = ("Three Down")
            WHERE ("POS" BETWEEN '-49' and '-26')
            OR ("POS" BETWEEN '46' and '50')
            """

            query5 = """
            UPDATE combined2
            SET "pos zone" = ("Four Down")
            WHERE ("POS" BETWEEN '21' and '45')"""

            self.cursor.execute(query2)
            self.cursor.execute(query3)
            self.cursor.execute(query4)
            self.cursor.execute(query5)

        add_positionquery()

        def adjust_playtype():
            query16 = """
            UPDATE combined2
            SET "PLAY TYPE" = ("Run")
            WHERE "PLAY TYPE" LIKE "%r%" COLLATE NOCASE """
            self.cursor.execute(query16)

            query17 = """
            UPDATE combined2
            SET "PLAY TYPE" = ("Pass")
            WHERE "PLAY TYPE" LIKE "%pa%" COLLATE NOCASE """
            self.cursor.execute(query17)

            query18 = """
            UPDATE combined2
            SET "PLAY TYPE" = ("Punt")
            WHERE "PLAY TYPE" LIKE "%pu%" COLLATE NOCASE"""
            self.cursor.execute(query18)

            query19 = """
            UPDATE combined2
            SET "PLAY TYPE" = ("No-play")
            WHERE "PLAY TYPE" LIKE "%np%" COLLATE NOCASE"""
            self.cursor.execute(query19)

            query20 = """
            UPDATE combined2
            SET "PLAY TYPE" = ("Field Goal")
            WHERE "PLAY TYPE" LIKE "%FG%" """
            self.cursor.execute(query20)

        adjust_playtype()

        def adjust_tree():
            query6 = """
                    UPDATE combined2
                    SET "TREE" = ("Gap")
                    WHERE "TREE" LIKE "%G%" COLLATE NOCASE """
            self.cursor.execute(query6)

            query7 = """
                    UPDATE combined2
                    SET "TREE" = ("Zone") 
                    WHERE ("TREE" = ("Z"))
                    OR ("TREE" = ("Z "))"""
            self.cursor.execute(query7)

            query8 = """
                    UPDATE combined2
                    SET "TREE" = ("Screen") 
                    WHERE "TREE" = ("SC")"""
            self.cursor.execute(query8)

            query9 = """
                    UPDATE combined2 
                    SET "TREE" = ("Qk Pass")
                    WHERE ("TREE" LIKE "%QK%" COLLATE NOCASE)
                    OR ("TREE" = ("QL"))"""
            self.cursor.execute(query9)

            query10 = """
                    UPDATE combined2
                    SET "TREE" = ("Read") 
                    WHERE "TREE" = ("R")"""
            self.cursor.execute(query10)

            query11 = """
                    UPDATE combined2
                    SET "TREE" = ("Dropback") 
                    WHERE ("TREE" LIKE "%db%" COLLATE NOCASE)
                    OR ("TREE" LIKE "%v%" COLLATE NOCASE) """
            self.cursor.execute(query11)

            query12 = """
                    UPDATE combined2
                    SET "TREE" = ("Play Action")
                    WHERE ("TREE" = "PA" COLLATE NOCASE)
                    OR ("TREE" = " PA" COLLATE NOCASE)
                    OR ("TREE" = "PA " COLLATE NOCASE) """
            self.cursor.execute(query12)

            query13 = """
                    UPDATE combined2
                    SET "TREE" = ("Boot Play Action") 
                    WHERE "TREE" = ("PA B")"""
            self.cursor.execute(query13)

            query14 = """
                    UPDATE combined2
                    SET "TREE" = ("Draw") 
                    WHERE "TREE" = ("D")"""
            self.cursor.execute(query14)

            query15 = """
                    UPDATE combined2
                    SET "TREE" = ("Screen Play Action") 
                    WHERE "TREE" = ("PA SC")"""
            self.cursor.execute(query15)

            query21 = """
            UPDATE combined2
            SET "TREE" = ("Sprint Out")
            WHERE "TREE" LIKE "%SO%" COLLATE NOCASE"""
            self.cursor.execute(query21)

            query22 = """
            UPDATE combined2
            SET "TREE" = ("Option")
            WHERE "TREE" = "O" COLLATE NOCASE """
            self.cursor.execute(query22)

            query23 = """
            UPDATE combined2 
            SET "TREE" = ("?")
            WHERE "TREE" = ("??")"""
            self.cursor.execute(query23)

        adjust_tree()

        def adjust_results():
            query24 = """
            UPDATE combined2
            SET "RESULT" = ("Touchdown")
            WHERE ("RESULT" LIKE "%td%" COLLATE NOCASE)
            OR ("RESULT" LIKE "%tb%" COLLATE NOCASE)"""
            self.cursor.execute(query24)

            query25 = """
            UPDATE combined2
            SET "RESULT" = ("Penalty")
            WHERE ("RESULT" LIKE "%pen%" COLLATE NOCASE)
            OR ("RESULT" LIKE "%ill%" COLLATE NOCASE)"""
            self.cursor.execute(query25)

            query26 = """
            UPDATE combined2
            SET "RESULT" = ("Run") 
            WHERE "RESULT" LIKE "%rush%" COLLATE NOCASE"""
            self.cursor.execute(query26)

            query27 = """
            UPDATE combined2
            SET "RESULT" = ("Completion")
            WHERE "RESULT" LIKE "%comp%" COLLATE NOCASE"""
            self.cursor.execute(query27)

            query28 = """
            UPDATE combined2 
            SET "RESULT" = ("Incomplete") 
            WHERE "RESULT" LIKE "%inc%" COLLATE NOCASE"""
            self.cursor.execute(query28)

            query29 = """
            UPDATE combined2
            SET "RESULT" = ("QB Scramble")
            WHERE "RESULT" LIKE "%scramble%" COLLATE NOCASE"""
            self.cursor.execute(query29)

            query31 = """
            UPDATE combined2
            SET "RESULT" = ("Fumble")
            WHERE "RESULT" LIKE "%fumble%" """
            self.cursor.execute(query31)

            query30 = """
            UPDATE combined2
            SET "RESULT" = ("Sack")
            WHERE "RESULT" LIKE "%sack%" COLLATE NOCASE"""
            self.cursor.execute(query30)

            query32 = """
            UPDATE combined2
            SET "RESULT" = ("Interception")
            WHERE "RESULT" LIKE "%int%" COLLATE NOCASE"""
            self.cursor.execute(query32)

            query33 = """
            UPDATE combined2
            SET "RESULT" = ("Field Goal")
            WHERE ("RESULT" LIKE "%fg%" COLLATE NOCASE)
            OR ("GAIN" LIKE "%fg%" COLLATE NOCASE)"""
            self.cursor.execute(query33)

            query34 = """
            UPDATE combined2
            SET "RESULT" = ("No Play")
            WHERE ("RESULT" LIKE "%np%" COLLATE NOCASE)
            OR ("PLAY TYPE" LIKE "No-Play")"""
            self.cursor.execute(query34)

            query35 = """
            UPDATE combined2
            SET "RESULT" = ("Punt") 
            WHERE ("RESULT" LIKE "%punt%" COLLATE NOCASE)
            OR ("GAIN" LIKE "%punt%" COLLATE NOCASE) """
            self.cursor.execute(query35)

            query36 = """UPDATE combined2 
            SET "PLAY TYPE" = ("Spec. Teams")
            WHERE ("RESULT" LIKE ("Punt"))
            OR ("RESULT" LIKE ("%Field Goal%"))
            OR ("PLAY TYPE" LIKE ("Field Goal"))"""

            self.cursor.execute(query36)

            query37 = """
            UPDATE combined2
            SET "RESULT" = " """

            # FIXME all combobox results which return NONE, instead fix them to return accurate data if possible
            #  play type for FG/Punt may be NONE, change tag to ST or something.

            try:
                query38 = """ALTER TABLE combined2 ADD COLUMN "down" """
                self.cursor.execute(query38)
            except sqlite3.OperationalError as e:
                print(e)

        adjust_results()

        def add_down_query():
            query39 = """
            UPDATE combined2
            SET "down" = ("1st, New Possession")
            WHERE ("D&D" LIKE "%P%")"""
            self.cursor.execute(query39)

            query40 = """
            UPDATE combined2
            SET "down" = ("1st")
            WHERE ("D&D" LIKE "%1&%")"""
            self.cursor.execute(query40)

            query41 = """
            UPDATE combined2
            SET "down" = ("2nd")
            WHERE ("D&D" LIKE "%2&%")"""
            self.cursor.execute(query41)

            query42 = """
            UPDATE combined2
            SET "down" = ("3rd")
            WHERE ("D&D" LIKE "%3&%")"""
            self.cursor.execute(query42)

            query43 = """
            UPDATE combined2
            SET "down" = ("4th")
            WHERE ("D&D" LIKE "%4&%")"""
            self.cursor.execute(query43)

        add_down_query()

        self.connection.commit()

    def split_table(self):
        query = """DROP TABLE IF EXISTS "combined2_copy" """
        self.cursor.execute(query)

        query0 = """
        CREATE TABLE IF NOT EXISTS combined2_copy 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, WK, TEAM, "OPP TM", QT, TIME, "D&D", POS, 
        GAIN, "PERS.O", "SET", "OFF. FORM", FIB, MOTN, "PLAY TYPE", TREE, 
        "MAIN TAG", "FS Routes", "BS TAG",
        "BS Routes", "L/R", "TARGET", "D/S", "PERS.D", FRONT, SHELL, COVERAGE, RUSH, BLITZ, GAMES, RESULT,
        "YEAR", "pos zone", "down") """
        self.cursor.execute(query0)

        query1 = """
        INSERT INTO combined2_copy 
        (WK, TEAM, "OPP TM", QT, TIME, "D&D", POS, 
        GAIN, "PERS.O", "SET", "OFF. FORM", FIB, MOTN, "PLAY TYPE", TREE, 
        "MAIN TAG", "FS Routes", "BS TAG",
        "BS Routes", "L/R", "TARGET", "D/S", "PERS.D", FRONT, SHELL, COVERAGE, RUSH, BLITZ, GAMES, RESULT,
        "YEAR", "pos zone", "down") 
        SELECT 
        WK, TEAM, "OPP TM", QT, TIME, "D&D", POS, 
        GAIN, "PERS.O", "SET", "OFF. FORM", FIB, MOTN, "PLAY TYPE", TREE, 
        "MAIN TAG", "FS Routes", "BS TAG",
        "BS Routes", "L/R", "TARGET", "D/S", "PERS.D", FRONT, SHELL, COVERAGE, RUSH, BLITZ, GAMES, RESULT,
        "YEAR", "pos zone", "down" 
        FROM combined2"""
        self.cursor.execute(query1)

        # print(pd.read_sql_query(sql="SELECT * FROM combined2_copy", con=self.connection))

        query3 = """
        CREATE TABLE IF NOT EXISTS "hidden_factors" AS SELECT
        id, "pos zone", "down" FROM combined2_copy """
        self.cursor.execute(query3)

        query4 = """
        ALTER TABLE combined2_copy DROP COLUMN "pos zone" """
        self.cursor.execute(query4)

        query5 = """
        ALTER TABLE combined2_copy DROP COLUMN "down" """
        self.cursor.execute(query5)

        self.connection.commit()

    def clean_data_continued(self):
        def adjust_coverage():
            try:
                query1 = """
                ALTER TABLE hidden_factors ADD COLUMN "coverage_type" """
                self.cursor.execute(query1)
            except sqlite3.OperationalError as e:
                pass

            query2 = """
            UPDATE hidden_factors
            FROM combined2_copy 
            SET hidden_factors.coverage_type = ("C3")
            WHERE (combined2_copy.COVERAGE LIKE "%3%")
            AND (combined2_copy.id = hidden_factors.id) """
            # self.cursor.execute(query2)

            query5 = """
            UPDATE hidden_factors
            SET coverage_type = (SELECT "COVERAGE" FROM combined2_copy
            WHERE combined2_copy.id = hidden_factors.id)"""
            self.connection.execute(query5)

            query6 = """
            UPDATE hidden_factors
            SET coverage_type = ("C3")
            WHERE coverage_type LIKE ("%3%") """
            self.cursor.execute(query6)

            query7 = """
            UPDATE hidden_factors
            SET coverage_type = ("C1")
            WHERE coverage_type LIKE ("%C1%") COLLATE NOCASE"""
            self.cursor.execute(query7)

            query8 = """
            UPDATE hidden_factors
            SET coverage_type = ("C2")
            WHERE coverage_type LIKE ("%C2%") COLLATE NOCASE """
            self.cursor.execute(query8)

            query3 = """
            SELECT * FROM hidden_factors """
            # print(pd.read_sql_query(query3, con=self.connection))

            query4 = """
            SELECT id, COVERAGE FROM combined2_copy
            WHERE combined2_copy.COVERAGE LIKE "%3%" """
            # print(pd.read_sql_query(query4, con=self.connection))

        adjust_coverage()

        def adjust_shells():
            query1 = """
            UPDATE combined2_copy
            SET SHELL = ("2-High")
            WHERE SHELL LIKE "%2%" COLLATE NOCASE"""
            self.cursor.execute(query1)

            query2 = """
            UPDATE combined2_copy
            SET SHELL = ("1-High")
            WHERE SHELL LIKE "%1%" COLLATE NOCASE """
            self.cursor.execute(query2)

            query3 = """
            UPDATE combined2_copy
            SET SHELL = ("Goal Line")
            WHERE (SHELL LIKE "%gl%" COLLATE NOCASE)
            OR (SHELL LIKE "%goal%" COLLATE NOCASE) """
            self.cursor.execute(query3)

            query4 = """
            UPDATE combined2_copy
            SET SHELL = ("0-High")
            WHERE SHELL LIKE "%0%" """
            self.cursor.execute(query4)

            query5 = """
            UPDATE combined2_copy
            SET SHELL = ("3-High")
            WHERE SHELL LIKE "%3%" """
            self.cursor.execute(query5)

            query6 = """
            UPDATE combined2_copy
            SET SHELL = ("4-High")
            WHERE SHELL LIKE "%4%" """
            self.cursor.execute(query6)

        adjust_shells()

        def adjust_pers():
            query1 = """
            UPDATE combined2_copy
            SET "PERS.O" = ("00") 
            WHERE "PERS.O" LIKE "%00%" """
            self.cursor.execute(query1)

            query2 = """
            UPDATE combined2_copy
            SET "PERS.O" = ("01")
            WHERE "PERS.O" LIKE "01%" """
            self.cursor.execute(query2)

            query3 = """
            UPDATE combined2_copy
            SET "PERS.O" = ("02") 
            WHERE "PERS.O" LIKE "02%" """
            self.cursor.execute(query3)

            query4 = """
            UPDATE combined2_copy
            SET "PERS.O" = ("10") 
            WHERE "PERS.O" LIKE "10%" """
            self.cursor.execute(query4)

            query5 = """
            UPDATE combined2_copy
            SET "PERS.O" = "11" 
            WHERE ("PERS.O" LIKE "11%")
            OR ("PERS.O" LIKE " 11%")"""
            self.cursor.execute(query5)

            query6 = """
            UPDATE combined2_copy
            SET "PERS.O" = "12" 
            WHERE ("PERS.O" LIKE "12%")
            OR ("PERS.O" LIKE " 12%")"""
            self.cursor.execute(query6)

            query7 = """
            UPDATE combined2_copy
            SET "PERS.O" = "13" 
            WHERE ("PERS.O" LIKE "13%")"""
            self.cursor.execute(query7)

            query8 = """UPDATE combined2_copy
            SET "PERS.O" = "20"
            WHERE ("PERS.O" LIKE "20%") """
            self.cursor.execute(query8)

            query9 = """
            UPDATE combined2_copy
            SET "PERS.O" = "21" 
            WHERE ("PERS.O" LIKE "21%")
            OR ("PERS.O" LIKE " 21%") """
            self.cursor.execute(query9)

            query10 = """
            UPDATE combined2_copy
            SET "PERS.O" = "22" 
            WHERE ("PERS.O" LIKE "22%") """
            self.cursor.execute(query10)

            query11 = """
            UPDATE combined2_copy
            SET "PERS.O" = "23"
            WHERE ("PERS.O" LIKE "23%")"""
            self.cursor.execute(query11)

        adjust_pers()

        def adjust_maintags():
            query1 = """
            UPDATE combined2_copy
            SET "MAIN TAG" = LOWER("MAIN TAG")"""
            self.cursor.execute(query1)

        adjust_maintags()

        def adjust_gains():
            query11 = """DROP TABLE IF EXISTS temp1"""
            self.cursor.execute(query11)

            query0 = """
            UPDATE combined2_copy
            SET "GAIN" = "N/A" 
            WHERE ("GAIN" LIKE "%P%" COLLATE NOCASE)
            OR ("GAIN" LIKE "%I%" COLLATE NOCASE) 
            OR ("GAIN" LIKE "%F%" COLLATE NOCASE)
            OR ("RESULT" LIKE "%Interception%" COLLATE NOCASE)"""
            self.cursor.execute(query0)

            query1 = """
            CREATE TABLE temp1 AS SELECT id, "GAIN"
            FROM combined2_copy
            """
            self.cursor.execute(query1)

            # query3 = """
            # UPDATE temp1
            # SET "GAIN" = SUBSTR("GAIN", 3, -2)
            # WHERE "GAIN" NOT LIKE "%(%" """
            # self.cursor.execute(query3)

            query2 = """
            UPDATE temp1
            SET "GAIN" = TRIM(SUBSTR("GAIN", INSTR("GAIN", "(")+1), ')')
            WHERE "GAIN" LIKE "%(%" """
            self.connection.execute(query2)

            query5 = """
            UPDATE combined2_copy
            SET "GAIN" = temp1.GAIN
            FROM temp1
            WHERE combined2_copy.id=temp1.id"""
            self.cursor.execute(query5)

            query6 = """
            UPDATE combined2_copy
            SET "GAIN" = "15" 
            WHERE "GAIN" = "+15" """
            self.cursor.execute(query6)

            query7 = """
            UPDATE combined2_copy
            SET "GAIN" = "5" 
            WHERE "GAIN" = "0, 5" """
            self.cursor.execute(query7)

            self.cursor.execute(query11)

        adjust_gains()

        def adjust_results():
            query1 = """
            UPDATE combined2_copy
            SET "RESULT" = "Penalty" 
            WHERE ("RESULT" = "Incomplete")
            AND (CAST(GAIN as INTEGER) != 0) """
            self.cursor.execute(query1)

            query2 = """
            UPDATE combined2_copy
            SET "RESULT" = "Penalty" 
            WHERE ("RESULT" = "No Play")"""
            self.cursor.execute(query2)

        adjust_results()

        self.connection.commit()

    def third_down_generation(self):
        query12 = """
        UPDATE combined2_copy
        SET "D&D" = "2&7" 
        WHERE "D&D" = "272" """
        self.cursor.execute(query12)

        query13 = """
        UPDATE combined2_copy
        SET "D&D" = "3&14" 
        WHERE "D&D" = "3714" """
        self.cursor.execute(query13)

        try:
            query1 = """
            ALTER TABLE hidden_factors ADD COLUMN "Distance" INTEGER"""
            self.cursor.execute(query1)
        except sqlite3.OperationalError as e:
            pass

        query4 = """
        CREATE TABLE IF NOT EXISTS temp1 AS SELECT id, SUBSTR("D&D", INSTR("D&D","&")+1) as Dist
        FROM combined2_copy"""
        self.cursor.execute(query4)

        query7 = """
        UPDATE hidden_factors
        SET Distance = temp1.Dist
        FROM temp1
        WHERE hidden_factors.id = temp1.id"""
        self.cursor.execute(query7)

        try:
            query9 = """ALTER TABLE hidden_factors ADD COLUMN "Conversion" INTEGER"""
            self.cursor.execute(query9)
        except sqlite3.OperationalError as e:
            pass

        query6 = """DROP TABLE IF EXISTS temp1"""
        self.cursor.execute(query6)

        query10 = """
        UPDATE hidden_factors 
        SET "Conversion" = True
        FROM combined2_copy
        WHERE (hidden_factors.id=combined2_copy.id)
        AND (CAST(combined2_copy.GAIN as INTEGER) >= CAST(hidden_factors.Distance as INTEGER)) """
        self.cursor.execute(query10)

        query11 = """
        UPDATE hidden_factors 
        SET "Conversion" = False
        FROM combined2_copy
        WHERE (hidden_factors.id=combined2_copy.id)
        AND (CAST(combined2_copy.GAIN as INTEGER) < CAST(hidden_factors.Distance as INTEGER)) """
        self.cursor.execute(query11)

        self.connection.commit()

    def testing(self):
        query1 = """
            SELECT DOWN, COUNT(*)
            FROM hidden_factors, combined2_copy
            WHERE hidden_factors.id = 322
            """

        # print(pd.read_sql_query(query1, con=self.connection))

        query2 = """
        SELECT * 
        FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id"""
        # print(pd.read_sql_query(query2, con=self.connection))

        query3 = """
        SELECT "pos zone", count(*)
        FROM hidden_factors
        INNER JOIN combined2_copy ON hidden_factors.id=combined2_copy.id
        WHERE TEAM="TB" 
        GROUP BY "pos zone" """
        # print(pd.read_sql_query(query3, con=self.connection))

        query4 = """
        SELECT id, SUBSTR("D&D", INSTR("D&D","&")+1)
        FROM combined2_copy"""
        # print(pd.read_sql_query(query4, con=self.connection))

        query5 = """SELECT id, "PERS.O" FROM combined2_copy
        WHERE ("PERS.O" LIKE "12%")
        AND ("PERS.O" NOT LIKE "%T%" COLLATE NOCASE) """
        # print(pd.read_sql_query(query5, con=self.connection))

        query6 = """
        SELECT combined2_copy.id, GAIN 
        FROM combined2_copy
        INNER JOIN hidden_factors ON hidden_factors.id=combined2_copy.id
        WHERE ("GAIN" > "Distance")
        AND ("Down" = "3rd") """
        # print(pd.read_sql_query(query6, con=self.connection))

        query7 = """SELECT id, SUBSTR("D&D", INSTR("D&D","&")+1) as Dist
        FROM combined2_copy"""
        # print(pd.read_sql_query(query7, con=self.connection))

        query8 = """SELECT id, SUBSTR("GAIN", 3, -2) as Gain
        FROM combined2_copy
        WHERE "GAIN" NOT LIKE "%(%" """
        # print(pd.read_sql_query(query8, con=self.connection))

        query9 = """
        SELECT id, TRIM(SUBSTR("GAIN", INSTR("GAIN", "(")+1), ')') as Gn
        FROM combined2_copy
        WHERE "GAIN" LIKE "%(%" """
        # print(pd.read_sql_query(query9, con=self.connection))

        query10 = """SELECT hidden_factors.Distance, hidden_factors.conversion, 
        combined2_copy.GAIN FROM hidden_factors
        INNER JOIN combined2_copy ON hidden_factors.id=combined2_copy.id"""
        # print(pd.read_sql_query(query10, con=self.connection))

        query11 = """
        SELECT * FROM hidden_factors 
        WHERE (Conversion != 1)
        AND (Conversion != 0)"""
        print(pd.read_sql_query(query11, con=self.connection))


if __name__ == "__main__":
    db = GenerateDatabase()
    db.restart_process()
    db.excel_to_database()
    db.adjust_tables()
    db.merge_tables()
    db.remove_old_tables()
    db.clean_data()
    db.split_table()
    db.clean_data_continued()
    db.third_down_generation()

    # db.distinct_test()
    # db.testing()
