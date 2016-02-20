#!/usr/bin/env python3
__version__ = 2.0
import ticker
import webbrowser
from tkinter import *
ENGLISH = 1
GERMAN = 2

import Language

lang = Language.load_language("english")
if False:
    #IDE autocomplete hook
    from Language import english as lang

class configrow():
    entry_width = 10
    def __init__(self, lefttext, value, righttext, minvalue, maxvalue, valuetype = int):
        self.lefttext = lefttext
        self.startvalue = value
        self.righttext = righttext
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.valuetype = valuetype

    def create(self, app):
        self.leftlabel = Label(app, textvar =self.lefttext)
        self.entry = Entry(app)
        self.entry["width"] = self.entry_width
        self.entry.insert(0, self.startvalue)
        self.rightlabel = Label(app, textvar = self.righttext)

    def integrate(self, gridrow):
        self.leftlabel.grid(sticky = W,column = 0, row = gridrow)
        self.entry.grid(column = 1, row = gridrow)
        self.rightlabel.grid(sticky=W, column = 2, row = gridrow)

    def disintegrate(self):
        self.leftlabel.grid_forget()
        self.entry.grid_forget()
        self.rightlabel.grid_forget()

    def norm_settings(self):self.value = min_max(self.minvalue, self.value, self.maxvalue)

    def _getvalue(self):
        text = self.entry.get()
        for i, char in enumerate(text):
            if char == ",":
                text = text[0:i]+"."+text[i+1:]

        self.value = value = min_max(self.minvalue, self.valuetype(text), self.maxvalue)
        return value

    def _setvalue(self, newvalue):
        self.entry.delete(0, END)
        self.entry.insert(0, newvalue)

    def resetvalue(self):self.value = self.startvalue

    def disable(self):self.entry["state"] = DISABLED

    def enable(self):self.entry["state"] = NORMAL

    value = property(_getvalue, _setvalue)

