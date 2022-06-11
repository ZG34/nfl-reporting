import pandas as pd
import sqlite3 as sql


class PlotConnection:
    def __init__(self, *args, **kwargs):
        self.connection = sql.connect("database_1.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    active_table = "combined2_copy"

    def conversion_dataframe(self):
        query = """
        SELECT Distance, Conversion, COUNT(*)
        FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        GROUP BY Distance, Conversion
        ORDER BY Distance"""

        # print(pd.read_sql_query(query, con=self.connection))

    def return_team_3rds_df(self, team):
        params = [
            team,
            team,
        ]

        query = """
         SELECT "Main Tag", COUNT(*) 
         FROM combined2_copy 
         WHERE ((?) IS NULL OR "TEAM"=(?))
         AND (Down = "3rd")
         GROUP BY "Main Tag" """

        # print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

    def return_gain_vs_dist(self, team):
        params = [
            team,
            team,
        ]

        query = """
         SELECT CAST(Distance AS int) "Distance to Gain" , CAST(Gain AS int) "Gained on Play", COUNT(*) Count, Conversion
         FROM combined2_copy 
         INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
         WHERE ((?) IS NULL OR "TEAM"=(?))
         AND (Distance NOT LIKE "%N/%")
         AND (GAIN NOT LIKE "%N/%")
         AND (Down = "3rd")
         GROUP BY Distance, Gain
         ORDER BY Count"""

        # print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

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
        SELECT "Main Tag", COUNT(*) Count
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

        # print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

    def team_3rd_down_conversions(self, team):
        query = """
        SELECT Conversion, Count(*) Count
        FROM hidden_factors
        INNER JOIN combined2_copy ON hidden_factors.id=combined2_copy.id
        WHERE (?) IS NULL OR "TEAM"=(?)
        AND (down = "3rd")
        AND (Conversion NOT LIKE "%N/%")
        GROUP BY Conversion
        ORDER BY Conversion"""

        params = [team, team]

        # print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

    def team_3rd_down_conversions_filtered(
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
        SELECT CAST(Distance AS int) "Distance to Gain" , CAST(Gain AS int) "Gained on Play", COUNT(*) Count, Conversion
        FROM combined2_copy 
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE ((?) IS NULL OR "TEAM"=(?))
        AND (Distance NOT LIKE "%N/%")
        AND (GAIN NOT LIKE "%N/%")
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
        AND (Down = "3rd")
        GROUP BY Distance, Gain
        ORDER BY Count 
        """

        return pd.read_sql_query(query, params=params, con=self.connection)

    def conversion_rates(self):
        query = """
        SELECT Team, Conversion, Count(*) Count
        FROM hidden_factors
        INNER JOIN combined2_copy ON hidden_factors.id=combined2_copy.id
        WHERE (down = "3rd")
        AND (Conversion NOT LIKE "%N/%")
        GROUP BY Conversion, Team
        ORDER BY Team"""

        # print(pd.read_sql_query(query, con=self.connection))

        return pd.read_sql_query(query, con=self.connection)

    def run_pass_on_3rd(self, team):
        query = """
        SELECT "Play Type" PlayType, Distance, Count(*) "Times Called"
        FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE ("Play Type" = "Run")
        AND ("Down" = "3rd")
        AND ((?) IS NULL OR "TEAM"=(?))
        OR ("Play Type" = "Pass")
        AND ("Down" = "3rd")
        AND ((?) IS NULL OR "TEAM"=(?))
        GROUP BY Distance, PlayType
        ORDER BY Distance DESC """

        params = [team, team, team, team]

        # print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)
        # TODO chart this with a dual-barred bar chart (playcall type on 3rd vs others, by dist?)
        #  https://stackoverflow.com/questions/40877135/plotting-two-columns-of-dataframe-in-seaborn

    def formations_on_3rd(self, team):
        query = """
        SELECT "OFF. FORM" Formation, Count(*) Count
        FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE ("Down" = "3rd") 
        AND ((?) IS NULL OR "TEAM"=(?))
        GROUP BY Formation
        ORDER BY Count"""

        params = [team, team]

        # print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

    def play_tree_3rd(self, team):
        query = """
        SELECT Tree "Play Tree", Count(*) Count
        FROM combined2_copy
        INNER JOIN hidden_factors ON combined2_copy.id=hidden_factors.id
        WHERE ("DOWN" = "3rd")
        AND ((?) IS NULL OR "TEAM"=(?))
        GROUP BY "Play Tree"
        ORDER BY Count
        """

        params = [team, team]

        # print(pd.read_sql_query(query, params=params, con=self.connection))

        return pd.read_sql_query(query, params=params, con=self.connection)

    def expected_3rd_gains(self, team):
        query0 = """
        SELECT COUNT(*), "Play Type" PlayType, avg(Gain)
        FROM combined2_copy
        WHERE (PlayType = "Run")
        OR (PlayType = "Pass")
        GROUP BY PlayType
        ORDER BY avg(Gain)
        """

        params = [team]

        query = """
        SELECT "Play Type" PlayType, CAST(Gain AS int) Gain, CAST(Distance AS int) Distance
        FROM combined2_copy
        INNER JOIN hidden_factors ON hidden_factors.id=combined2_copy.id
        WHERE (PlayType = "Run")
        OR (PlayType = "Pass")
        AND (Down = "3rd")
        AND (TEAM = (?))
        """

        # print(pd.read_sql_query(query, params=params, con=self.connection))
        return pd.read_sql_query(query, params=params, con=self.connection)

    def test(self):
        query = """
        SELECT "OFF. FORM" FROM combined2_copy"""

        print(pd.read_sql_query(query, con=self.connection))


if __name__ == "__main__":
    db = PlotConnection()
    # db.play_tree_3rd('MIA')
    # db.run_pass_on_3rd("MIA")
    # db.test()
    db.expected_3rd_gains("MIA")
