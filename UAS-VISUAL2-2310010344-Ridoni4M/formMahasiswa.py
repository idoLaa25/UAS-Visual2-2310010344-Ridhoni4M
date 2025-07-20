import sys
import mysql.connector as mc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from mahasiswa import Ui_mhsWindow  

class AppMahasiswa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mhsWindow()
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
            npm = self.ui.lineEdit.text()
            nama = self.ui.lineEdit_2.text()
            panggilan= self.ui.lineEdit_3.text()
            hp= self.ui.lineEdit_4.text()
            email = self.ui.lineEdit_5.text()
            kelas = self.ui.lineEdit_6.text()
            matkul = self.ui.lineEdit_7.text()
            lokasi = self.ui.lineEdit_8.text()

            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="tugas"
            )
            mycursor = mydb.cursor()
            sql = """
                INSERT INTO mhs (npm, nama, panggilan, hp, email, kelas, matkul, lokasi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (npm, nama, panggilan, hp, email, kelas, matkul, lokasi)
            mycursor.execute(sql, val)
            mydb.commit()

            self.ui.label_8.setText("Data berhasil ditambahkan")
            self.loadSql()  
        except mc.Error as err:
            self.ui.label_8.setText(f" Error: {err}")

    def editdata(self):
        try:
            npm = self.ui.lineEdit.text()
            nama= self.ui.lineEdit_2.text()
            panggilan= self.ui.lineEdit_3.text()
            hp = self.ui.lineEdit_4.text()
            email = self.ui.lineEdit_5.text()
            kelas = self.ui.lineEdit_6.text()
            matkul = self.ui.lineEdit_7.text()
            lokasi = self.ui.lineEdit_8.text()
            

            mydb = mc.connect(
                host ="localhost",
                user ="root",
                password ="",
                database ="tugas"
            )
            mycursor = mydb.cursor()

            sql = """UPDATE mhs SET
                nama = %s, panggilan = %s,
                hp = %s, email = %s,
                kelas = %s, matkul = %s,
                lokasi = %s
            WHERE npm = %s """
            val = (nama, panggilan, hp, email, kelas, matkul, lokasi, npm)
            mycursor.execute(sql, val)
            mydb.commit()
            
            self.ui.label_8.setText("Data berhasil diUpdate")
            self.ui.lineEdit.setText("")
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_3.setText("")
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_5.setText("")
            self.ui.lineEdit_6.setText("")
            self.ui.lineEdit_7.setText("")
            self.ui.lineEdit_8.setText("")
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
            
            npm = item_npm.text()
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="tugas"
            )
            cursor = mydb.cursor()
            sql = "DELETE FROM mhs WHERE npm = %s"
            val = (npm,)
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
            self.ui.lineEdit_7.clear()
            self.ui.lineEdit_8.clear()
            self.ui.label_8.setText("Input dibersihkan")

    def hapus(self):
        self.ui.tableWidget.clearContents()          
        self.ui.tableWidget.setRowCount(0)           
        self.ui.label_8.setText("Data berhasil dihapus dari tampilan")


    def loadByid(self, row):
        try:
            rownpm = self.ui.tableWidget.item(row,0)
            rownama = self.ui.tableWidget.item(row,1)
            rowpanggilan = self.ui.tableWidget.item(row,2)
            rowhp = self.ui.tableWidget.item(row,3)
            rowemail = self.ui.tableWidget.item(row,4)
            rowkelas = self.ui.tableWidget.item(row,5)
            rowmatkul = self.ui.tableWidget.item(row,6)
            rowlokasi = self.ui.tableWidget.item(row,7)

            if rownpm :
                npm = rownpm.text()
                nama = rownama.text()
                panggilan = rowpanggilan.text()
                hp = rowhp.text()
                email = rowemail.text()
                kelas = rowkelas.text()
                matkul = rowmatkul.text()
                lokasi = rowlokasi.text()

                self.ui.lineEdit.setText(npm)
                self.ui.lineEdit_2.setText(nama)
                self.ui.lineEdit_3.setText(panggilan)
                self.ui.lineEdit_4.setText(hp)
                self.ui.lineEdit_5.setText(email)
                self.ui.lineEdit_6.setText(kelas)
                self.ui.lineEdit_7.setText(matkul)
                self.ui.lineEdit_8.setText(lokasi)

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
            mycursor.execute("SELECT * FROM mhs ORDER BY npm ASC")
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
    window = AppMahasiswa()
    window.show()
    sys.exit(app.exec_())