class Application(Frame):
    def __init__(self,settings, master = None):
        Frame.__init__(self, master)
        self.cpucount = settings.cpucount
        self.settings = settings
        self.modebinding = lang.m_mode_basic, lang.m_mode_freq
        self.grid()
        self.grid_configure()
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.statustext = "ready"
        self.language = ENGLISH

    def create_entries(self):
        self.tvo_procl = StringVar(self, lang.m_option_proc)
        self.tvo_procr = StringVar(self, lang.m_option_proc_suffix)
        self.procrow = configrow(self.tvo_procl, self.settings.cpucount, self.tvo_procr, 1, 128)

        self.tvo_timel = StringVar(self, lang.m_option_time)
        self.tvo_timer = StringVar(self, lang.m_option_time_suffix)
        self.timerow = configrow(self.tvo_timel, 60, self.tvo_timer, 1, 60000)

        self.tvo_freql = StringVar(self, lang.m_option_freq)
        self.tvo_freqr = StringVar(self, lang.m_option_freq_suffix)
        self.frequencyrow = configrow(self.tvo_freql, 2.0,self.tvo_freqr, 0.001, 1000000, float)

        self.tvo_freq2l = StringVar(self, lang.m_option_freqend)
        self.frequencyrow2 = configrow(self.tvo_freq2l, 2.0, self.tvo_freqr, 0.001, 1000000, float)
        self.frequencyrow2.create(self)

        start = 3
        self.rows = [self.procrow, self.timerow, self.frequencyrow]
        for row in self.rows:
            row.create(self)
            row.integrate(start)
            start += 1
        
    def open_3dcenter(self):webbrowser.open("http://www.3dcenter.org/")

    def change_language(self):
        global lang
        if self.language == ENGLISH:
            self.language = GERMAN
            lang = Language.load_language("german")
        else:
            self.language = ENGLISH
            lang = Language.english

        self.modebinding = lang.m_mode_basic, lang.m_mode_freq

        self.tv_mode.set(self.modebinding[self.settings.method])
        self.tv_idealabel.set(lang.m_madeby)
        self.tv_cpulabel.set(lang.m_cpu_count+str(self.cpucount))
        self.tv_lang.set("GER" if self.language == ENGLISH else "ENG")

        self.tv_statuslabel.set(lang.m_status_prefix+self.statustext)

        self.tvo_freql.set(lang.m_option_freq)
        self.tvo_freqr.set(lang.m_option_freq_suffix)

        self.tvo_procl.set(lang.m_option_proc)
        self.tvo_procr.set(lang.m_option_proc_suffix)

        self.tvo_timel.set(lang.m_option_time)
        self.tvo_timer.set(lang.m_option_time_suffix)

        self.tvo_freq2l.set(lang.m_option_freqend)

        self.update_labels()
        
    def create_buttons(self):
        self.tv_lang = StringVar(self, "GER")
        self.tv_mode = StringVar(self, lang.m_mode_basic)
        self.tv_start = StringVar(self, "Start Test")
        self.threedcenterbutton = Button(self, text = "3DCenter",
                                     command = self.open_3dcenter,
                                         borderwidth = 0,
                                         fg = "blue")

        self.languagebutton = Button(self, textvar = self.tv_lang,
                                     command = self.change_language)
        self.modebutton = Button(self, textvar =self.tv_mode,
                                  command = self.mode_change)
        self.startbutton = Button(self, textvar =self.tv_start,
                                  command = self.start_button_func)
        self.threedcenterbutton.grid(column = 2,row = 0, sticky = E)
        self.languagebutton.grid(column = 2, row = 1)
        self.modebutton.grid(column = 1, row = 0)
        self.startbutton.grid(column = 1, row = 1)

    def mode_change(self):
        self.settings.method = (self.settings.method+1)%settings.methods
        self.tv_mode.set(self.modebinding[self.settings.method])
        if self.settings.method:#normal -> freq sweep
            self.rows.append(self.frequencyrow2)
            self.frequencyrow2.integrate(6)
        else:#freq sweep -> normal
            self.rows = self.rows[:4]
            self.frequencyrow2.disintegrate()

    def update_settings(self, tries = 4):
        tries = tries
        current = self.procrow
        try:

            self.settings.cpucount = self.procrow.value
            current = self.frequencyrow
            if self.frequencyrow.value == 0:raise ValueError("Can't be zero.")
            self.settings.frequency = self.frequencyrow.value
            if self.frequencyrow2.value == 0:raise ValueError("Can't be zero.")
            self.settings.frequency2 = self.frequencyrow2.value
            current = self.timerow
            self.settings.testtime = self.timerow.value
        except ValueError as e:
            current.resetvalue()
            tries -= 1
            if not tries:raise (e)
            self.update_settings(tries)
            return True
        return False

    def enable(self):
        for row in self.rows:
            row.enable()
        self.modebutton["state"] = NORMAL

    def disable(self):
        for row in self.rows:
            row.disable()
        self.modebutton["state"] = DISABLED

    def start_button_func(self):
        self.startbutton.grid_forget()
        self.statustext = lang.m_status_running
        self.testtimelabel.grid(column = 0, columnspan = 3, row=2)
        if not (self.update_settings()):#only run on valid input
            self.disable()
            self.statuslabel.config(fg ="red")
            self.update_labels()
            self.update_idletasks()
            ticker.test(self.settings, self.show_remaining_time)
            self.statustext = lang.m_status_ready
            self.statuslabel.config(fg ="black")
            self.enable()
        self.testtimelabel.grid_forget()
        self.startbutton.grid(column = 1, row=1)
        self.update_labels()
        self.update_idletasks()

    def reset_entries(self):
        for row in self.rows:
            row.resetvalue()

    def show_remaining_time(self, time_elapsed):
        if time_elapsed < 0:
            self.tv_testtimelabel.set(lang.m_status_preparing)
        else:
            self.tv_testtimelabel.set(lang.m_timelabel+str(int(round(self.settings.testtime-time_elapsed)))+lang.m_timelabel_suffix)
        self.testtimelabel.update()

    def update_labels(self):
        self.tv_statuslabel.set(lang.m_status_prefix+self.statustext)

    def create_labels(self):
        self.tv_testtimelabel = StringVar(self, "")
        self.testtimelabel = Label(self, textvar = self.tv_testtimelabel)
        self.tv_idealabel = StringVar(self, lang.m_madeby)
        self.idealabel = Label(self, textvar = self.tv_idealabel)
        self.tv_statuslabel = StringVar(self, lang.m_status_prefix+lang.m_status_ready)
        self.statuslabel = Label(self, textvar = self.tv_statuslabel)
        self.tv_cpulabel = StringVar(self, lang.m_cpu_count+str(self.settings.cpucount))
        self.cpulabel = Label(self, textvar = self.tv_cpulabel)
        self.statuslabel.grid(sticky = W, column = 0, row = 0, columnspan = 2)
        self.cpulabel.grid(sticky = W, column = 0, row = 1, columnspan = 1)
        self.idealabel.grid(row = 7, columnspan = 2)

def start(settings):
    root = Tk()
    try: root.wm_iconbitmap('favicon.ico')
    except TclError: print ("Icon not found")
    root.resizable(0,0)
    gui = Application(settings, root)
    gui.master.title("3DCenter CPU Ticker "+str(__version__))
    gui.mainloop()
    
def min_max(min_value, value, max_value):
    if min_value > value:
        return min_value
    elif max_value < value:
        return max_value
    return value

if __name__ == "__main__":
    from multiprocessing import freeze_support
    from shared import Settings
    freeze_support()
    settings = Settings()
    start(settings)