import os.path
import sys
from sys import exit as sys_exit
import tkinter.ttk as ttk
import tkinter as tk

from ctypes import windll
user32 = windll.user32
user32.SetProcessDPIAware()

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import time

from db_access import UserConnection
from db_plotting import PlotConnection
from third_down_reporting import ThirdDowns

import db_generate

def generate_database():
    dbgen = db_generate.GenerateDatabase()
    dbgen.restart_process()
    dbgen.excel_to_database()
    dbgen.adjust_tables()
    dbgen.merge_tables()
    dbgen.remove_old_tables()
    dbgen.clean_data()
    dbgen.split_table()
    dbgen.clean_data_continued()
    dbgen.third_down_generation()

# generate_database()

UCDB = UserConnection()
PCDB = PlotConnection()

BASE_FONT = ("Times New Roman", 10)


class WindowManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        style = ttk.Style()
        style.theme_use("winnative")

        labelframe_styling = ttk.Style()
        labelframe_styling.configure(
            "my.TLabelframe", background="#E7F1F6", font=BASE_FONT
        )

        button_styling = ttk.Style()
        button_styling.configure("my.TButton", font=BASE_FONT)

        label_styling = ttk.Style()
        label_styling.configure("my.TLabel", font=BASE_FONT)

        tk.Tk.wm_title(self, "Playmaker Reporting")

        container = tk.Frame(self)
        container.grid_configure(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (ReportMain, DatabaseGenerator,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ReportMain)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="placeholder", command=lambda: print("placeholder"))

        filemenu.add_command(label="Exit", command=sys_exit)

        tk.Tk.config(self, menu=filemenu)


    # method for raising new pages (frames)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<Raised>>")


# FilterTemplate is used to create instances of ComboBoxes for the filtering of columns on the LandingPage
# This is to reduce total lines of code required. CURRENTLY LOSING A BIT OF FUNCTIONALITY. Is that worth it?
class FilterTemplate(WindowManager):
    def __init__(self, *, frame, label, column, values, row=0, width=10):
        self.template_label = ttk.Label(frame, text=label)
        self.template_label.grid(row=row, column=column, pady=5, padx=5, sticky="sw")

        self.template_var = tk.StringVar()
        self.template_filter = ttk.Combobox(
            frame, textvariable=self.template_var, width=width
        )
        self.template_filter["state"] = "readonly"
        self.template_filter.grid(row=row + 1, column=column, padx=5, pady=5)
        self.template_filter["values"] = values

        self.new_value = None

        # method made to be bound on selection, storing actual value, to be sent up the chain
        def get_value(event=None):
            value = self.template_filter.get()
            self.new_value = value

        self.template_filter.bind("<<ComboboxSelected>>", get_value)

    # takes new_value and sends it up the chain to be interpreted by SQL at a later date
    def send_value(self, event=None):
        if self.new_value == "":
            return None
        else:
            return self.new_value

    def clear_value(self):
        self.template_filter.set("")
        self.new_value = None

    # TODO how can i make this refresh other comboboxes based on currently identified active box selection?
    def update_selections(self, event=None):
        print(self.template_label.info)
        print(self.template_label.cget("text"))


