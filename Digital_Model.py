import sqlite3


class SqlDB:

    def __init__(self):
        self.sqlmsg = ''

    def connect(self):
        path = 'BD/aut_ini_prod_dig.db'
        connection = sqlite3.connect(path)
        return connection

    def add(self, data):
        conn = self.connect()
        sql = 'INSERT INTO jobs (id, item, date, time, var_tones, var_print_faults, var_right_mat, var_shaft_dim,' \
              'var_dev_dim, var_tape, var_txt_pdf, var_folios, var_barcode, var_fdie_cut, var_ftones, var_ftxt_pdf, ' \
              'var_fstamping, var_fgap, var_fcolor_sep, var_frefile, var_fcross_hatch, var_ftape_film, var_fmek,' \
              'var_falcohol, var_fchip_test, var_fvarnish_window, var_ffotolum, var_fcof) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cursor = conn.cursor()
        while True:
            try:
                print(data)
                cursor.execute(sql, data)
                conn.commit()
                conn.close()
                self.sqlmsg = 'Los datos fueron agregados'
                return self.sqlmsg

            except sqlite3.Error as error:
                if 'UNIQUE' in error.args[0]:
                    self.sqlmsg = 'JOB DUPLICADO'
                elif 'locked' in error.args[0]:
                    self.sqlmsg = 'BD BLOQUEADA'
                return self.sqlmsg

    def search(self, jobid):
        conn = self.conectar()
        sql = 'SELECT id FROM jobs WHERE id = ?', jobid
        cursor = conn.cursor()
        while True:
            try:
                cursor.execute('SELECT id FROM jobs WHERE id=', jobid)
                conn.commit()
                conn.close()
                sqlmsg = 'SIOMBRE'
                return sqlmsg
            except sqlite3.Error:
                return
        return
