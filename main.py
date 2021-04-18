from PyQt5.QtWidgets import QWidget,QLabel,QApplication,QVBoxLayout,QPushButton,QListWidget,QHBoxLayout,QFileDialog
import os
from PIL import ImageFilter,Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL.ImageFilter import BLUR

app = QApplication([])
main_win = QWidget()
main_win.resize(700,500)

l1 = QVBoxLayout()
l2 = QVBoxLayout()
l3 = QHBoxLayout()
l4 = QHBoxLayout()
btn_pap = QPushButton('Папка')
spisok = QListWidget()
kart = QLabel()
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркально')
reis = QPushButton('Размытие')
blkwht = QPushButton('Ч/Б')
backblkwht = QPushButton('Вернуть')

l1.addWidget(btn_pap)
l1.addWidget(spisok)
l2.addWidget(kart)
l3.addWidget(left)
l3.addWidget(right)
l3.addWidget(mirror)
l3.addWidget(reis)
l3.addWidget(blkwht)
l3.addWidget(backblkwht)
l2.addLayout(l3)
l4.addLayout(l1)

l4.addLayout(l2)

wordkir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(filenames,extentions):
    m= []
    for name in filenames:
        for ext in extentions:
            if name.endswith(ext):
                m.append(name)
    return m

def showFilenamesList():
    global workdir
    extentions =['jpeg','jpg']
    chooseWorkdir()
    filenames=os.listdir(workdir)
    names = filter(filenames,extentions)
    spisok.clear()
    for file in names:
        spisok.addItem(file)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = 'modif/'
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(label, path):
        kart.hide()
        pixmapimage = QPixmap(path)
        w, h =kart.width(), kart.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        kart.setPixmap(pixmapimage)
        kart.show()
    def saveImage(self):
        global workdir
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path)or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_reis(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_backblkwht(self): # почему не рабоотает возврат цвета?
        #print('я работаю')
        image_path = os.path.join(workdir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()
def showChosenImage():
    if spisok.currentRow() >=0:
        filename = spisok.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)


spisok.currentRowChanged.connect(showChosenImage)
blkwht.clicked.connect(workimage.do_bw)
btn_pap.clicked.connect(showFilenamesList)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
mirror.clicked.connect(workimage.do_mirror)
reis.clicked.connect(workimage.do_reis)
backblkwht.clicked.connect(workimage.do_backblkwht)

main_win.setLayout(l4)
main_win.show()
app.exec()