import sqlite3 as sql
import pandas as pd
import db_plotting

PCDB = db_plotting.PlotConnection()

class ReportConnector:
    def __init__(self, *args, **kwargs):
        self.connection = sql.connect("database_1.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

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