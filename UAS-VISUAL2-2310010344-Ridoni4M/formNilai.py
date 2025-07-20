import sys
import mysql.connector as mc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from nilai import Ui_NilaiWindow  

class AppNilai(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NilaiWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.tambahdata)
        self.ui.pushButton_2.clicked.connect(self.editdata)
        self.ui.pushButton_3.clicked.connect(self.batal)
        self.ui.pushButton_4.clicked.connect(self.hapusdata)
        self.ui.pushButton_5.clicked.connect(self.loadSql)
        self.ui.tableWidget.cellClicked.connect(self.loadByid)

        self.loadSql()
        
    def tambahdata(self):
        try:
            id = self.ui.lineEdit.text()
            id_mhs = self.ui.lineEdit_2.text()
            nilai_h= self.ui.lineEdit_3.text()
            nilai_t= self.ui.lineEdit_4.text()
            nilai_ut = self.ui.lineEdit_5.text()
            nilai_ua = self.ui.lineEdit_6.text()


            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="tugas"
            )
            mycursor = mydb.cursor()
            sql = """
                INSERT INTO nilai (id, id_mhs, nilai_h, nilai_t, nilai_ut, nilai_ua)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            val = (id, id_mhs, nilai_h, nilai_t, nilai_ut, nilai_ua)
            mycursor.execute(sql, val)
            mydb.commit()

            self.ui.label_8.setText("Data berhasil ditambahkan")
            self.loadSql()  
        except mc.Error as err:
            self.ui.label_8.setText(f" Error: {err}")

    def editdata(self):
        try:
            id = self.ui.lineEdit.text()
            id_mhs = self.ui.lineEdit_2.text()
            nilai_h= self.ui.lineEdit_3.text()
            nilai_t= self.ui.lineEdit_4.text()
            nilai_ut = self.ui.lineEdit_5.text()
            nilai_ua = self.ui.lineEdit_6.text()
            

            mydb = mc.connect(
                host ="localhost",
                user ="root",
                password ="",
                database ="tugas"
            )
            mycursor = mydb.cursor()

            sql = """UPDATE nilai SET
                id_mhs = %s,
                nilai_h = %s, nilai_t = %s,
                nilai_ut = %s, nilai_ua = %s
            WHERE id = %s """
            val = (id_mhs, nilai_h, nilai_t, nilai_ut, nilai_ua, id)
            mycursor.execute(sql, val)
            mydb.commit()
            
            self.ui.label_8.setText("Data berhasil diUpdate")
            self.ui.lineEdit.setText("")
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_3.setText("")
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_5.setText("")
            self.ui.lineEdit_6.setText("")
            self.loadSql()
        except mc.Error as err:
            self.ui.label_8.setText("Data Gagal DiUpdate")

    def hapusdata(self):
        try:
            selected_row = self.ui.tableWidget.currentRow()
            if selected_row < 0:
                self.ui.label_8.setText("Pilih data yang ingin dihapus terlebih dahulu")
                return

            item_npm = self.ui.tableWidget.item(selected_row, 0)
            if item_npm is None:
                self.ui.label_8.setText("Data tidak valid atau kosong")
                return
            
            id = item_npm.text()
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="tugas"
            )
            cursor = mydb.cursor()
            sql = "DELETE FROM nilai WHERE id = %s"
            val = (id,)
            cursor.execute(sql, val)
            mydb.commit()

            self.ui.label_8.setText("Data berhasil dihapus")
            self.loadSql()

        except mc.Error as err:
            self.ui.label_8.setText(f"Error: {err}")

    def batal(self):
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            self.ui.lineEdit_4.clear()
            self.ui.lineEdit_5.clear()
            self.ui.lineEdit_6.clear()
            self.ui.label_8.setText("Input dibersihkan")

    def hapus(self):
        self.ui.tableWidget.clearContents()          
        self.ui.tableWidget.setRowCount(0)           
        self.ui.label_8.setText("Data berhasil dihapus dari tampilan")


    def loadByid(self, row):
        try:
            rowid = self.ui.tableWidget.item(row,0)
            rowid_mhs = self.ui.tableWidget.item(row,1)
            rownilai_h = self.ui.tableWidget.item(row,2)
            rownilai_t = self.ui.tableWidget.item(row,3)
            rownilai_ut = self.ui.tableWidget.item(row,4)
            rownilai_ua = self.ui.tableWidget.item(row,5)

            if rowid :
                id = rowid.text()
                id_mhs = rowid_mhs.text()
                nilai_h = rownilai_h.text()
                nilai_t = rownilai_t.text()
                nilai_ut = rownilai_ut.text()
                nilai_ua = rownilai_ua.text()


                self.ui.lineEdit.setText(id)
                self.ui.lineEdit_2.setText(id_mhs)
                self.ui.lineEdit_3.setText(nilai_h)
                self.ui.lineEdit_4.setText(nilai_t)
                self.ui.lineEdit_5.setText(nilai_ut)
                self.ui.lineEdit_6.setText(nilai_ua)


            self.ui.label_8.setText("Data Berhasil ditampilkan")
        except mc.Error as err:
            self.ui.label_8.setText("Data Gagal ditampilkan")
            
        
    def loadSql(self):
        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="tugas"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM nilai ORDER BY id ASC")
            result = mycursor.fetchall()
            self.ui.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.ui.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            self.ui.label_8.setText("Data berhasil ditampilkan")
        except mc.Error as err:
            self.ui.label_8.setText("Data Gagal ditampilkan")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppNilai()
    window.show()
    sys.exit(app.exec_())
