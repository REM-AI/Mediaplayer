def stylesheet(self):
    return """
        QPushButton
        {   
            color: white;
            background: #2b2b2b;
            border: 0px;
        }

        QPushButton:hover
        {
            color: white;
            background: Black;
            border: 0px; 
        }

        QSlider {background: #2b2b2b;}

        QSlider::handle:horizontal 
        {
            background: white;
            width: 18px;
        }

        QSlider::groove:horizontal 
        {
            height: 8px;
            background: black;
        }

        QSlider::sub-page:horizontal 
        {
            background: #e2222e;;
            height: 8px;
        }

        QSlider::handle:horizontal:hover 
        {
            background: white;
            width: 18px;
        }

        QSlider::sub-page:horizontal:disabled {background: #bbbbbb;}
        QSlider::add-page:horizontal:disabled {background: #2a82da;}
        QSlider::handle:horizontal:disabled {background: #2a82da;}

        QLabel
        {   
            color: white;
            background: #2b2b2b;
        }

        QLineEdit
        {
            color: white;
            background: #2b2b2b;
            border: 0px;
            font-size: 8pt;
            font-weight: bold;
        }

        QStatusBar
        {
            color: white;
            background: black;
        }"""

    def stylesheet_0(self):
        return """
            QLabel
            {   
                color: white;
                background: #2b2b2b;
            }"""