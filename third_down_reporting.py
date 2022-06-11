import tkinter as tk
from tkinter import ttk
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageGrab
import seaborn as sns

from db_access import UserConnection
from db_plotting import PlotConnection
from db_reporting import ReportConnector
from printer_handler import PrinterHandler, PrintingAction

UCDB = UserConnection()
PCDB = PlotConnection()
RCDB = ReportConnector()


class ThirdDowns(tk.Frame):
    def __init__(
      self, year, field_pos, results, form, off_set, tree, play_type, blitz, coverage, d_pers, shell, front, down, dist,
            opers, maintag, bstag, pos, gain, rush, conversion, opptm, qtr, team):

        tk.Frame.__init__(self)
        # tk.Tk.wm_title("Playmaker Reporting")

        def third_down_reporting(event=None):
            try:
                os.mkdir("print_prep")
            except FileExistsError as e:
                pass

            def cleanup():
                directory = "print_prep"
                for item in os.listdir(directory):
                    os.remove((os.path.join(directory, item)))

            cleanup()

            img_path = "print_prep"

            if team is None:
                alert_popup = tk.Toplevel(self)
                alert_popup.geometry("300x300")
                alert_text = ttk.Label(
                    alert_popup,
                    text="Please select a team for reporting,\nalong with any other "
                    "desired filters",
                )
                alert_text.pack(pady=100)

            else:
                self.report = tk.Toplevel(self)
                self.report.title(f"{team} 3rd Down Report")
                self.report.geometry("1350x1000")
                self.report.resizable(False, False)
                self.report.rowconfigure(0, weight=1)
                self.report.columnconfigure(0, weight=1)

                self.canvas = tk.Canvas(self.report, borderwidth=0)
                self.frame = tk.Frame(self.canvas)
                self.vsb = tk.Scrollbar(
                    self.report, orient=tk.VERTICAL, command=self.canvas.yview
                )
                self.canvas.configure(yscrollcommand=self.vsb.set)

                self.canvas.bind_all(
                    "<MouseWheel>",
                    lambda event: self.canvas.yview_scroll(
                        int(-1 * (event.delta / 120)), "units"
                    ),
                )

                self.canvas.grid(row=0, column=0, sticky="nsew")
                self.canvas.create_window(
                    0, 0, window=self.frame, anchor="nw", tags="frame"
                )
                self.vsb.grid(row=0, column=10, sticky="ns")

                def jump_to_widget(widget):
                    if self.frame.winfo_height() > self.canvas.winfo_height():
                        position = widget.winfo_rooty() - self.frame.winfo_rooty()
                        height = self.frame.winfo_height()
                        self.canvas.yview_moveto(position / height)

                        # Must update widget after repositioning window, to return to print_prep an accurate rootx&y
                        widget.update()
                        return widget

                def print_prep(var, widget):
                    jump_to_widget(widget)

                    if var.get() == 1:
                        ImageGrab.grab(
                            bbox=(
                                widget.winfo_rootx(),
                                widget.winfo_rooty(),
                                widget.winfo_rootx() + widget.winfo_width(),
                                widget.winfo_rooty() + widget.winfo_height(),
                            ),include_layered_windows=False,
                        ).save(f"{img_path}/{widget}.png")
                    elif var.get() == 0:
                        try:
                            os.remove(f"{img_path}/{widget}.png")
                        except Exception as e:
                            print(e)

                def summary_placment():
                    summary_frame = ttk.Labelframe(self.frame, text="Summary")
                    summary_frame.grid(row=0, column=0)

                    conversion_getter = RCDB.team_3rd_down_conversions(team)

                    run_pass_3rds_df = RCDB.run_pass_on_3rd(team)

                    def one_yd_checker():
                        # print(run_pass_3rds_df.loc[run_pass_3rds_df['Distance'] == 5])
                        one_yd = run_pass_3rds_df.loc[run_pass_3rds_df['Distance'] == 1]
                        df_1yd = one_yd.reset_index()
                        # print(df_1yd)
                        # row1 = (df_1yd.loc[0, 'Times Called'])
                        # row2 = (df_1yd.loc[1, 'Times Called'])

                        # row1 = (df_1yd.loc[df_1yd['PlayType'] == 'Pass'])
                        # row2 = (df_1yd.loc[df_1yd['PlayType'] == 'Run'])
                        # print(row1)
                        # print(row2)

                        # calculation = 100 * float(row1.loc['Times Called'])/float(row2.loc['Times Called'])
                        # print(calculation)

                        # print(two_yds.loc[0].at['Times Called'])
                        # print(run_pass_3rds_df.loc[1].at['Times Called'])
                        # if on distance, run # is > than pass # by X percent (or reverse), give print a sentance to GUI
                        # for index, row in run_pass_3rds_df.iterrows():
                        #     print(row['PlayType'], row['Distance'], row['Times Called'])
                            # if
                    one_yd_checker()

                    total_attempts = conversion_getter.loc[1].at['Count'] + conversion_getter.loc[0].at['Count']
                    summary_text = f"{team} has {conversion_getter.loc[1].at['Count']} successful third down " \
                                    f"conversions " \
                                    f"on {total_attempts} attempts "
                    summary_widget = ttk.Label(summary_frame, text=summary_text)
                    summary_widget.grid(row=0, column=0)
                summary_placment()

                plotset_1_frame = ttk.Labelframe(self.frame, text="first set")
                plotset_1_frame.grid(row=1, columnspan=5, rowspan=4)
                p1_chkValue = tk.IntVar()
                plotset_1_printcheck = tk.Checkbutton(
                    plotset_1_frame,
                    text="Want Printed",
                    command=lambda: print_prep(p1_chkValue, plotset_1_frame),
                    variable=p1_chkValue,
                    onvalue=1,
                    offvalue=0,
                )
                plotset_1_printcheck.grid(row=2, column=5)

                plotset_2_frame = ttk.Labelframe(self.frame, text="second set")
                plotset_2_frame.grid(row=5, columnspan=5, rowspan=4)
                p2_chkValue = tk.IntVar()
                plotset_2_printcheck = tk.Checkbutton(
                    plotset_2_frame,
                    text="Want Printed",
                    command=lambda: print_prep(p2_chkValue, plotset_2_frame),
                    variable=p2_chkValue,
                    onvalue=1,
                    offvalue=0,
                )
                plotset_2_printcheck.grid(row=2, column=5)

                plotset_3_frame = ttk.Labelframe(self.frame, text="third set")
                plotset_3_frame.grid(row=9, columnspan=5, rowspan=4)
                p3_chkValue = tk.IntVar()
                plotset_3_printcheck = tk.Checkbutton(
                    plotset_3_frame,
                    text="Want Printed",
                    command=lambda: print_prep(p3_chkValue, plotset_3_frame),
                    variable=p3_chkValue,
                    onvalue=1,
                    offvalue=0,
                )
                plotset_3_printcheck.grid(row=2, column=5)

                plotset_4_frame = ttk.Labelframe(self.frame, text="fourth set")
                plotset_4_frame.grid(row=14, columnspan=5, rowspan=4)
                p4_chkValue = tk.IntVar()
                plotset_4_printcheck = tk.Checkbutton(
                    plotset_4_frame,
                    text="Want Printed",
                    command=lambda: print_prep(p4_chkValue, plotset_4_frame),
                    variable=p4_chkValue,
                    onvalue=1,
                    offvalue=0,
                )
                plotset_4_printcheck.grid(row=2, column=5)

                plotset_5_frame = ttk.Labelframe(self.frame, text="fifth set")
                plotset_5_frame.grid(row=18, columnspan=5, rowspan=4)
                p5_chkValue = tk.IntVar()
                plotset_5_printcheck = tk.Checkbutton(
                    plotset_5_frame,
                    text="Want Printed",
                    command=lambda: print_prep(p5_chkValue, plotset_5_frame),
                    variable=p5_chkValue,
                    onvalue=1,
                    offvalue=0,
                )
                plotset_5_printcheck.grid(row=2, column=5)

                print_button = ttk.Button(
                    self.frame, text="Print Report", command=PrintingAction
                )
                print_button.grid(row=0, column=4)

                printer_select = ttk.Button(
                    self.frame, text="Select Printer", command=PrinterHandler
                )
                printer_select.grid(row=0, column=3)

                def plot():
                    sns.set_theme()

                    def plotset_1():
                        fig = plt.figure(figsize=(12, 9))

                        df = PCDB.return_team_3rd_downs(
                            team, opptm, year, qtr, form, pos, off_set, tree, play_type, results, blitz, coverage,
                            d_pers, shell, front, down, dist, opers, maintag, bstag, gain, rush, conversion)

                        ax1 = fig.add_subplot(211)
                        p1 = sns.barplot(x="MAIN TAG", y="Count", data=df)
                        p1.set_xlabel("Call", fontsize=10)
                        p1.set_ylabel("Frequency", fontsize=10)
                        p1.set_xticklabels(p1.get_xticklabels(), rotation=60)
                        plt.title("Main Tags")
                        p1.bar_label(p1.containers[0])
                        plt.tight_layout()

                        df2 = PCDB.play_tree_3rd(team)
                        ax2 = fig.add_subplot(212)
                        p2 = sns.pointplot(x="Play Tree", y="Count", data=df2)
                        p2.set_xticklabels(p2.get_xticklabels(), rotation=60)
                        plt.tight_layout()

                        fig_canvas = FigureCanvasTkAgg(fig, master=plotset_1_frame)

                        fig_canvas.draw()
                        fig_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)

                    plotset_1()

                    def plotset_2():
                        df = PCDB.return_gain_vs_dist(team)

                        x = df.iloc[:, 0].values.reshape(-1, 1)
                        y = df.iloc[:, 1].values.reshape(-1, 1)

                        # TODO get line to interesect the point between non-conversion and conversions
                        def create_lmplot():
                            p1 = sns.lmplot(
                                y="Distance to Gain",
                                x="Gained on Play",
                                data=df,
                                hue="Conversion",
                                col="Conversion",
                            )
                            return p1.fig

                        p1 = sns.relplot(
                            data=df, y="Distance to Gain", x="Gained on Play"
                        )
                        figure = create_lmplot()

                        fig_canvas = FigureCanvasTkAgg(figure, master=plotset_2_frame)

                        fig_canvas.draw()
                        fig_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)

                    plotset_2()

                    def plotset_3():
                        fig = plt.figure(figsize=(11, 9))
                        df = PCDB.return_gain_vs_dist(team)
                        ax1 = fig.add_subplot(211)

                        p5 = sns.scatterplot(
                            y="Distance to Gain",
                            x="Gained on Play",
                            data=df,
                            size="Count",
                            sizes=(40, 200),
                            hue="Conversion",
                            style="Conversion",
                        )
                        y_column = df["Distance to Gain"]
                        y_min = y_column.min()
                        y_max = y_column.max()
                        p5.set_yticks(range(y_min, y_max))
                        x_column = df["Gained on Play"]
                        x_min = x_column.min()
                        x_max = x_column.max()
                        p5.set_xticks(range(x_min, x_max))
                        plt.tight_layout()
                        plt.title(f"All {team} 3rd Downs")
                        p5.set_xticklabels(p5.get_xticklabels(), rotation=60)


                        ax2 = fig.add_subplot(212)
                        df = PCDB.team_3rd_down_conversions_filtered(
                         team, opptm, year, qtr, form, pos, off_set, tree, play_type, results, blitz, coverage, d_pers,
                            shell, front, down, dist, opers, maintag, bstag, gain, rush, conversion)

                        p5 = sns.scatterplot(
                            y="Distance to Gain",
                            x="Gained on Play",
                            data=df,
                            size="Count",
                            sizes=(40, 200),
                            hue="Conversion",
                            style="Conversion",
                        )
                        y_column = df["Distance to Gain"]
                        y_min = y_column.min()
                        y_max = y_column.max()
                        p5.set_yticks(range(y_min, y_max))
                        x_column = df["Gained on Play"]
                        x_min = x_column.min()
                        x_max = x_column.max()
                        p5.set_xticks(range(x_min, x_max))
                        plt.tight_layout()
                        plt.title(f"Filtered {team} 3rd Downs")
                        p5.set_xticklabels(p5.get_xticklabels(), rotation=60)


                        fig_canvas = FigureCanvasTkAgg(fig, master=plotset_3_frame)

                        fig_canvas.draw()
                        fig_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)

                    plotset_3()

                    def plotset_4():
                        fig = plt.figure(figsize=(11, 9))
                        df = PCDB.run_pass_on_3rd(team)

                        p1 = sns.barplot(
                            x="Distance", y="Times Called", hue="PlayType", data=df
                        )

                        fig_canvas = FigureCanvasTkAgg(fig, master=plotset_4_frame)

                        fig_canvas.draw()
                        fig_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)

                    plotset_4()

                    def plotset_5():
                        fig = plt.figure(figsize=(11, 9))
                        df = PCDB.formations_on_3rd(team)

                        p1 = sns.barplot(x="Count", y="Formation", data=df)
                        plt.tight_layout()

                        fig_canvas = FigureCanvasTkAgg(fig, master=plotset_5_frame)

                        fig_canvas.draw()
                        fig_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)

                    plotset_5()

                    self.update_idletasks()

                plot()

                def onFrameConfigure(event):
                    """Reset the scroll region to encompass the inner frame"""
                    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

                self.frame.bind("<Configure>", onFrameConfigure)

        third_down_reporting()