class ReportMain(tk.Frame, FilterTemplate):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.geometry("1700x750")
        # tk.Frame.attributes("-fullscreen", True)
        # app.geometry("1800x750")
        # app.attributes("-fullscreen", True)

        # self.summary_frame = ttk.Labelframe(self, text="Result Summary", relief='ridge', style="my.TLabelframe",)
        # self.summary_frame.grid(row=0, column=4)

        self.general_frame = ttk.Labelframe(
            self, text="General Filters", relief="ridge", style="my.TLabelframe"
        )
        self.general_frame.grid(row=0, column=0, ipady=5, ipadx=5, rowspan=3)

        self.offensive_frame = ttk.Labelframe(
            self, text="Offensive Filters", relief="ridge", style="my.TLabelframe"
        )
        self.offensive_frame.grid(row=0, column=1, ipady=5, ipadx=5, rowspan=3)

        self.defense_frame = ttk.Labelframe(
            self, text="Defensive Filters", relief="ridge", style="my.TLabelframe"
        )
        self.defense_frame.grid(row=0, column=2, ipady=5, ipadx=5, rowspan=3)

        self.button_frame = ttk.Labelframe(self, relief="ridge", style="my.TLabelframe")
        self.button_frame.grid(row=0, column=3, ipadx=5, ipady=5)

        self.year_filter = FilterTemplate(
            frame=self.general_frame,
            label="Year",
            values=UCDB.populate_yearlist(),
            column=0,
        )
        self.field_pos_filter = FilterTemplate(
            frame=self.general_frame,
            label="Field Position",
            values=UCDB.populate_fieldpos(),
            column=4,
        )
        self.result_filter = FilterTemplate(
            frame=self.general_frame,
            label="Result",
            values=UCDB.populate_results(),
            column=5,
            width=13,
        )

        self.formation_filter = FilterTemplate(
            frame=self.offensive_frame,
            label="Formation",
            values=UCDB.populate_formlist(),
            column=0,
            width=15,
        )
        self.set_filter = FilterTemplate(
            frame=self.offensive_frame,
            label="Set",
            values=UCDB.populate_setlist(),
            column=1,
        )
        self.playtype_filter = FilterTemplate(
            frame=self.offensive_frame,
            label="Play Type",
            values=UCDB.populate_playtypelist(),
            column=2,
        )
        self.tree_filter = FilterTemplate(
            frame=self.offensive_frame,
            label="Play Tree",
            values=UCDB.populate_treelist(),
            column=3,
        )

        self.shell_filter = FilterTemplate(
            frame=self.defense_frame,
            label="Shell",
            values=UCDB.populate_shells(),
            column=1,
        )
        self.coverage_filter = FilterTemplate(
            frame=self.defense_frame,
            label="Coverage",
            values=UCDB.populate_coverages(),
            column=2,
            width=15,
        )
        self.blitz_filter = FilterTemplate(
            frame=self.defense_frame,
            label="Blitz",
            values=UCDB.populate_blitzlist(),
            column=4,
        )
        self.def_pers_filter = FilterTemplate(
            frame=self.defense_frame,
            label="Personnel",
            values=UCDB.populate_def_pers(),
            column=0,
            width=8,
        )
        self.front_filter = FilterTemplate(
            frame=self.defense_frame,
            label="Front",
            values=UCDB.populate_fronts(),
            column=3,
        )
        self.down_filter = FilterTemplate(
            frame=self.general_frame,
            label="Down",
            values=UCDB.populate_downs(),
            column=0,
            row=2,
        )
        self.dist_filter = FilterTemplate(
            frame=self.general_frame,
            label="Distance",
            values=UCDB.populate_distance(),
            column=1,
            row=2,
        )
        self.pers_filter = FilterTemplate(
            frame=self.offensive_frame,
            label="Personnel",
            values=UCDB.populate_off_pers(),
            column=0,
            row=2,
        )
        self.main_tag = FilterTemplate(
            frame=self.offensive_frame,
            label="Playcall",
            values=UCDB.populate_maintag(),
            column=1,
            row=2,
        )
        self.backside_call = FilterTemplate(
            frame=self.offensive_frame,
            label="Backside Tag",
            values=UCDB.populate_bstag(),
            column=2,
            row=2,
        )
        self.gain_filter = FilterTemplate(
            frame=self.general_frame,
            label="Gained Yds",
            values=UCDB.populate_gain(),
            column=2,
            row=2,
        )
        self.rush_filter = FilterTemplate(
            frame=self.defense_frame,
            label="Rushers",
            values=UCDB.populate_rushers(),
            column=4,
        )
        self.conversion_filter = FilterTemplate(
            frame=self.general_frame,
            label="Conversion",
            values=UCDB.populate_conversion(),
            column=3,
            row=2,
        )

        filter_widgets = [
            self.year_filter,
            self.field_pos_filter,
            self.result_filter,
            self.formation_filter,
            self.set_filter,
            self.tree_filter,
            self.playtype_filter,
            self.def_pers_filter,
            self.blitz_filter,
            self.coverage_filter,
            self.shell_filter,
            self.front_filter,
            self.down_filter,
            self.dist_filter,
            self.pers_filter,
            self.main_tag,
            self.backside_call,
            self.gain_filter,
            self.rush_filter,
            self.conversion_filter,
        ]

        self.quarter_label = ttk.Label(self.general_frame, text="Quarter")
        self.quarter_label.grid(row=0, column=3, pady=5, padx=5, sticky="sw")
        self.quarter_var = tk.StringVar()
        self.quarter_var.set(0)
        self.filter_quarter = ttk.Combobox(
            self.general_frame, textvariable=self.quarter_var, width=10
        )
        self.filter_quarter["state"] = "readonly"
        self.filter_quarter.grid(row=1, column=3, padx=5, pady=5)
        self.filter_quarter["values"] = UCDB.populate_quarterlist()

        self.off_team_label = ttk.Label(self.general_frame, text="Offense Team")
        self.off_team_label.grid(row=0, column=1, pady=5, padx=5, sticky="sw")
        self.off_var = tk.StringVar()
        self.off_team_filter = ttk.Combobox(
            self.general_frame, textvariable=self.off_var, width=10
        )
        self.off_team_filter["state"] = "readonly"
        self.off_team_filter.grid(row=1, column=1, padx=5, pady=5)
        self.off_team_filter["values"] = UCDB.populate_off_teamlist()

        self.def_team_label = ttk.Label(self.general_frame, text="Defense Team")
        self.def_team_label.grid(row=0, column=2, pady=5, padx=5, sticky="sw")
        self.def_var = tk.StringVar()
        self.def_team_filter = ttk.Combobox(
            self.general_frame, textvariable=self.def_var, width=10
        )
        self.def_team_filter["state"] = "readonly"
        self.def_team_filter.grid(row=1, column=2, padx=5, pady=5)
        self.def_team_filter["values"] = UCDB.populate_def_teamlist()

        self.report_table = ttk.Treeview(self, height=20)
        self.report_table["columns"] = UCDB.populate_gui_columns()
        self.report_table.column("#0", width=1)

        for item in UCDB.populate_gui_columns():
            self.report_table.column(f"{item}", width=55)

        for item in UCDB.populate_gui_columns():
            self.report_table.heading(f"{item}", text=item)

        for record in UCDB.populate_gui_data():
            self.report_table.insert(parent="", index="end", text="", values=record)

        self.table_scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.report_table.yview
        )
        self.report_table.configure(yscrollcommand=self.table_scrollbar.set)
        self.report_table.grid(row=4, columnspan=9, sticky="ew", pady=10, padx=10)
        self.table_scrollbar.grid(row=4, column=9, sticky="ns")

        self.custom_frame = ttk.Labelframe(
            self, text="Custom Query", relief="ridge", style="my.TLabelframe"
        )
        self.custom_frame.grid(row=6, column=0)

        def filter_by_selected():
            for row in self.report_table.get_children():
                self.report_table.delete(row)

            year = FilterTemplate.send_value(self.year_filter)
            field_pos = FilterTemplate.send_value(self.field_pos_filter)
            results = FilterTemplate.send_value(self.result_filter)

            form = FilterTemplate.send_value(self.formation_filter)
            off_set = FilterTemplate.send_value(self.set_filter)
            tree = FilterTemplate.send_value(self.tree_filter)
            play_type = FilterTemplate.send_value(self.playtype_filter)

            blitz = FilterTemplate.send_value(self.blitz_filter)
            coverage = FilterTemplate.send_value(self.coverage_filter)
            d_pers = FilterTemplate.send_value(self.def_pers_filter)
            shell = FilterTemplate.send_value(self.shell_filter)
            front = FilterTemplate.send_value(self.front_filter)
            down = FilterTemplate.send_value(self.down_filter)
            dist = FilterTemplate.send_value(self.dist_filter)
            opers = FilterTemplate.send_value(self.pers_filter)
            maintag = FilterTemplate.send_value(self.main_tag)
            bstag = FilterTemplate.send_value(self.backside_call)
            gain = FilterTemplate.send_value(self.gain_filter)
            rush = FilterTemplate.send_value(self.rush_filter)
            conversion = FilterTemplate.send_value(self.conversion_filter)
            if conversion == "True":
                conversion = 1
            elif conversion == "False":
                conversion = 0
            else:
                conversion = None

            team = self.off_team_filter.get()
            if team == "":
                team = None

            opp_tm = self.def_team_filter.get()
            if opp_tm == "":
                opp_tm = None

            qt = int(self.filter_quarter.get())
            if qt == 0:
                qt = None

            for row in UCDB.complex_filter(
                year, team, qt, form, field_pos, off_set, opp_tm, tree, play_type, results, blitz, coverage, d_pers,
                shell, front, down, dist, opers, maintag, bstag, gain, rush, conversion):

                self.report_table.insert(parent="", index="end", text="", values=row)

        self.graph_frame = ttk.Labelframe(
            self, text="Graphs", relief="ridge", style="my.TLabelframe"
        )
        self.graph_frame.grid(row=5, column=0, columnspan=4, pady=10, padx=10)

        def plot_graphs():
            team = self.off_team_filter.get()
            if team == "":
                team = None

            opp_tm = self.def_team_filter.get()
            if opp_tm == "":
                opp_tm = None

            qt = int(self.filter_quarter.get())
            if qt == 0:
                qt = None

            year = FilterTemplate.send_value(self.year_filter)
            field_pos = FilterTemplate.send_value(self.field_pos_filter)
            results = FilterTemplate.send_value(self.result_filter)

            form = FilterTemplate.send_value(self.formation_filter)
            off_set = FilterTemplate.send_value(self.set_filter)
            tree = FilterTemplate.send_value(self.tree_filter)
            play_type = FilterTemplate.send_value(self.playtype_filter)

            blitz = FilterTemplate.send_value(self.blitz_filter)
            coverage = FilterTemplate.send_value(self.coverage_filter)
            d_pers = FilterTemplate.send_value(self.def_pers_filter)
            shell = FilterTemplate.send_value(self.shell_filter)
            front = FilterTemplate.send_value(self.front_filter)
            down = FilterTemplate.send_value(self.down_filter)
            dist = FilterTemplate.send_value(self.dist_filter)
            opers = FilterTemplate.send_value(self.pers_filter)
            maintag = FilterTemplate.send_value(self.main_tag)
            bstag = FilterTemplate.send_value(self.backside_call)
            pos = FilterTemplate.send_value(self.field_pos_filter)
            gain = FilterTemplate.send_value(self.gain_filter)
            rush = FilterTemplate.send_value(self.rush_filter)
            conversion = FilterTemplate.send_value(self.conversion_filter)
            if conversion == "True":
                conversion = 1
            elif conversion == "False":
                conversion = 0
            else:
                conversion = None

            fig = plt.figure(figsize=(18, 4))

            def play_type_plotting():
                x_treelist = []
                y_treedata = []

                for item in UCDB.return_team_treecount(
                    team, year, qt, form, pos, off_set, opp_tm, tree, play_type, results, blitz, coverage, d_pers,
                    shell, front, down, dist, opers, maintag, bstag, gain, rush, conversion):

                    x_treelist.append(item[0])
                    y_treedata.append(item[1])

                try:
                    if x_treelist[0] is None:
                        x_treelist.pop(0)
                        y_treedata.pop(0)
                except IndexError as e:
                    print(e, "plotting error1")

                try:
                    if x_treelist[0] == "?":
                        x_treelist.pop(0)
                        y_treedata.pop(0)
                except IndexError as e:
                    print(e, "plotting error2")

                x1 = np.arange(len(y_treedata))

                ax = fig.add_subplot(222)
                bar1 = ax.bar(x1, y_treedata, 0.5, align="center")
                ax.set_xticks(x1, x_treelist, rotation=45)
                ax.bar_label(bar1, label_type="center", color="w")
                ax.set_facecolor("xkcd:salmon")
                ax.set_facecolor((1.0, 0.47, 0.42))
                plt.title("Play Types")
                plt.tight_layout()

            play_type_plotting()

            def third_down_plotting():
                x_3rds = []
                y_3rds = []

                for item in UCDB.return_team_3rd_downs(
                    team, opp_tm, year, qt, form, pos, off_set, tree, play_type, results, blitz, coverage,
                    d_pers, shell, front, down, dist, opers, maintag, bstag, gain, rush, conversion,
                ):
                    x_3rds.append(item[0])
                    y_3rds.append(item[1])

                try:
                    if x_3rds[0] is None:
                        x_3rds.pop(0)
                        y_3rds.pop(0)
                except IndexError as e:
                    print(e, "plotting error3")

                x2 = np.arange(len(y_3rds))

                ax = fig.add_subplot(212)
                plot1 = ax.bar(x2, y_3rds, 0.5)
                ax.set_xticks(x2, x_3rds, rotation=45)
                # ax.annotate(plot1, label_type='center', color='b')
                plt.tight_layout()
                plt.title("3rd Down Calls")
                plt.grid()

            third_down_plotting()

            def run_pass_plotting():
                x_run_pass = []
                y_run_pass = []

                for item in UCDB.return_team_run_vs_pass(
                    year, team, qt, form, field_pos, off_set, opp_tm, tree, results, blitz, coverage,
                    d_pers, shell, front, down, dist, opers, maintag, bstag, gain, rush, conversion,
                ):
                    x_run_pass.append(item[0])
                    y_run_pass.append(item[1])

                x3 = np.arange(len(y_run_pass))

                ax = fig.add_subplot(221)
                pie1 = ax.pie(
                    y_run_pass,
                    labels=x_run_pass,
                    shadow=True,
                    startangle=90,
                    autopct="%0.1f%%",
                    radius=5000,
                    labeldistance=0.3,
                    pctdistance=3.1,
                )
                ax.axis("equal")
                plt.title("Run/Pass Balance")
                plt.tight_layout()

            run_pass_plotting()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(
                row=5, column=0, columnspan=4, sticky="w", padx=10, pady=10
            )

        plot_graphs()

        self.database_totals = ttk.Label(
            self.button_frame, borderwidth=1, relief="solid"
        )
        self.database_totals.grid(column=0, row=3, padx=3, pady=3)

        self.report_total_var = tk.StringVar()
        self.report_totals = ttk.Label(self.button_frame, borderwidth=1, relief="solid")
        self.report_totals.grid(column=0, row=4, padx=3, pady=3)

        self.db_totals_var = tk.StringVar()
        self.database_totals = ttk.Label(
            self.button_frame,
            textvariable=self.db_totals_var,
            borderwidth=1,
            relief="solid",
        )
        self.database_totals.grid(column=0, row=3, padx=3, pady=3)
        self.db_totals_var.set(f"{UCDB.report_db_total()[0]} Total Plays")

        def report_totals():
            self.report_total_var = tk.StringVar()
            self.report_totals = ttk.Label(
                self.button_frame,
                textvariable=self.report_total_var,
                borderwidth=1,
                relief="solid",
            )
            self.report_totals.grid(column=0, row=4, padx=3, pady=3)
            self.report_total_var.set(
                f"{len(self.report_table.get_children())} Reported Plays"
            )

        def generate_all():
            start = time.perf_counter()

            plot_graphs()
            filter_by_selected()
            report_totals()

            end = time.perf_counter()
            print(f"{end - start:0.4} seconds")

        self.generate = ttk.Button(
            self.button_frame, text="Generate Report", command=generate_all
        )
        self.generate.grid(row=0, padx=3, pady=3)

        def reset_filters():
            for row in self.report_table.get_children():
                self.report_table.delete(row)

            for item in filter_widgets:
                item.clear_value()

            self.off_var.set("")
            self.def_var.set("")

            self.quarter_var.set(0)

            self.def_team_filter["values"] = UCDB.populate_def_teamlist()
            self.off_team_filter["values"] = UCDB.populate_off_teamlist()

            for widget in self.graph_frame.winfo_children():
                widget.destroy()

        self.reset_filters = ttk.Button(
            self.button_frame, text="Reset Filters", command=reset_filters
        )
        self.reset_filters.grid(row=1, padx=3, pady=3)

        self.generate_third_down_report = ttk.Button(
            self.button_frame,
            text="Generate 3rd Down Report",
            command=self.third_down_reporting,
        )
        self.generate_third_down_report.grid(row=2, padx=3, pady=3)

        self.custom_query = FilterTemplate(
            frame=self.custom_frame, label="Custom", column=0, values="test"
        )

        self.off_team_filter.bind("<<ComboboxSelected>>", self.repop_defender_list)
        self.def_team_filter.bind("<<ComboboxSelected>>", self.repop_offense_list)

        # TODO bind the selection of certain elements to auto-refresh other elements to only the relavent filters

    def repop_defender_list(self, event=None):
        new_query = UCDB.repop_opp_teams(self.off_team_filter.get())
        self.def_team_filter["values"] = new_query

    def repop_offense_list(self, event=None):
        new_query = UCDB.repop_off_team(self.def_team_filter.get())
        self.off_team_filter["values"] = new_query

    def update_options(self):
        # TODO make method which calls each repop method, and bind that to each combo box so they all update at once?
        pass

    def third_down_reporting(self):
        team = self.off_team_filter.get()
        if team == "":
            team = None

        opp_tm = self.def_team_filter.get()
        if opp_tm == "":
            opp_tm = None

        qt = int(self.filter_quarter.get())
        if qt == 0:
            qt = None

        year = FilterTemplate.send_value(self.year_filter)
        field_pos = FilterTemplate.send_value(self.field_pos_filter)
        results = FilterTemplate.send_value(self.result_filter)

        form = FilterTemplate.send_value(self.formation_filter)
        off_set = FilterTemplate.send_value(self.set_filter)
        tree = FilterTemplate.send_value(self.tree_filter)
        play_type = FilterTemplate.send_value(self.playtype_filter)

        blitz = FilterTemplate.send_value(self.blitz_filter)
        coverage = FilterTemplate.send_value(self.coverage_filter)
        d_pers = FilterTemplate.send_value(self.def_pers_filter)
        shell = FilterTemplate.send_value(self.shell_filter)
        front = FilterTemplate.send_value(self.front_filter)
        down = FilterTemplate.send_value(self.down_filter)
        dist = FilterTemplate.send_value(self.dist_filter)
        opers = FilterTemplate.send_value(self.pers_filter)
        maintag = FilterTemplate.send_value(self.main_tag)
        bstag = FilterTemplate.send_value(self.backside_call)
        pos = FilterTemplate.send_value(self.field_pos_filter)
        gain = FilterTemplate.send_value(self.gain_filter)
        rush = FilterTemplate.send_value(self.rush_filter)
        conversion = FilterTemplate.send_value(self.conversion_filter)
        if conversion == "True":
            conversion = 1
        elif conversion == "False":
            conversion = 0
        else:
            conversion = None

        ThirdDowns(
            year, field_pos, results, form, off_set, tree, play_type, blitz, coverage, d_pers, shell, front, down,
            dist, opers, maintag, bstag, pos, gain, rush, conversion, opp_tm, qt, team,
        )


class DatabaseGenerator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.name_entry_label = ttk.Label(self, text="Table Name:")
        self.name_entry_label.grid(row=0, column=0)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=1, column=0)

        self.select_source = ttk.Button(self, text="Upload a Source File", command=self.source_upload())
        self.select_source.grid(row=10, column=5)

        self.home_button = ttk.Button(self, text="Home", command=lambda: controller.show_frame(LandingPage))
        self.home_button.grid(row=10, column=4)




        # Add logic to add new elements once source is selected, displaying the selected column names and allow edit
        self.col1_label = ttk.Label(self, text="col 1 var")
        self.col1_label.grid(row=3, column=0)

        self.col1_type_entry = ttk.Combobox(self)
        self.col1_type_entry.grid(row=3, column=1)

    # LOGIC
    # if excel (or csv) _ to _ sql
    # enter: table name, index yes/no + index label --> GENERATE
    # Populate column names into UI, allow for rename / set data types (combobox) / drop column /

    def source_upload(self):
        print("placeholder")


if __name__ == "__main__":
    app = WindowManager()
    # app.geometry("1800x750")
    app.attributes("-fullscreen", True)
    app.mainloop()
