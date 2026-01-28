from PyQt5 import QtWidgets, QtCore,QtGui

class StarRatingWidget(QtWidgets.QWidget):
    """ეს კლასი არის ვარსკვლავებით შეფასების სისტემისთვის"""
    def __init__(self, stars=5):
        super().__init__()
        self.stars = stars
        self.current_rating = 0

        layout = QtWidgets.QHBoxLayout(self)

        self.star_labels = []
        for i in range(stars):
            lbl = QtWidgets.QLabel("☆")
            lbl.setStyleSheet("font-size: 24px; color: gray;")
            lbl.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            lbl.mousePressEvent = lambda _, index=i: self.set_rating(index+1)
            layout.addWidget(lbl)
            self.star_labels.append(lbl)

    def set_rating(self, rating):
        """
            ეს კოდი ☆ ასეთ ვარსკვლავებს ცვლის, ასეთ ვარსკვლავებად ★, თუ მონიშნულია
        """
        self.current_rating = rating
        for i, lbl in enumerate(self.star_labels):
            if i < rating:
                lbl.setText("★")
                lbl.setStyleSheet("font-size: 24px; color: gold;")
            else:
                lbl.setText("☆")
                lbl.setStyleSheet("font-size: 24px; color: gray;")

    def get_rating(self):
        """
            აბრუნებს რეიტინგს
        """
        return self.current_rating



