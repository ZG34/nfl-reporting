import sqlite3

import numpy as np
import pandas as pd
import sqlite3 as sql
import openpyxl
import matplotlib.pyplot as plt

# class actively used by users of the GUI application, talking with the final sets of data
class UserConnection:
    def __init__(self, *args, **kwargs):
        self.connection = sql.connect("database_1.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    active_table = "combined2_copy"

    def populate_gui_data(self):
        self.cursor.execute("""SELECT * FROM combined2_copy """)
        data = self.cursor.fetchall()
        return data

    def populate_gui_columns(self):
        name_search = self.cursor.execute("""SELECT * FROM combined2_copy""")
        names = list(map(lambda x: x[0], name_search.description))
        return names

    def populate_yearlist(self):
        query = """
        SELECT DISTINCT(YEAR) 
        FROM combined2_copy"""
        self.cursor.execute(query)
        years = []
        for item in self.cursor.fetchall():
            years.append(item[0])
        return years

    def populate_off_teamlist(self):
        query = """
        SELECT DISTINCT(TEAM)
        FROM combined2_copy
        GROUP BY "TEAM" 
        ORDER BY COUNT("TEAM") DESC """
        self.cursor.execute(query)
        teams = []
        for item in self.cursor.fetchall():
            teams.append(item[0])
        return teams

    def populate_def_teamlist(self):
        query = """
        SELECT DISTINCT("OPP TM")
        FROM combined2_copy
        GROUP BY "OPP TM" 
        ORDER BY COUNT("OPP TM") DESC """
        self.cursor.execute(query)
        teams = []
        for item in self.cursor.fetchall():
            teams.append(item[0])
        return teams

    @staticmethod
    def populate_quarterlist():
        return ["0", "1", "2", "3", "4"]

    def populate_formlist(self):
        query = """
        SELECT DISTINCT("OFF. FORM")
        FROM combined2_copy 
        GROUP BY "OFF. FORM" 
        ORDER BY COUNT("OFF. FORM") DESC"""
        self.cursor.execute(query)
        formations = []
        for item in self.cursor.fetchall():
            formations.append(item[0])
        return formations

    @staticmethod
    def populate_fieldpos():
        return ["Green Zone", "Three Down", "Four Down", "Red Zone"]

    def populate_setlist(self):
        query = """
        SELECT DISTINCT("SET") 
        FROM combined2_copy 
        GROUP BY "SET"
        ORDER BY COUNT("SET") DESC """
        self.cursor.execute(query)
        sets = []
        for item in self.cursor.fetchall():
            sets.append(item[0])
        return sets

    def populate_treelist(self):
        query = """
        SELECT DISTINCT("TREE") 
        FROM combined2_copy 
        GROUP BY "TREE"
        ORDER BY COUNT("TREE") DESC """
        self.cursor.execute(query)
        trees = []
        for item in self.cursor.fetchall():
            trees.append(item[0])
        return trees

    def populate_playtypelist(self):
        query = """
        SELECT DISTINCT("PLAY TYPE") 
        FROM combined2_copy 
        GROUP BY "PLAY TYPE"
        ORDER BY COUNT("PLAY TYPE") DESC """
        self.cursor.execute(query)
        play_types = []
        for item in self.cursor.fetchall():
            play_types.append(item[0])
        return play_types

    def populate_results(self):
        query = """
        SELECT DISTINCT("RESULT")
        FROM combined2_copy 
        GROUP BY "RESULT"
        ORDER BY COUNT ("RESULT") DESC
        """
        self.cursor.execute(query)
        results = []
        for item in self.cursor.fetchall():
            results.append(item[0])
        return results

    def populate_blitzlist(self):
        query = """
        SELECT DISTINCT("BLITZ")
        FROM combined2_copy 
        GROUP BY "BLITZ"
        ORDER BY COUNT ("BLITZ") DESC
        """
        self.cursor.execute(query)
        blitz = []
        for item in self.cursor.fetchall():
            blitz.append(item[0])
        return blitz

    def populate_coverages(self):
        # query = """
        # SELECT DISTINCT("COVERAGE")
        # FROM combined2_copy
        # GROUP BY "COVERAGE"
        # ORDER BY COUNT ("COVERAGE") DESC
        # """
        query1 = """
                SELECT DISTINCT(coverage_type)
                FROM hidden_factors 
                INNER JOIN combined2_copy ON hidden_factors.id=combined2_copy.id
                GROUP BY coverage_type
                ORDER BY COUNT (coverage_type) DESC
                """
        self.cursor.execute(query1)
        coverages = []
        for item in self.cursor.fetchall():
            coverages.append(item[0])
        return coverages

    def populate_def_pers(self):
        query = """
        SELECT DISTINCT("PERS.D")
        FROM combined2_copy 
        GROUP BY "PERS.D"
        ORDER BY COUNT ("PERS.D") DESC
        """
        self.cursor.execute(query)
        packages = []
        for item in self.cursor.fetchall():
            packages.append(item[0])
        return packages

    def populate_shells(self):
        query = """
        SELECT DISTINCT("SHELL")
        FROM combined2_copy 
        GROUP BY "SHELL"
        ORDER BY COUNT ("SHELL") DESC
        """
        self.cursor.execute(query)
        shells = []
        for item in self.cursor.fetchall():
            shells.append(item[0])
        return shells

    def populate_fronts(self):
        query = """
        SELECT DISTINCT("FRONT")
        FROM combined2_copy 
        GROUP BY "FRONT"
        ORDER BY COUNT("FRONT") DESC
        """
        self.cursor.execute(query)
        fronts = []
        for item in self.cursor.fetchall():
            fronts.append(item[0])
        # fronts.pop(0)
        return fronts

    def repop_opp_teams(self, team):
        query = """
        SELECT DISTINCT("OPP TM")
        FROM combined2_copy
        WHERE "TEAM" = (?)"""
        params = [team]
        self.cursor.execute(query, params)
        teams = []
        for item in self.cursor.fetchall():
            teams.append(item[0])
        return teams

    def repop_off_team(self, team):
        query = """
        SELECT DISTINCT("TEAM")
        FROM combined2_copy
        WHERE "OPP TM" = (?)"""
        params = [team]
        self.cursor.execute(query, params)
        teams = []
        for item in self.cursor.fetchall():
            teams.append(item[0])
        return teams

    def complex_filter(
        self,
        year,
        team,
        qt,
        form,
        pos,
        off_set,
        opp_tm,
        tree,
        play_type,
        result,
        blitz,
        coverage,
        dpers,
        shell,
        front,
        down,
        dist,
        opers,
        mtag,
        bstag,
        gain,
        rush,
        conversion,
    ):

        params = [
            year,
            year,
            team,
            team,
            qt,
            qt,
            form,
            form,
            pos,
            pos,
            off_set,
            off_set,
            opp_tm,
            opp_tm,
            tree,
            tree,
            play_type,
            play_type,
            result,
            result,
            blitz,
            blitz,
            coverage,
            coverage,
            dpers,
            dpers,
            shell,
            shell,
            front,
            front,
            down,
            down,
            dist,
            dist,
            opers,
            opers,
            mtag,
            mtag,
            bstag,
            bstag,
            gain,
            gain,
            rush,
            rush,
            conversion,
            conversion,
        ]

        query = """
        SELECT * FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE ((?) IS NULL OR "YEAR"=(?))
        AND ((?) IS NULL OR "TEAM"=(?))
        AND ((?) IS NULL OR "QT"=(?))
        AND ((?) IS NULL OR "OFF. FORM"=(?))
        AND ((?) IS NULL OR "pos zone"=(?))
        AND ((?) IS NULL OR "SET"=(?))
        AND ((?) IS NULL OR "OPP TM"=(?))
        AND ((?) IS NULL OR "TREE"=(?))
        AND ((?) IS NULL OR "PLAY TYPE"=(?))
        AND ((?) IS NULL OR "RESULT"=(?))
        AND ((?) IS NULL OR "BLITZ"=(?))
        AND ((?) IS NULL OR "coverage_type"=(?))
        AND ((?) IS NULL OR "PERS.D"=(?))
        AND ((?) IS NULL OR "SHELL"=(?))
        AND ((?) IS NULL OR "FRONT"=(?))
        AND ((?) IS NULL OR "down"=(?))
        AND ((?) IS NULL OR "Distance"=(?))
        AND ((?) IS NULL OR "PERS.O"=(?))
        AND ((?) IS NULL OR "MAIN TAG"=(?))
        AND ((?) IS NULL OR "BS TAG"=(?))
        AND ((?) IS NULL OR "GAIN"=(?))
        AND ((?) IS NULL OR "RUSH" LIKE ('%' || ? || '%'))
        AND ((?) IS NULL OR "Conversion"=(?))
        """

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def return_team_treecount(
        self,
        team,
        year,
        qt,
        form,
        pos,
        off_set,
        opp_tm,
        tree,
        play_type,
        result,
        blitz,
        coverage,
        dpers,
        shell,
        front,
        down,
        dist,
        opers,
        mtag,
        bstag,
        gain,
        rush,
        conversion,
    ):
        params = [
            team,
            team,
            year,
            year,
            qt,
            qt,
            form,
            form,
            pos,
            pos,
            off_set,
            off_set,
            opp_tm,
            opp_tm,
            tree,
            tree,
            play_type,
            play_type,
            result,
            result,
            blitz,
            blitz,
            coverage,
            coverage,
            dpers,
            dpers,
            shell,
            shell,
            front,
            front,
            down,
            down,
            dist,
            dist,
            opers,
            opers,
            mtag,
            mtag,
            bstag,
            bstag,
            gain,
            gain,
            rush,
            rush,
            conversion,
            conversion,
        ]

        query = """
        SELECT TREE, COUNT(*) 
        FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE ((?) IS NULL OR "TEAM"=(?))
        AND ((?) IS NULL OR "YEAR"=(?))
        AND ((?) IS NULL OR "QT"=(?))
        AND ((?) IS NULL OR "OFF. FORM"=(?))
        AND ((?) IS NULL OR "pos zone"=(?))
        AND ((?) IS NULL OR "SET"=(?))
        AND ((?) IS NULL OR "OPP TM"=(?))
        AND ((?) IS NULL OR "TREE"=(?))
        AND ((?) IS NULL OR "PLAY TYPE"=(?))
        AND ((?) IS NULL OR "RESULT"=(?))
        AND ((?) IS NULL OR "BLITZ"=(?))
        AND ((?) IS NULL OR "coverage_type"=(?))
        AND ((?) IS NULL OR "PERS.D"=(?))
        AND ((?) IS NULL OR "SHELL"=(?))
        AND ((?) IS NULL OR "FRONT"=(?))
        AND ((?) IS NULL OR "down"=(?))
        AND ((?) IS NULL OR "Distance"=(?))
        AND ((?) IS NULL OR "PERS.O"=(?))
        AND ((?) IS NULL OR "MAIN TAG"=(?))
        AND ((?) IS NULL OR "BS TAG"=(?))
        AND ((?) IS NULL OR "GAIN"=(?))
        AND ((?) IS NULL OR "RUSH" LIKE ('%' || ? || '%'))
        AND ((?) IS NULL OR "Conversion"=(?))
        GROUP BY TREE"""
        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def return_team_3rd_downs(
        self,
        team,
        opp_tm,
        year,
        qt,
        form,
        pos,
        off_set,
        tree,
        play_type,
        result,
        blitz,
        coverage,
        dpers,
        shell,
        front,
        down,
        dist,
        opers,
        mtag,
        bstag,
        gain,
        rush,
        conversion,
    ):
        params = [
            team,
            team,
            opp_tm,
            opp_tm,
            year,
            year,
            qt,
            qt,
            form,
            form,
            pos,
            pos,
            off_set,
            off_set,
            tree,
            tree,
            play_type,
            play_type,
            result,
            result,
            blitz,
            blitz,
            coverage,
            coverage,
            dpers,
            dpers,
            shell,
            shell,
            front,
            front,
            down,
            down,
            dist,
            dist,
            opers,
            opers,
            mtag,
            mtag,
            bstag,
            bstag,
            gain,
            gain,
            rush,
            rush,
            conversion,
            conversion,
        ]

        query = """
        SELECT "Main Tag", COUNT(*)
        FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE ((?) IS NULL OR "TEAM"=(?))
        AND ((?) IS NULL OR "OPP TM"=(?))
        AND ((?) IS NULL OR "YEAR"=(?))
        AND ((?) IS NULL OR "QT"=(?))
        AND ((?) IS NULL OR "OFF. FORM"=(?))
        AND ((?) IS NULL OR "pos zone"=(?))
        AND ((?) IS NULL OR "SET"=(?))
        AND ((?) IS NULL OR "TREE"=(?))
        AND ((?) IS NULL OR "PLAY TYPE"=(?))
        AND ((?) IS NULL OR "RESULT"=(?))
        AND ((?) IS NULL OR "BLITZ"=(?))
        AND ((?) IS NULL OR "coverage_type"=(?))
        AND ((?) IS NULL OR "PERS.D"=(?))
        AND ((?) IS NULL OR "SHELL"=(?))
        AND ((?) IS NULL OR "FRONT"=(?))
        AND ((?) IS NULL OR "down"=(?))
        AND ((?) IS NULL OR "Distance"=(?))
        AND ((?) IS NULL OR "PERS.O"=(?))
        AND ((?) IS NULL OR "MAIN TAG"=(?))
        AND ((?) IS NULL OR "BS TAG"=(?))
        AND ((?) IS NULL OR "GAIN"=(?))
        AND ((?) IS NULL OR "RUSH" LIKE ('%' || ? || '%'))
        AND ((?) IS NULL OR "Conversion"=(?))
        AND ("down" = "3rd")
        GROUP BY "Main Tag" """
        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def return_team_run_vs_pass(
        self,
        year,
        team,
        qt,
        form,
        pos,
        off_set,
        opp_tm,
        tree,
        result,
        blitz,
        coverage,
        dpers,
        shell,
        front,
        down,
        dist,
        opers,
        mtag,
        bstag,
        gain,
        rush,
        conversion,
    ):

        params = [
            year,
            year,
            team,
            team,
            qt,
            qt,
            form,
            form,
            pos,
            pos,
            off_set,
            off_set,
            opp_tm,
            opp_tm,
            tree,
            tree,
            result,
            result,
            blitz,
            blitz,
            coverage,
            coverage,
            dpers,
            dpers,
            shell,
            shell,
            front,
            front,
            down,
            down,
            dist,
            dist,
            opers,
            opers,
            mtag,
            mtag,
            bstag,
            bstag,
            gain,
            gain,
            rush,
            rush,
            conversion,
            conversion,
        ]

        query = """
        SELECT "PLAY TYPE" , COUNT(*) 
        FROM combined2_copy 
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE (("PLAY TYPE") IN ("Run", "Pass"))
        AND ((?) IS NULL OR "YEAR"=(?))
        AND ((?) IS NULL OR "TEAM"=(?))
        AND ((?) IS NULL OR "QT"=(?))
        AND ((?) IS NULL OR "OFF. FORM"=(?))
        AND ((?) IS NULL OR "pos zone"=(?))
        AND ((?) IS NULL OR "SET"=(?))
        AND ((?) IS NULL OR "OPP TM"=(?))
        AND ((?) IS NULL OR "TREE"=(?))
        AND ((?) IS NULL OR "RESULT"=(?))
        AND ((?) IS NULL OR "BLITZ"=(?))
        AND ((?) IS NULL OR "coverage_type"=(?))
        AND ((?) IS NULL OR "PERS.D"=(?))
        AND ((?) IS NULL OR "SHELL"=(?))
        AND ((?) IS NULL OR "FRONT"=(?))
        AND ((?) IS NULL OR "down"=(?))
        AND ((?) IS NULL OR "Distance"=(?))
        AND ((?) IS NULL OR "PERS.O"=(?))
        AND ((?) IS NULL OR "MAIN TAG"=(?))
        AND ((?) IS NULL OR "BS TAG"=(?))
        AND ((?) IS NULL OR "GAIN"=(?))
        AND ((?) IS NULL OR "RUSH" LIKE ('%' || ? || '%'))
        AND ((?) IS NULL OR "Conversion"=(?))
        GROUP BY "PLAY TYPE" """
        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def return_team_treecount_df(self, team):
        params = [
            team,
            team,
        ]

        query = """
         SELECT TREE, COUNT(*) 
         FROM combined2_copy 
         WHERE ((?) IS NULL OR "TEAM"=(?))
         GROUP BY TREE"""

        print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

    def return_team_3rds_df(self, team):
        params = [
            team,
            team,
        ]

        query = """
         SELECT "Main Tag", COUNT(*) 
         FROM combined2_copy 
         WHERE ((?) IS NULL OR "TEAM"=(?))
         GROUP BY "Main Tag" """

        print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

    def populate_downs(self):
        query = """
        SELECT DISTINCT(down) 
        FROM hidden_factors
        GROUP BY down
        ORDER BY down ASC"""

        result = self.cursor.execute(query).fetchall()
        result.pop(0)

        return [x[0] for x in result]

    def populate_distance(self):
        query = """
        SELECT DISTINCT(Distance) 
        FROM hidden_factors
        GROUP BY Distance
        ORDER BY Distance + 0 asc"""

        result = self.cursor.execute(query).fetchall()
        result.pop(0)

        return [x[0] for x in result]

    def populate_off_pers(self):
        query = """
        SELECT DISTINCT("PERS.O") 
        FROM combined2_copy
        GROUP BY "PERS.O"
        ORDER BY "PERS.O" ASC"""

        result = self.cursor.execute(query).fetchall()
        result.pop(0)

        return [x[0] for x in result]

    def populate_maintag(self):
        query = """
        SELECT DISTINCT("MAIN TAG") 
        FROM combined2_copy
        GROUP BY "MAIN TAG"
        ORDER BY "MAIN TAG" DESC"""

        result = self.cursor.execute(query).fetchall()

        return [x[0] for x in result]

    def populate_bstag(self):
        query = """
        SELECT DISTINCT("BS TAG") 
        FROM combined2_copy
        GROUP BY "BS TAG"
        ORDER BY "BS TAG" DESC"""

        result = self.cursor.execute(query).fetchall()

        return [x[0] for x in result]

    def report_db_total(self):
        query = """
        SELECT COUNT(*)
        FROM combined2_copy"""

        result = self.cursor.execute(query).fetchall()

        return [x[0] for x in result]

    def populate_gain(self):
        # THIS MAY BE FOR DATA CLEANING STRICTLY. I probably dont want to sort by gain, or do I?
        query = """
        SELECT DISTINCT("GAIN") 
        FROM combined2_copy
        GROUP BY "GAIN"
        ORDER BY "GAIN" + 0 asc"""

        result = self.cursor.execute(query).fetchall()

        return [x[0] for x in result]

    def populate_rushers(self):
        query = """
        SELECT DISTINCT(RUSH)
        FROM combined2_copy
        GROUP BY RUSH 
        ORDER BY RUSH """

        result = self.cursor.execute(query).fetchall()

        return [x[0] for x in result]

    def populate_conversion(self):
        return "True", "False"


if __name__ == "__main__":
    pass
