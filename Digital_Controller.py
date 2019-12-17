from Digital_Model import SqlDB
from Digital_View import MainView
from Digital_View import CheckBox_Items


class AppInit:
# Ctrl = Controller
    def __init__(self):
        self.model = SqlDB()
        self.controller = Controller(self.model)
        self.view = MainView(self.controller) # App initialization
        self.view.printme()

class Controller:

    def __init__(self, model):
        self.model = model

    def add_to_db(self, instance, job, item, date, time):
        self.instance = instance
        self.job = job
        self.item = item
        self.date = str(date)
        self.time = time
        self.data_chkbxs = self.instance.get_chkboxes_state
        self.chkbxs_states = (self.job, self.item, self.date, self.time) + self.data_chkbxs
        self.dbmsg = self.model.add(self.chkbxs_states)
        return

    def clean_screen(self):
        self.instance.clear_chkboxes_state()
        self.entry_job.delete(0, 'end')
        self.entry_item.delete(0, 'end')
        self.entry_job.focus_set()
        return
