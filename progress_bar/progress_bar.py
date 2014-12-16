import sys


#allows us to reprint over an existing line.
#Uses terminal escape codes.  May not be device
#independent, but works on Mac and Ubuntu
def single_line_print(data):
    sys.stdout.write("\r\x1b[K" + data.__str__())
    sys.stdout.flush()


#usage is simple...
#
# p = ProgressBar(num_items_to_process)
# for i in num_items_to_process:
#    p.progress_made()
#
#
class ProgressBar:
    def __init__(self, goal):
        self.goal = goal
        self.current_progress = 0
        self.old_percent = -1.0
        self.current_percent = 0.0
        self.prog_bar = '[]'
        self.fill_char = '#'
        self.width = 40
        self.__update_bar_text()

    def reset(self, new_goal=None):
        if new_goal:
            self.goal = new_goal
        self.current_progress = 0
        self.old_percent = -1.0
        self.current_percent = 0.0
        self.prog_bar = '[]'
        self.fill_char = '#'
        self.width = 40
        self.__update_bar_text()

    def progress_made(self, increment=1):
        self.old_percent = float(self.current_progress) / float(self.goal)
        self.current_progress = (self.current_progress + increment)
        self.current_percent = float(self.current_progress) / float(self.goal)
        if ((self.current_percent > self.old_percent) * 100) >= 1:
            self.__update_bar_text()
            single_line_print(self.prog_bar)

    def __update_bar_text(self):
        percent_done = int(round((self.current_percent) * 100.0))
        all_full = self.width - 2
        num_hashes = int(round((percent_done / 100.0) * all_full))
        self.prog_bar = '[' + self.fill_char * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = (len(self.prog_bar) / 2) - len(str(percent_done))
        pct_string = '%d%%' % percent_done
        self.prog_bar = self.prog_bar[0:pct_place] + \
            (pct_string + self.prog_bar[pct_place + len(pct_string):])

    def get_progress(self):
        return self.current_progress

    def get_goal(self):
        return self.goal()

    def __str__(self):
        return str(self.prog_bar)
