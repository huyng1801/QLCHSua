#Chạy lệnh pip install PyQt5 để cài đặt thư viện
import sys
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from maininterface import Ui_Program
from addeditproduct import Ui_AddEditProduct
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_Program()
        self.uic.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.loadProduct()

        self.uic.QTWProduct.setColumnWidth(0, 100)
        self.uic.QTWProduct.setColumnWidth(1, 100)
        self.uic.QTWProduct.setColumnWidth(2, 250)
        self.uic.QTWProduct.setColumnWidth(3, 250)
        self.uic.QTWProduct.setColumnWidth(4, 250)
        self.uic.QTWProduct.setColumnWidth(5, 100)
        self.uic.QTWProduct.setColumnWidth(6, 100)
        self.uic.QTWBillDetails.setColumnWidth(0,100)
        self.uic.QTWBillDetails.setColumnWidth(1,550)
        self.uic.QTWBillDetails.setColumnWidth(2,150)
        self.uic.QTWBillDetails.setColumnWidth(3,150)
        self.uic.QTWBillDetails.setColumnWidth(4,150)
        self.uic.QPBProduct.clicked.connect(lambda: self.uic.QSW.setCurrentIndex(0))
        self.uic.QPBSell.clicked.connect(lambda: self.uic.QSW.setCurrentIndex(1))
        self.uic.QPBCart.clicked.connect(lambda: self.uic.QSW.setCurrentIndex(2))
        self.uic.QPBStatistics.clicked.connect(lambda: self.uic.QSW.setCurrentIndex(3))
        self.uic.QTWProduct.horizontalHeader().show()
        self.uic.QTWBillDetails.horizontalHeader().show()
        self.uic.QTWStaticstics.horizontalHeader().show()
        self.uic.QPBExit.clicked.connect(lambda: main_win.close())
        self.uic.QPBAddProduct.clicked.connect(lambda: self.addProduct())
        self.uic.QLESearchProduct.textChanged.connect(lambda: self.searchProduct())
        self.uic.QPBPay.clicked.connect(lambda: self.pay())
        self.main_win_3 = QMainWindow()
        self.uic_3 = Ui_AddEditProduct()
        self.uic_3.setupUi(self.main_win_3)
        self.uic_3.QPBUpLoadProductImage.clicked.connect(lambda: self.upLoadImage())
        self.uic_3.QPBSaveProduct.clicked.connect(lambda: self.saveAddEditProduct())
        self.loadProductToOrder()
        self.uic.QLESearchProductToOrder.textChanged.connect(lambda: self.searchProductToOrder())
        self.uic.QLCountProductToBill.hide()
        self.uic.QTWBillDetails.setRowCount(0)
        self.uic.QTWStaticstics.setRowCount(3)
        self.uic.QPBProduct.clicked.connect(lambda: self.focusMenu())
        self.uic.QPBSell.clicked.connect(lambda: self.focusMenu())
        self.uic.QPBStatistics.clicked.connect(lambda: self.focusMenu())
        self.loadStaticstics()
        self.uic.QLCountProductToBill.setText("0")
        self.uic_3.QLEProductPrice.setValidator(QIntValidator())
        self.uic.QLESearchProductToOrder.setPlaceholderText("Nhập tên sản phẩm để tìm kiếm")
        self.uic.QLESearchProductToOrder.setMinimumWidth(350)
    def focusMenu(self):
        self.uic.QPBProduct.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.uic.QPBStatistics.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.uic.QPBSell.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.sender().setStyleSheet("background-color: rgb(255, 184, 108);")
    def loadStaticstics(self):
        self.uic.QTWStaticstics.setRowCount(0)
        for row in range(self.uic.QTWProduct.rowCount()):
            self.uic.QTWStaticstics.setRowCount(self.uic.QTWStaticstics.rowCount() + 1)
            self.uic.QTWStaticstics.setItem(row, 0, QTableWidgetItem(self.uic.QTWProduct.item(row, 1).text()))
            self.uic.QTWStaticstics.setItem(row, 1, QTableWidgetItem(self.uic.QTWProduct.item(row, 2).text()))
            self.uic.QTWStaticstics.setItem(row, 2, QTableWidgetItem(self.uic.QTWProduct.item(row, 3).text()))
            self.uic.QTWStaticstics.setItem(row, 3, QTableWidgetItem(self.uic.QTWProduct.item(row, 4).text()))
            self.uic.QTWStaticstics.setItem(row, 4, QTableWidgetItem(self.uic.QTWProduct.item(row, 5).text()))
            self.uic.QTWStaticstics.setItem(row, 5, QTableWidgetItem(self.uic.QTWProduct.item(row, 6).text()))
    def pay(self):
        self.uic.QLCountProductToBill.hide()
        self.uic.QLCountProductToBill.setText("0")
        for row1 in range(self.uic.QTWBillDetails.rowCount()):
            for row2 in range(self.uic.QTWProduct.rowCount()):
                if self.uic.QTWProduct.item(row2, 2).text() == self.uic.QTWBillDetails.item(row1, 1).text():
                    print(self.uic.QTWBillDetails.item(row1,1).text())
                    print(self.uic.QTWProduct.item(row2, 2).text())
                    self.uic.QTWProduct.setItem(row2, 6, QTableWidgetItem(str((int(self.uic.QTWProduct.item(row2, 6).text()))-int(self.uic.QTWBillDetails.cellWidget(row1, 2).text()))))
                    self.uic.QTWProduct.item(row2, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()
                    cursor.execute("""CREATE TABLE IF NOT EXISTS SAN_PHAM(MA_SUA TEXT NOT NULL PRIMARY KEY, TEN_SUA TEXT NOT NULL, TEN_CONG_TY_SAN_XUAT TEXT,
                    QUY_CACH_HANG_HOA TEXT, DON_GIA INTEGER, SO_LUONG INTEGER, ANH_DAI_DIEN TEXT)""")
                    update = f"UPDATE SAN_PHAM SET SO_LUONG = {int(self.uic.QTWProduct.item(row2, 6).text())} WHERE MA_SUA LIKE '{self.uic.QTWProduct.item(row2, 1).text()}'"
                    cursor.execute(update)
                    conn.commit()
                    conn.close()
        self.uic.QTWBillDetails.setRowCount(0)
        self.alert("Thanh toán thành công!")
        self.uic.QSW.setCurrentIndex(1)
        
        self.loadStaticstics()
    def alert(self, str: str):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.alertShow())
        self.timer.start(3000)
        self.uic.QLTitle.setText(str)
    def alertShow(self):
            self.timer.stop()
            del self.timer
            self.uic.QLTitle.clear()
    def addProductToBill(self):
        self.uic.QLCountProductToBill.show()
        self.uic.QLCountProductToBill.setText(str(int(self.uic.QLCountProductToBill.text())+1))
        productName = []
        for i in range(self.uic.QTWBillDetails.rowCount()):
            productName.append(self.uic.QTWBillDetails.item(i, 1).text().split())
        if self.sender().parent().toolTip().split()[1: len(self.sender().parent().toolTip().split())] not in productName:
            for row in range(self.uic.QTWProduct.rowCount()):
                if self.uic.QTWProduct.item(row, 1).text() == self.sender().parent().toolTip().split()[0]:
                    self.uic.QTWBillDetails.setRowCount(self.uic.QTWBillDetails.rowCount()+1)
                    QWEmployeeImage = QWidget()
                    QLEmployeeImage = QLabel(QWEmployeeImage)
                    QLEmployeeImage.setGeometry(30, 2, 30, 36)
                    QLEmployeeImage.setScaledContents(True)
                    QLEmployeeImage.setPixmap(QPixmap(self.imageProduct[self.uic.QTWProduct.item(row, 1).text()]))
                    self.uic.QTWBillDetails.setCellWidget(self.uic.QTWBillDetails.rowCount()-1, 0, QWEmployeeImage)
                    QSBNumber = QSpinBox()
                    QSBNumber.setMinimum(1)
                    QSBNumber.setMaximum(int(self.uic.QTWProduct.item(row, 6).text()))
                    QSBNumber.valueChanged.connect(lambda: self.changedNumber())
                    self.uic.QTWBillDetails.setCellWidget(self.uic.QTWBillDetails.rowCount()-1, 2, QSBNumber)
                    self.uic.QTWBillDetails.setItem(self.uic.QTWBillDetails.rowCount()-1, 1, QTableWidgetItem(self.uic.QTWProduct.item(row, 2).text()))
                    self.uic.QTWBillDetails.setItem(self.uic.QTWBillDetails.rowCount()-1, 3, QTableWidgetItem(self.uic.QTWProduct.item(row, 5).text()))
                    self.uic.QTWBillDetails.setItem(self.uic.QTWBillDetails.rowCount()-1, 4, QTableWidgetItem(self.uic.QTWProduct.item(row, 5).text()))
                    QWActionProduct = QWidget()
                    QWActionProduct.setStyleSheet("border-right: 1px solid rgb(40, 42, 54);")
                    buttonRemoveProduct = QPushButton(QWActionProduct)
                    buttonRemoveProduct.setIcon(QIcon("icon\\removeproduct.png"))
                    buttonRemoveProduct.setGeometry(40, 2, 30, 30)
                    buttonRemoveProduct.setStyleSheet("background-color: rgb(255, 184, 108); border-radius: 5px;")
                    buttonRemoveProduct.clicked.connect(lambda: self.removeBill())
                    self.uic.QTWBillDetails.setCellWidget(self.uic.QTWBillDetails.rowCount() - 1, 5, QWActionProduct)
                    self.loadTotalPrice()
        else:
            for row in range(self.uic.QTWBillDetails.rowCount()):
                if self.uic.QTWBillDetails.item(row, 1).text().split() == self.sender().parent().toolTip().split()[1: len(self.sender().parent().toolTip().split())]:
                    self.uic.QTWBillDetails.cellWidget(row, 2).setValue(int(self.uic.QTWBillDetails.cellWidget(row, 2).text())+1)
                    self.uic.QTWBillDetails.setItem(row, 4, QTableWidgetItem(str(int(self.uic.QTWBillDetails.cellWidget(row, 2).text())*
                                                                                 int(self.uic.QTWBillDetails.item(row, 3).text()))))
                    self.loadTotalPrice()
    def removeBill(self):
        self.sender().parent().setFocus()
        if self.uic.QTWBillDetails.rowCount() > 0:
            self.uic.QTWBillDetails.removeRow(self.uic.QTWBillDetails.currentRow())
            self.loadTotalPrice()
    def loadTotalPrice(self):
        totalPrice = 0
        for row in range(self.uic.QTWBillDetails.rowCount()):
            totalPrice += int(self.uic.QTWBillDetails.item(row, 4).text())
        self.uic.QLTotalPriceNumeric.setText(self.convertToVND(str(totalPrice)))
    def changedNumber(self):
        self.sender().parent().setFocus()
        self.uic.QTWBillDetails.setItem(self.uic.QTWBillDetails.currentRow(), 
            4, QTableWidgetItem(str(int(self.uic.QTWBillDetails.cellWidget(self.uic.QTWBillDetails.currentRow(), 2).text())*
                int(self.uic.QTWBillDetails.item(self.uic.QTWBillDetails.currentRow(), 3).text()))))
        self.loadTotalPrice()
    def convertToVND(self, str):
        temp = ""
        count = 0
        for i in range(len(str) - 1, -1, -1):
            count += 1
            temp += str[i]
            if count % 3 == 0:
                temp += "."
        if temp[-1] == ".":
            temp = temp[0: -1]
        return temp[-1: :-1] + "đ"
    
    def searchProductToOrder(self):
        rowProduct = 0
        row = 0
        column = 0
        self.uic.QTWProductToOrder.setRowCount(row)
        while rowProduct < self.uic.QTWProduct.rowCount():
            self.uic.QTWProductToOrder.setRowCount(row+1)
            if (self.uic.QTWProduct.item(rowProduct, 2).text().lower().find(self.uic.QLESearchProductToOrder.text().lower())  != -1):
                QWLoadProductToOrder = QWidget()
                QWLoadProductToOrder.setToolTip(self.uic.QTWProduct.item(rowProduct,1).text()+"\n" + self.uic.QTWProduct.item(rowProduct,2).text())
                QWLoadProductToOrder.setStyleSheet("font: 10pt 'MS Shell Dlg 2';")
                QLImageProductToOrder = QLabel(QWLoadProductToOrder)
                QLImageProductToOrder.setGeometry(50, 50, 200, 200)
                QLImageProductToOrder.setScaledContents(True)
                QLProductNameToOrder = QLabel(QWLoadProductToOrder)
                QLProductNameToOrder.setGeometry(20, 250, 260, 71)
                QLProductNameToOrder.setWordWrap(True)
                QLProductNameToOrder.setText(self.uic.QTWProduct.item(rowProduct,2).text())
                QLProductPriceToOrder = QLabel(QWLoadProductToOrder)
                QLProductPriceToOrder.setGeometry(20, 315, 110, 20)
                QLProductPriceToOrder.setText(self.convertToVND(self.uic.QTWProduct.item(rowProduct, 5).text()))
                QLProductPriceToOrder.setStyleSheet("color: rgb(255, 85, 85);")
                QPBProductOrder = QPushButton(QWLoadProductToOrder)
                QPBProductOrder.setGeometry(75, 340, 150, 40)
                QPBProductOrder.setText("CHỌN MUA")
                QPBProductOrder.setStyleSheet("color: rgb(40, 42, 48); border-radius: 5px; background-color: rgb(80, 250, 123)")
                QPBProductOrder.clicked.connect(lambda: self.addProductToBill())
                QLImageProductToOrder.setPixmap(QPixmap(self.imageProduct[self.uic.QTWProduct.item(rowProduct,1).text()]))
                if self.uic.QTWProduct.item(rowProduct, 6).text() == "0":
                    QPBProductOrder.setDisabled(True)
                    QPBProductOrder.setStyleSheet("color: rgb(200, 200, 200); border-radius: 5px; background-color: rgb(80, 250, 123)")
                self.uic.QTWProductToOrder.setCellWidget(row, column, QWLoadProductToOrder)
                column += 1
            if column == 4:
                column = 0
                row += 1
            rowProduct += 1
        while column < 4:
                QWTemp = QWidget()
                QWTemp.setStyleSheet("background-color: rgb(248, 248, 242);")
                self.uic.QTWProductToOrder.setCellWidget(row, column, QWTemp)
                column += 1
        if self.uic.QLESearchProductToOrder.text == "":
            self.loadProductToOrder()
    def setNumberProduct(self):
        for row in range(self.uic.QTWBillDetails.rowCount()):
            if self.uic.QTWBillDetails.item(row, 1).text().split() == self.sender().parent().toolTip().split()[1:len(self.sender().parent().toolTip().split())]:
                self.uic.QTWBillDetails.setItem(row, 2, QTableWidgetItem(str(self.sender().value())))
                
    def loadProductToOrder(self):
        rowProduct = 0
        row = 0
        column = 0
        while rowProduct < self.uic.QTWProduct.rowCount():
                self.uic.QTWProductToOrder.setRowCount(row+1)
                QWLoadProductToOrder = QWidget()
                QWLoadProductToOrder.setToolTip(self.uic.QTWProduct.item(rowProduct,1).text()+"\n" + self.uic.QTWProduct.item(rowProduct,2).text())
                QWLoadProductToOrder.setStyleSheet("font: 10pt 'MS Shell Dlg 2';")
                QLImageProductToOrder = QLabel(QWLoadProductToOrder)
                QLImageProductToOrder.setGeometry(50, 50, 200, 200)
                QLImageProductToOrder.setScaledContents(True)
                QLProductNameToOrder = QLabel(QWLoadProductToOrder)
                QLProductNameToOrder.setGeometry(20, 250, 260, 71)
                QLProductNameToOrder.setWordWrap(True)
                QLProductNameToOrder.setText(self.uic.QTWProduct.item(rowProduct,2).text())
                QLProductPriceToOrder = QLabel(QWLoadProductToOrder)
                QLProductPriceToOrder.setGeometry(20, 315, 110, 20)
                QLProductPriceToOrder.setText(self.convertToVND(self.uic.QTWProduct.item(rowProduct, 5).text()))
                QLProductPriceToOrder.setStyleSheet("color: rgb(255, 85, 85);")
                QPBProductOrder = QPushButton(QWLoadProductToOrder)
                QPBProductOrder.setGeometry(75, 340, 150, 40)
                QPBProductOrder.setText("CHỌN MUA")
                QPBProductOrder.setStyleSheet("color: rgb(40, 42, 48); border-radius: 5px; background-color: rgb(80, 250, 123)")
                QPBProductOrder.clicked.connect(lambda: self.addProductToBill())
                if self.uic.QTWProduct.item(rowProduct, 6).text() == "0":
                    QPBProductOrder.setDisabled(True)
                    QPBProductOrder.setStyleSheet("color: rgb(200, 200, 200); border-radius: 5px; background-color: rgb(80, 250, 123)")
                QLImageProductToOrder.setPixmap(QPixmap(self.imageProduct[self.uic.QTWProduct.item(rowProduct,1).text()]))
                self.uic.QTWProductToOrder.setCellWidget(row, column, QWLoadProductToOrder)
                column += 1
                if column == 4:
                    column = 0
                    row += 1
                rowProduct += 1
        while column < 4:
                QWTemp = QWidget()
                QWTemp.setStyleSheet("background-color: rgb(248, 248, 242);")
                self.uic.QTWProductToOrder.setCellWidget(row, column, QWTemp)
                column += 1
                
    def editProduct(self):
        self.addEdit = "edit"
        self.main_win_3.show()
        self.uic_3.QLEProductId.setDisabled(True)
        self.uic_3.QLEProductName.setPlaceholderText("Nhập tên sữa")
        self.uic_3.QLEProductProducer.setPlaceholderText("Nhập tên công ty sản xuất")
        self.uic_3.QLEProductCS.setPlaceholderText("Nhập quy cách hàng hóa")
        self.uic_3.QLEProductPrice.setPlaceholderText("Nhập đơn giá")
        self.sender().parent().setFocus()
        self.uic_3.QLEProductId.setText(self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 1).text())
        self.uic_3.QLEProductName.setText(self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 2).text())
        self.uic_3.QLEProductProducer.setText(self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 3).text())
        self.uic_3.QLEProductCS.setText(self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 4).text())
        self.uic_3.QLEProductPrice.setText(self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 5).text())
        self.uic_3.QSBProductNumber.setValue(int(self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 6).text()))
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = f"SELECT ANH_DAI_DIEN FROM SAN_PHAM WHERE MA_SUA LIKE '{self.uic_3.QLEProductId.text()}'"
        cursor.execute(query)    
        for milk in cursor:
            self.image = ((milk[0]), '')
            self.uic_3.QLProductImage.setPixmap(QPixmap(self.image[0]))
            
        conn.commit()
        conn.close()
    def searchProduct(self):
        for row in range(self.uic.QTWProduct.rowCount()):
            if (self.uic.QTWProduct.item(row, 1).text().lower().find(self.uic.QLESearchProduct.text().lower()) == -1 and
                self.uic.QTWProduct.item(row, 2).text().lower().find(self.uic.QLESearchProduct.text().lower()) == -1):
                self.uic.QTWProduct.hideRow(row)
            else:
                self.uic.QTWProduct.showRow(row)
                
        if self.uic.QLESearchProduct.text() == "":
            for row in range(self.uic.QTWProduct.rowCount()):
                self.uic.QTWProduct.showRow(row)
                
    def loadProduct(self):
        self.uic.QTWProduct.setRowCount(0)
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS SAN_PHAM(MA_SUA TEXT NOT NULL PRIMARY KEY, TEN_SUA TEXT NOT NULL, TEN_CONG_TY_SAN_XUAT TEXT,
                    QUY_CACH_HANG_HOA TEXT, DON_GIA INTEGER, SO_LUONG INTEGER, ANH_DAI_DIEN TEXT)""")
        cursor.execute("SELECT* FROM SAN_PHAM")
        self.imageProduct = {}
        for milk in cursor:
            self.imageProduct[milk[0]] = milk[6]
            QWProductImage = QWidget()
            QLProductImage = QLabel(QWProductImage)
            QLProductImage.setGeometry(30, 2, 30, 36)
            QLProductImage.setScaledContents(True)
            QLProductImage.setPixmap(QPixmap(milk[6]))
            QWActionProduct = QWidget()
            QWActionProduct.setStyleSheet("border-right: 1px solid rgb(40, 42, 54);")
            buttonRemoveProduct = QPushButton(QWActionProduct)
            buttonRemoveProduct.setIcon(QIcon("icon\\removeproduct.png"))
            buttonEditProduct = QPushButton(QWActionProduct)
            buttonEditProduct.setIcon(QIcon("icon\\editproduct.png"))
            buttonRemoveProduct.setGeometry(60, 5, 30, 30)
            buttonEditProduct.setGeometry(20, 5, 30, 30)
            buttonEditProduct.setStyleSheet("background-color: rgb(139, 233, 253); border-radius: 5px;")
            buttonRemoveProduct.setStyleSheet("background-color: rgb(255, 184, 108); border-radius: 5px;")
            buttonRemoveProduct.clicked.connect(lambda: self.removeProduct())
            buttonEditProduct.clicked.connect(lambda: self.editProduct())
            self.uic.QTWProduct.setRowCount(self.uic.QTWProduct.rowCount() + 1)
            self.uic.QTWProduct.setCellWidget(self.uic.QTWProduct.rowCount() - 1, 0, QWProductImage)
            self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 1, QTableWidgetItem(milk[0]))
            self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 2, QTableWidgetItem(milk[1]))
            self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 3, QTableWidgetItem(milk[2]))
            self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 4, QTableWidgetItem(milk[3]))
            self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 5, QTableWidgetItem(str(milk[4])))
            self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 6, QTableWidgetItem(str(milk[5])))
            self.uic.QTWProduct.setCellWidget(self.uic.QTWProduct.rowCount() - 1, 7, QWActionProduct)
            self.uic.QTWProduct.item(self.uic.QTWProduct.rowCount() - 1, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.uic.QTWProduct.item(self.uic.QTWProduct.rowCount() - 1, 5).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.uic.QTWProduct.item(self.uic.QTWProduct.rowCount() - 1, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                    
        conn.commit()
        conn.close()    
    def removeProduct(self):
        self.sender().parent().setFocus()
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Thông báo")
        self.msg.setText("Bạn có muốn xóa sản phẩm?")
        self.msg.addButton(QPushButton('Đồng ý'), QMessageBox.YesRole)
        self.msg.addButton(QPushButton('Hủy'), QMessageBox.NoRole)
        self.msg.show()
        ret = self.msg.exec()
        if ret == 0:
            self.agreeRemoveProduct()
        
    def agreeRemoveProduct(self):
        if self.uic.QTWProduct.rowCount() > 0:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            delete = f"DELETE FROM SAN_PHAM WHERE MA_SUA LIKE '{self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 1).text()}'"
            cursor.execute(delete)
            conn.commit()
            self.uic.QTWProduct.removeRow(self.uic.QTWProduct.currentRow())
            self.loadProductToOrder()
            self.alert("Xóa thành công")
    def saveAddEditProduct(self):
        products = []
        
        for row in range(self.uic.QTWProduct.rowCount()):
            products.append(self.uic.QTWProduct.item(row, 1).text())
        
        if self.addEdit == "add":
            if (self.uic_3.QLEProductId.text() not in products and self.uic_3.QLEProductName.text() != ""  and 
                self.uic_3.QLEProductProducer.text() != "" and self.uic_3.QLEProductCS.text() != "" 
                and self.uic_3.QLEProductPrice.text() != ""):
                self.imageProduct[self.uic_3.QLEProductId.text()] = self.image[0][self.image[0].find("image"): len(self.image[0])]
                self.alert("Thêm thành công")
                QWProductImage = QWidget()
                QLProductImage = QLabel(QWProductImage)
                QLProductImage.setGeometry(30, 2, 30, 36)
                QLProductImage.setScaledContents(True)
                QLProductImage.setPixmap(QPixmap(self.image[0][self.image[0].find("image"): len(self.image[0])]))
                QWActionProduct = QWidget()
                QWActionProduct.setStyleSheet("border-right: 1px solid rgb(40, 42, 54);")
                buttonRemoveProduct = QPushButton(QWActionProduct)
                buttonRemoveProduct.setIcon(QIcon("icon\\removeproduct.png"))
                buttonEditProduct = QPushButton(QWActionProduct)
                buttonEditProduct.setIcon(QIcon("icon\\editproduct.png"))
                buttonRemoveProduct.setGeometry(60, 5, 30, 30)
                buttonEditProduct.setGeometry(20, 5,30, 30)
                buttonEditProduct.setStyleSheet("background-color: rgb(139, 233, 253); border-radius: 5px;")
                buttonRemoveProduct.setStyleSheet("background-color: rgb(255, 184, 108); border-radius: 5px;")
                buttonRemoveProduct.clicked.connect(lambda: self.removeProduct())
                buttonEditProduct.clicked.connect(lambda: self.editProduct())
                self.uic.QTWProduct.setRowCount(self.uic.QTWProduct.rowCount() + 1)
                self.uic.QTWProduct.setCellWidget(self.uic.QTWProduct.rowCount() - 1, 0, QWProductImage)
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 1, QTableWidgetItem(self.uic_3.QLEProductId.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 2, QTableWidgetItem(self.uic_3.QLEProductName.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 3,QTableWidgetItem(self.uic_3.QLEProductProducer.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 4,QTableWidgetItem(self.uic_3.QLEProductCS.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 5,QTableWidgetItem(self.uic_3.QLEProductPrice.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.rowCount() - 1, 6,QTableWidgetItem(self.uic_3.QSBProductNumber.text()))
                self.uic.QTWProduct.setCellWidget(self.uic.QTWProduct.rowCount() - 1, 7, QWActionProduct)
                self.uic.QTWProduct.item(self.uic.QTWProduct.rowCount() - 1, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.uic.QTWProduct.item(self.uic.QTWProduct.rowCount() - 1, 5).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.uic.QTWProduct.item(self.uic.QTWProduct.rowCount() - 1, 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS SAN_PHAM(MA_SUA TEXT NOT NULL PRIMARY KEY, TEN_SUA TEXT NOT NULL, TEN_CONG_TY_SAN_XUAT TEXT,
                    QUY_CACH_HANG_HOA TEXT, DON_GIA INTEGER, SO_LUONG INTEGER, ANH_DAI_DIEN TEXT)""")
        
                data = [(self.uic_3.QLEProductId.text(), self.uic_3.QLEProductName.text(), self.uic_3.QLEProductProducer.text(), 
                         self.uic_3.QLEProductCS.text(), int(self.uic_3.QLEProductPrice.text()), int(self.uic_3.QSBProductNumber.text()), self.image[0][self.image[0].find('image'): len(self.image[0])])]
                insert = """INSERT OR IGNORE INTO SAN_PHAM (MA_SUA, TEN_SUA, TEN_CONG_TY_SAN_XUAT, QUY_CACH_HANG_HOA, DON_GIA, SO_LUONG, ANH_DAI_DIEN) VALUES (?, ?, ?, ?, ?, ?, ?);"""
                cursor.executemany(insert, data)
                conn.commit()
                conn.close()
                self.clearAddEditProduct()
                self.main_win_3.close()
                self.loadProductToOrder()

        if self.addEdit == "edit":
            if (self.uic_3.QLEProductName.text() != ""  and self.uic_3.QLEProductProducer.text() != "" 
                and self.uic_3.QLEProductCS.text() != "" and self.uic_3.QLEProductPrice.text() != ""):
                self.imageProduct[self.uic_3.QLEProductId.text()] = self.image[0][self.image[0].find("image"): len(self.image[0])]
                self.alert("Sửa thành công")
                QWProductImage = QWidget()
                QLProductImage = QLabel(QWProductImage)
                QLProductImage.setGeometry(30, 2, 30, 36)
                QLProductImage.setScaledContents(True)
                QLProductImage.setPixmap(QPixmap(self.image[0][self.image[0].find("image"): len(self.image[0])]))
                print(self.image[0][self.image[0].find("image"): len(self.image[0])])
                self.uic.QTWProduct.setCellWidget(self.uic.QTWProduct.currentRow(), 0, QWProductImage)
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.currentRow(), 2,QTableWidgetItem(self.uic_3.QLEProductName.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.currentRow(), 3,QTableWidgetItem(self.uic_3.QLEProductProducer.text())) 
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.currentRow(), 4,QTableWidgetItem(self.uic_3.QLEProductCS.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.currentRow(), 5,QTableWidgetItem(self.uic_3.QLEProductPrice.text()))
                self.uic.QTWProduct.setItem(self.uic.QTWProduct.currentRow(), 6,QTableWidgetItem(self.uic_3.QSBProductNumber.text()))
                self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 5).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.uic.QTWProduct.item(self.uic.QTWProduct.currentRow(), 6).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS SAN_PHAM(MA_SUA TEXT NOT NULL PRIMARY KEY, TEN_SUA TEXT NOT NULL, TEN_CONG_TY_SAN_XUAT TEXT,
                    QUY_CACH_HANG_HOA TEXT, DON_GIA INTEGER, SO_LUONG INTEGER, ANH_DAI_DIEN TEXT)""")
                update = f"UPDATE SAN_PHAM SET TEN_SUA = '{self.uic_3.QLEProductName.text()}', TEN_CONG_TY_SAN_XUAT = '{self.uic_3.QLEProductProducer.text()}', QUY_CACH_HANG_HOA = '{self.uic_3.QLEProductCS.text()}', DON_GIA = {int(self.uic_3.QLEProductPrice.text())},SO_LUONG = {int(self.uic_3.QSBProductNumber.text())} ,ANH_DAI_DIEN = '{self.image[0][self.image[0].find('image'): len(self.image[0])]}' WHERE MA_SUA LIKE '{self.uic_3.QLEProductId.text()}'"
                cursor.execute(update)
                conn.commit()
                conn.close()
                self.main_win_3.close()
                self.loadProductToOrder()
    def addProduct(self):
        self.addEdit = "add"
        self.clearAddEditProduct()
        self.uic_3.QLEProductId.setEnabled(True)
        self.main_win_3.show()
        self.image = ('', '')
        self.uic_3.QLProductImage.setPixmap(QPixmap(self.image[0]))
        self.uic_3.QLEProductId.setPlaceholderText("Nhập mã sữa")
        self.uic_3.QLEProductName.setPlaceholderText("Nhập tên sữa")
        self.uic_3.QLEProductProducer.setPlaceholderText("Nhập tên công ty sản xuất")
        self.uic_3.QLEProductCS.setPlaceholderText("Nhập quy cách hàng hóa")
        self.uic_3.QLEProductPrice.setPlaceholderText("Nhập đơn giá")
        max = -9999999999
        for row in range(self.uic.QTWProduct.rowCount()):
            if int(self.uic.QTWProduct.item(row, 1).text()) > max:
                max = int(self.uic.QTWProduct.item(row, 1).text())
        max += 1
        for i in range(len(str(max)), 6):
            max = "0" + str(max)
        self.uic_3.QLEProductId.setText(max)
        self.uic_3.QLEProductId.setDisabled(True)
        
    def clearAddEditProduct(self):
        self.uic_3.QLEProductId.clear()
        self.uic_3.QLEProductName.clear()
        self.uic_3.QLEProductProducer.clear()
        self.uic_3.QLEProductCS.clear()
        self.uic_3.QLEProductPrice.clear()
        self.uic_3.QSBProductNumber.setValue(1)
        
    def upLoadImage(self):
        temp = QFileDialog.getOpenFileName(filter='*.png *.jpg *.jfif')
        
        if temp != ('', ''):
            self.image = temp
            
        if self.sender().objectName() == "QPBUpLoadEmployeeImage":
            self.uic_2.QLUserImage.setPixmap(QPixmap(self.image[0]))
        if self.sender().objectName() == "QPBUpLoadProductImage":
            self.uic_3.QLProductImage.setPixmap(QPixmap(self.image[0]))
        
        
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()
        
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos()-self.oldPosition)
        self.move(self.x()+ delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

import sqlite3

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Main()
    main_win.show()
    sys.exit(app.exec())