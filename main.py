import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np 
from PySide2 import QtWidgets, QtCore, QtGui
import sys
from Font import font
import xlsxwriter
import xlrd

class Window (QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui()
        self.theme()
        self.otherSettings()
        self.disableWidgets()
        self.setAllToolTips()
        self.SELECTED_COLUMNS = []
        self.MULTIPLE_COLUMNS = []
        self.first_date = "default"
        self.second_date = "default"
        plt.style.use('seaborn-darkgrid')
        self.setWindowTitle("DataVis - Personal Graph Creator")
        self.setWindowIcon(QtGui.QIcon('.\\app_photos\\window_icon.png'))
        self.setGeometry(680, 100, 550, 850)
        self.figSizeX.setText("9") 
        self.figSizeY.setText("6")
        self.MULTIPLE_CHOICE = False
        self.spinbox.setSuffix(" inch")
        self.spinbox.setSingleStep(0.2)
        self.spinbox.setMaximum(7.0000000000000036)
        self.markerSizeSpinBox.setSuffix(" inch")
        self.markerSizeSpinBox.setSingleStep(0.2)
        self.markerSizeSpinBox.setMaximum(11.99999999999999)
        self.markerCB.addItem("Set Marker")
        self.markerCB.addItems(["Filled Square", "Filled Circle", "X"])
        self.lineWidth = 1.60
        self.markerSize = 0
        self.markerStyle = '.'
        self.lineStyleCB.addItem("Set Style")
        self.lineStyleCB.addItems(["Straight Line", "Dotted Line", "Intermittent Line"])
        self.lineStyle = "-"
        self.y_fontSize = 12
        self.x_fontSize = 12
        self.titleFontSize = 14
        
        self.y_fontSizeSpinBox.setValue(self.y_fontSize)
        self.x_fontSizeSpinBox.setValue(self.x_fontSize)
        self.titleFontSizeSB.setValue(self.titleFontSize)

    def setAllToolTips(self):
        self.loadFile_Button.setToolTip('<b>%s</b><br><img src="%s">' % ("Tool Tip 1", ".\\app_photos\\load_file_info.png"))
        self.browseData_Button.setToolTip('<b>%s</b><br><img src="%s">' % ("Tool Tip 2", ".\\app_photos\\Browse_data_info.png"))
        self.lineThicknessTip.setToolTip('<b>%s</b><br><img src="%s">' % ("Tool Tip 3", ".\\app_photos\\lineStyles.png"))
        self.markerTip.setToolTip('<b>%s</b><br><img src="%s">' % ("Tool Tip 4", ".\\app_photos\\markerStyles.png"))

    def disableWidgets(self):
        #Line chart widgets
        self.multipleColCB.setEnabled(False)
        #Time Series widgets
        self.dateCheckBox.setEnabled(False)
        self.date1.setEnabled(False)
        self.date2.setEnabled(False)
        self.setDateButton.setEnabled(False)
        self.trendNoice.setEnabled(False)
        self.bollingerBandsCB.setEnabled(False)

        font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")
        font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")
        font.adjust_font(self.dateLabel1, "QLabel", "Candara", 
                        font_size=12, color="#908F8F")
        font.adjust_font(self.datelabel2, "QLabel", "Candara", 
                        font_size=12, color="#908F8F")
        font.adjust_font(self.multipleColCBLabel, "QLabel", "Candara", 
                        font_size=12, color="#908F8F")
        font.adjust_font(self.multipleColCB, "QCheckBox", "Candara",
                            bg_color="#908F8F")
        font.adjust_font(self.setDateButton, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#908F8F", 
                        bg_color="black")
        font.adjust_font(self.dateCheckBox, "QCheckBox", "Candara", 
                            bg_color="#908F8F")
        font.adjust_font(self.trendNoice, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")

        font.adjust_font(self.bollingerBandsCB, "QCheckBox", "Trebuchet MS", 
                        font_size=11, color="#908F8F")

    def otherSettings(self):
        self.loadFile_Button.setFixedWidth(250)
        self.browseData_Button.setFixedWidth(250)
        self.selectColButton.setFixedWidth(140)
        self.browseColumnButton.setFixedWidth(140)
        self.clearSelectedButt.setFixedWidth(140)
        self.printGraph.setFixedWidth(140)
        self.columns.setFixedWidth(350)
        self.trendNoice.setFixedWidth(80)
        self.spinbox.setFixedWidth(73)
        self.spinbox.setFixedHeight(27)
        self.markerCB.setFixedHeight(27)
        self.markerCB.setFixedWidth(94)
        self.markerSizeSpinBox.setFixedHeight(27)
        self.markerSizeSpinBox.setFixedWidth(73)
        self.lineStyleCB.setFixedWidth(94)
        self.lineStyleCB.setFixedHeight(27)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.columnsLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.yTitle.setPlaceholderText("for instance, Price")
        self.yTitle.setFixedWidth(150)
        self.xTitle.setPlaceholderText("for instance, Date")
        self.xTitle.setFixedWidth(150)
        self.graphTitle.setPlaceholderText("the title of graph")
        self.graphTitle.setFixedWidth(150)
        self.figSizeX.setPlaceholderText("inch")
        self.figSizeX.setFixedWidth(150)
        self.figSizeY.setPlaceholderText("inch")
        self.figSizeY.setFixedWidth(150)
        self.date1.setPlaceholderText("yyyy-mm-dd")
        self.date2.setPlaceholderText("yyyy-mm-dd")
        self.trendNoice.setPlaceholderText("effect rate")

        self.rbGroup.addButton(self.timeSeriesRB)
        self.rbGroup.addButton(self.lineChartRB)

    def ui(self):
        #Empty Label
        self.emptyLabel         = QtWidgets.QLabel("")
        self.emptyLabel2        = QtWidgets.QLabel("")

        #FILE SECTION.
        self.loadFile_Label     = QtWidgets.QLabel("FILE")
        self.loadFile_Button    = QtWidgets.QPushButton("Load File")
        self.browseData_Button  = QtWidgets.QPushButton("Browse Data")
        self.infoLabel          = QtWidgets.QLabel("No data loaded.")

        #GRAPH SETTINGS
        self.settingsLabel      = QtWidgets.QLabel("\nGRAPH SETTINGS")
        self.timeSeriesRB       = QtWidgets.QRadioButton("Time Series")
        self.lineChartRB        = QtWidgets.QRadioButton("Line")
        self.trendCheckBox      = QtWidgets.QCheckBox("Show Trend")
        self.yTitleLabel        = QtWidgets.QLabel("Title of y Line\t\t   ")
        self.xTitleLabel        = QtWidgets.QLabel("Title of x Line\t\t   ")
        self.graphTitleLabel    = QtWidgets.QLabel("Title of Graph\t\t   ")
        self.yTitle             = QtWidgets.QLineEdit()
        self.xTitle             = QtWidgets.QLineEdit()
        self.graphTitle         = QtWidgets.QLineEdit()
        self.figSizeLabelX      = QtWidgets.QLabel("Fig. size horizontal\t\t   ")
        self.figSizeLabelY      = QtWidgets.QLabel("Fig. size vertical\t\t   ")
        self.figSizeX           = QtWidgets.QLineEdit()
        self.figSizeY           = QtWidgets.QLineEdit()
        self.rbGroup            = QtWidgets.QButtonGroup()
        self.trendNoice         = QtWidgets.QLineEdit()
        self.bollingerBandsCB   = QtWidgets.QCheckBox("Bollinger Bands")
        self.spinboxLabel       = QtWidgets.QLabel("Line Thickness & Style\t: ")
        self.spinbox            = QtWidgets.QDoubleSpinBox()
        self.markerLabel        = QtWidgets.QLabel("Marker Style & Size\t: ")
        self.markerCB           = QtWidgets.QComboBox()
        self.markerSizeSpinBox  = QtWidgets.QDoubleSpinBox()
        self.lineStyleCB        = QtWidgets.QComboBox()
        self.y_fontSizeLabel    = QtWidgets.QLabel("Font Size:")
        self.y_fontSizeSpinBox  = QtWidgets.QSpinBox()
        self.x_fontSizeLabel    = QtWidgets.QLabel("Font Size:")
        self.x_fontSizeSpinBox  = QtWidgets.QSpinBox()
        self.titleFontSizeLB    = QtWidgets.QLabel("Font Size:")
        self.titleFontSizeSB    = QtWidgets.QSpinBox()

        #DATA SETTINGS
        self.dataSettingsLabel  = QtWidgets.QLabel("\nDATA SETTINGS")
        self.columns            = QtWidgets.QListWidget()
        self.LChartLabel        = QtWidgets.QLabel("Line Chart Settings")
        self.multipleColCB      = QtWidgets.QCheckBox()
        self.multipleColCBLabel = QtWidgets.QLabel("Multiple Columns")
        self.columnsLabel       = QtWidgets.QLabel("Columns of Data")
        self.selectColButton    = QtWidgets.QPushButton("Select Column")
        self.browseColumnButton = QtWidgets.QPushButton("Browse Column")
        self.clearSelectedButt  = QtWidgets.QPushButton("Clear Selected Data")
        self.tSeriesLabel       = QtWidgets.QLabel("Time Series Settings")
        self.dateCheckBox       = QtWidgets.QCheckBox()
        self.dateLabel1         = QtWidgets.QLabel("Set date between")
        self.date1              = QtWidgets.QLineEdit()
        self.datelabel2         = QtWidgets.QLabel("and")
        self.date2              = QtWidgets.QLineEdit()
        self.setDateButton      = QtWidgets.QPushButton("SET")
        self.lineThicknessTip   = QtWidgets.QLabel("See styles.")
        self.markerTip          = QtWidgets.QLabel("See markers.")

        #PRINT GRAPH
        self.printGraph         = QtWidgets.QPushButton("Create Graph")

        vbox                = QtWidgets.QVBoxLayout()
        hbox                = QtWidgets.QHBoxLayout()
        buttonsLayout       = QtWidgets.QHBoxLayout()
        infoHLayout         = QtWidgets.QHBoxLayout()
        settingHBox         = QtWidgets.QHBoxLayout()
        rbHBox              = QtWidgets.QHBoxLayout()
        yTitlesHBox         = QtWidgets.QHBoxLayout()
        xTitlesHBox         = QtWidgets.QHBoxLayout()
        titleGraphHBox      = QtWidgets.QHBoxLayout()
        emptyHBox           = QtWidgets.QHBoxLayout()
        dataSettHBox        = QtWidgets.QHBoxLayout()
        dataColLabHBox      = QtWidgets.QHBoxLayout()
        columnListHBox      = QtWidgets.QHBoxLayout()
        buttonHBox          = QtWidgets.QHBoxLayout()
        figSizeXHBox        = QtWidgets.QHBoxLayout()
        figSizeYHBox        = QtWidgets.QHBoxLayout()
        lineRBHBox          = QtWidgets.QHBoxLayout()
        printGraphHBox      = QtWidgets.QHBoxLayout()
        LchartSettingsHBox  = QtWidgets.QHBoxLayout()
        tSeriesLabelHBox    = QtWidgets.QHBoxLayout()
        dateSettingsHBox    = QtWidgets.QHBoxLayout()
        spinboxHBox         = QtWidgets.QHBoxLayout()
        markerHBox          = QtWidgets.QHBoxLayout()
        emptyLayout2        = QtWidgets.QHBoxLayout()

        vbox.addWidget(self.loadFile_Label)
        buttonsLayout.addWidget(self.loadFile_Button)
        buttonsLayout.addWidget(self.browseData_Button)
        infoHLayout.addWidget(self.infoLabel)
        settingHBox.addWidget(self.settingsLabel)
        rbHBox.addWidget(self.lineChartRB)
        rbHBox.addWidget(self.timeSeriesRB)
        rbHBox.addWidget(self.trendCheckBox)
        rbHBox.addWidget(self.trendNoice)
        rbHBox.addWidget(self.bollingerBandsCB)
        spinboxHBox.addWidget(self.spinboxLabel)
        spinboxHBox.addWidget(self.spinbox)
        spinboxHBox.addWidget(self.lineStyleCB)
        spinboxHBox.addWidget(self.lineThicknessTip)
        spinboxHBox.addStretch()
        markerHBox.addWidget(self.markerLabel)
        markerHBox.addWidget(self.markerSizeSpinBox)
        markerHBox.addWidget(self.markerCB)
        markerHBox.addWidget(self.markerTip)
        markerHBox.addStretch()
        emptyLayout2.addWidget(self.emptyLabel2)
        emptyHBox.addWidget(self.emptyLabel)
        xTitlesHBox.addWidget(self.xTitleLabel)
        xTitlesHBox.addWidget(self.xTitle)
        xTitlesHBox.addWidget(self.x_fontSizeLabel)
        xTitlesHBox.addWidget(self.x_fontSizeSpinBox)
        xTitlesHBox.addStretch()
        yTitlesHBox.addWidget(self.yTitleLabel)
        yTitlesHBox.addWidget(self.yTitle)
        yTitlesHBox.addWidget(self.y_fontSizeLabel)
        yTitlesHBox.addWidget(self.y_fontSizeSpinBox)
        yTitlesHBox.addStretch()
        titleGraphHBox.addWidget(self.graphTitleLabel)
        titleGraphHBox.addWidget(self.graphTitle)
        titleGraphHBox.addWidget(self.titleFontSizeLB)
        titleGraphHBox.addWidget(self.titleFontSizeSB)
        titleGraphHBox.addStretch()
        figSizeXHBox.addWidget(self.figSizeLabelX)
        figSizeXHBox.addWidget(self.figSizeX)
        figSizeXHBox.addStretch()
        figSizeYHBox.addWidget(self.figSizeLabelY)
        figSizeYHBox.addWidget(self.figSizeY)
        figSizeYHBox.addStretch()
        dataSettHBox.addWidget(self.dataSettingsLabel)
        LchartSettingsHBox.addWidget(self.LChartLabel)
        lineRBHBox.addWidget(self.multipleColCB)
        lineRBHBox.addWidget(self.multipleColCBLabel)
        lineRBHBox.addStretch()
        emptyHBox.addWidget(self.emptyLabel)
        tSeriesLabelHBox.addWidget(self.tSeriesLabel)
        dateSettingsHBox.addWidget(self.dateCheckBox)
        dateSettingsHBox.addWidget(self.dateLabel1)
        dateSettingsHBox.addWidget(self.date1)
        dateSettingsHBox.addWidget(self.datelabel2)
        dateSettingsHBox.addWidget(self.date2)
        dateSettingsHBox.addWidget(self.setDateButton)
        dataColLabHBox.addWidget(self.columnsLabel)
        columnListHBox.addWidget(self.columns)
        buttonHBox.addWidget(self.selectColButton)
        buttonHBox.addWidget(self.browseColumnButton)
        buttonHBox.addWidget(self.clearSelectedButt)
        printGraphHBox.addWidget(self.printGraph)
        
        vbox.addLayout(buttonsLayout)
        vbox.addLayout(infoHLayout)
        vbox.addLayout(dataColLabHBox)
        vbox.addLayout(columnListHBox)
        vbox.addLayout(buttonHBox)
        vbox.addLayout(settingHBox)
        vbox.addLayout(rbHBox)
        vbox.addLayout(emptyHBox)
        vbox.addLayout(spinboxHBox)
        vbox.addLayout(markerHBox)
        vbox.addLayout(emptyLayout2)
        vbox.addLayout(xTitlesHBox)
        vbox.addLayout(yTitlesHBox)
        vbox.addLayout(titleGraphHBox)
        vbox.addLayout(figSizeXHBox)
        vbox.addLayout(figSizeYHBox)
        vbox.addLayout(dataSettHBox)
        vbox.addLayout(LchartSettingsHBox)
        vbox.addLayout(lineRBHBox)
        vbox.addLayout(emptyHBox)
        vbox.addLayout(tSeriesLabelHBox)
        vbox.addLayout(dateSettingsHBox)
        vbox.addLayout(printGraphHBox)
        vbox.addStretch()

        hbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()

        self.setLayout(hbox)
        self.show()
        self.loadFile_Button.clicked.connect(self.loadProcess)
        self.browseData_Button.clicked.connect(self.dataBrowse)
        self.selectColButton.clicked.connect(self.columnSelector)
        self.browseColumnButton.clicked.connect(self.columnBrowse)
        self.printGraph.clicked.connect(self.graphType)
        self.clearSelectedButt.clicked.connect(self.clearSelections)
        self.lineChartRB.toggled.connect(self.enableLineChartSelections)
        self.timeSeriesRB.toggled.connect(self.enableTimeSeriesSelections)
        self.dateCheckBox.toggled.connect(self.enableTimesSeriesQLines)
        self.setDateButton.clicked.connect(self.setDate)
        self.trendCheckBox.toggled.connect(self.enableTrendWidgets)
        self.spinbox.valueChanged.connect(self.setLineThickness)
        self.markerSizeSpinBox.valueChanged.connect(self.setMarkerSize)
        self.titleFontSizeSB.valueChanged.connect(self.setTitleFontSize)
        self.x_fontSizeSpinBox.valueChanged.connect(self.setXfontSize)
        self.y_fontSizeSpinBox.valueChanged.connect(self.setYfontSize)
        self.markerCB.currentIndexChanged.connect(self.setMarkerStyle)
        self.lineStyleCB.currentIndexChanged.connect(self.setLineStyle)
        self.y_fontSize = 13
        self.x_fontSize = 13
        self.titleFontSize = 15

    def setTitleFontSize(self):
        self.titleFontSize = int(self.titleFontSizeSB.value())

    def setXfontSize(self):
        self.x_fontSize = int(self.x_fontSizeSpinBox.value())

    def setYfontSize(self):
        self.y_fontSize = int(self.y_fontSizeSpinBox.value())

    def setMarkerStyle(self):
        if self.markerCB.currentIndex() == 1:
            self.markerStyle = "s"
            print(self.markerStyle)
        elif self.markerCB.currentIndex() == 2:
            self.markerStyle = "."
            print(self.markerStyle)
        elif self.markerCB.currentIndex() == 3:
            self.markerStyle = "x"
            print(self.markerStyle)
    
    def setMarkerSize(self):
        self.markerSize = self.markerSizeSpinBox.value()
        print(self.markerSize)

    def setLineThickness(self):
        self.lineWidth = self.spinbox.value()
        print(self.lineWidth)
    
    def setLineStyle(self):
        if self.lineStyleCB.currentIndex() == 1:
            self.lineStyle = "-"
            print(self.lineStyle)

        elif self.lineStyleCB.currentIndex() == 2:
            self.lineStyle = ":"
            print(self.lineStyle)

        elif self.lineStyleCB.currentIndex() == 3:
            self.lineStyle = "--"
            print(self.lineStyle)

    def enableTrendWidgets(self):
        if self.trendCheckBox.isChecked() == True:
            self.trendNoice.setEnabled(True)
            self.bollingerBandsCB.setEnabled(True)

            font.adjust_font(self.trendNoice, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#F5F57F")

            font.adjust_font(self.bollingerBandsCB, "QCheckBox", "Trebuchet MS", 
                        font_size=11, color="#61D9F7")
        else:
            self.trendNoice.setEnabled(False)
            self.bollingerBandsCB.setEnabled(False)
            self.trendNoice.setText("")
            self.bollingerBandsCB.setChecked(False)

            font.adjust_font(self.trendNoice, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#9E9E9E")

            font.adjust_font(self.bollingerBandsCB, "QCheckBox", "Trebuchet MS", 
                        font_size=11, color="#908F8F")
            
    def setDate(self):
        if len(self.date1.text() ) == 0 or len(self.date2.text() ) == 0:
            font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#F77361")
            font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#F77361")

            self.infoLabel.setText("Date couldn't set! Check the inputs please.")
            font.adjust_font(self.infoLabel, "QLabel", 
                            "Franklin Gothic Book", font_size=12, color="#FFB200", 
                            bg_color="#5F5F5F")
            
        else:
            self.first_date   = str(self.date1.text() )
            self.second_date  = str(self.date2.text() )

            font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#74F263")
            font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#74F263")
            
            self.infoLabel.setText("Date has set successfully!")
            font.adjust_font(self.infoLabel, "QLabel", 
                            "Franklin Gothic Book", font_size=12, color="#FFB200", 
                            bg_color="#5F5F5F")

    def enableTimesSeriesQLines(self):
        if self.dateCheckBox.isChecked() == True:
            self.date1.setEnabled(True)
            self.date2.setEnabled(True)
            self.setDateButton.setEnabled(True)
            font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#F5F57F")
            font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#F5F57F")

        elif self.dateCheckBox.isChecked() == False:
            self.date1.setEnabled(False)
            self.date2.setEnabled(False)
            self.setDateButton.setEnabled(False)

            font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#9E9E9E")
            font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#9E9E9E")
            
            self.date1.setText("")
            self.date2.setText("")

    def enableLineChartSelections(self):
        if self.lineChartRB.isChecked() == True:
            self.multipleColCB.setEnabled(True)

            font.adjust_font(self.multipleColCB, "QCheckBox", bg_color="")
            font.adjust_font(self.multipleColCBLabel, "QLabel", "Candara", 
                            font_size=12, color="white")

        elif self.lineChartRB.isChecked() == False:
            self.multipleColCB.setEnabled(False)

            font.adjust_font(self.multipleColCB, "QCheckBox", bg_color="#908F8F")
            font.adjust_font(self.multipleColCBLabel, "QLabel", "Candara", 
                            font_size=12, color="#908F8F")

    def enableTimeSeriesSelections(self):
        if self.timeSeriesRB.isChecked() == True:
            self.dateCheckBox.setEnabled(True)

            font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#9E9E9E")
            font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#9E9E9E")
            font.adjust_font(self.dateLabel1, "QLabel", "Candara", 
                            font_size=12, color="white")
            font.adjust_font(self.datelabel2, "QLabel", "Candara", 
                            font_size=12, color="white")
            font.adjust_font(self.setDateButton, "QPushButton", "Candara", 
                            font_size=12, bold=True, color="#0098FB", 
                            bg_color="black")
            font.adjust_font(self.dateCheckBox, "QCheckBox", "Candara", 
                            bg_color="")

        elif self.timeSeriesRB.isChecked() == False:
            self.dateCheckBox.setEnabled(False)
            self.date1.setEnabled(False)
            self.date2.setEnabled(False)
            self.setDateButton.setEnabled(False)

            font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#9E9E9E")
            font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                            font_size=10, color="#000000", bg_color="#9E9E9E")
            font.adjust_font(self.dateLabel1, "QLabel", "Candara", 
                            font_size=12, color="#908F8F")
            font.adjust_font(self.datelabel2, "QLabel", "Candara", 
                            font_size=12, color="#908F8F")
            font.adjust_font(self.setDateButton, "QPushButton", "Candara", 
                            font_size=12, bold=True, color="#908F8F", 
                            bg_color="black")
            font.adjust_font(self.dateCheckBox, "QCheckBox", "Candara", 
                            bg_color="#908F8F")

    def clearSelections(self):
        #Line chart
        self.CURRENT_COLUMN = None
        self.SELECTED_COLUMNS.clear()
        self.MULTIPLE_COLUMNS.clear()
        self.MULTIPLE_X = None
        self.singleColumn = None
        self.MULTIPLE_CHOICE = False
        self.columns.setEnabled(True)
        self.first_date = "default"
        self.second_date = "default"
         
        font.adjust_font(self.columns, "QListWidget", "Trebuchet MS", 
                        font_size=12, color="#FFBD06", bg_color="#5F5F5F")
        self.multipleColCB.setChecked(False)

        self.infoLabel.setText("All variables have cleared successfuly!")
        font.adjust_font(self.infoLabel, "QLabel", 
                        "Franklin Gothic Book", font_size=12, color="#FFB200", 
                        bg_color="#5F5F5F")

        #Time series
        self.dateCheckBox.setEnabled(False)
        self.date1.setEnabled(False)
        self.date2.setEnabled(False)
        self.setDateButton.setEnabled(False)

        font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")
        font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")
        font.adjust_font(self.dateLabel1, "QLabel", "Candara", 
                        font_size=12, color="#908F8F")
        font.adjust_font(self.datelabel2, "QLabel", "Candara", 
                        font_size=12, color="#908F8F")
        font.adjust_font(self.setDateButton, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#908F8F", 
                        bg_color="black")
        font.adjust_font(self.dateCheckBox, "QCheckBox", "Candara", 
                            bg_color="#908F8F")
        
        self.first_date = None
        self.second_date = None
        self.date1.setText("")
        self.date2.setText("")
        self.dateCheckBox.setChecked(False)

    def loadProcess(self):
        fileDialog = QtWidgets.QFileDialog()
        self.fName = fileDialog.getOpenFileName(None,'Load File')

        try:
            if self.fName[0]:
                data = pd.read_csv(self.fName[0])
                self.mainDF = pd.DataFrame(data)
                self.successfulLoad()
                self.listColumns()
        except:
            self.failureLoad()
    
    def listColumns(self):
        self.columns.clear()
        for column in list(self.mainDF.columns):
            self.columns.addItem(column)

    def columnSelector(self):
        self.CURRENT_COLUMN = self.columns.currentItem().text()
        self.SELECTED_COLUMNS.append(self.CURRENT_COLUMN)

        self.singleColumn = self.mainDF['{}'.format(self.CURRENT_COLUMN)]
        self.definingData()

    def successfulLoad(self):
        spliting_list = self.fName[0].split("/")
        loadedFileName = spliting_list[len(spliting_list)-1]
        self.infoLabel.setText("{} loaded successfully!".format(loadedFileName) )
        font.adjust_font(self.infoLabel, "QLabel", 
                        "Candara", font_size=12, 
                        bold=True, color="#00FF66", 
                        bg_color="#5F5F5F")

    def failureLoad(self):
        try:
            spliting_list = self.fName[0].split("/")
            loadedFileName = spliting_list[len(spliting_list)-1]
            self.infoLabel.setText("FAILED! {} couldn't load.".format(loadedFileName) )
            font.adjust_font(self.infoLabel, "QLabel", 
                            "Candara", font_size=12, 
                            bold=True, color="#FF0000", 
                            bg_color="#5F5F5F")
        except AttributeError:
            self.failureBrowse()

    def failureBrowse(self):
        self.infoLabel.setText("There isn't any loaded data to browse.")
        font.adjust_font(self.infoLabel, "QLabel", 
                        "Candara", font_size=12, 
                        bold=True, color="#FF0000", 
                        bg_color="#5F5F5F")

    def dataBrowse(self):

        try:
            self.isItSingleColumn = False
            self.openPage = DataBrowser(self.mainDF, self.isItSingleColumn)
        except AttributeError:
            self.failureLoad()

    def columnBrowse(self):

        try:
            self.isItSingleColumn = True
            self.singleColumn = self.mainDF['{}'.format(self.columns.currentItem().text() )]
            self.openPage = DataBrowser(self.singleColumn, self.isItSingleColumn)
        except AttributeError:
            self.failureLoad()

    def definingData(self):

        if self.multipleColCB.isChecked() == True:
            self.MULTIPLE_CHOICE = True
            self.MULTIPLE_COLUMNS.append(self.columns.currentItem().text() )

            self.columns.setEnabled(True)
            font.adjust_font(self.columns, "QListWidget", "Trebuchet MS", 
                            font_size=12, color="#FFBD06", bg_color="#5F5F5F")

            self.infoLabel.setText("Selected columns: {}".format(self.MULTIPLE_COLUMNS) )
            font.adjust_font(self.infoLabel, "QLabel", 
                            "Franklin Gothic Book", font_size=12, color="#FFB200", 
                            bg_color="#5F5F5F")

    def graphType(self):
        if self.timeSeriesRB.isChecked() == True:
            self.timeSeriesGraph()
        elif self.lineChartRB.isChecked() == True:
            self.lineGraph()
        else:
            print("it was at this moment, he knew, he fucked up (graph type)")
        
    def timeSeriesGraph(self):
        try:
            if self.trendCheckBox.isChecked() == False:
                print("no trend!")
                if len(self.first_date) == 10 and len(self.second_date) == 10:
                    
                    selectedValues = self.columns.currentItem().text()
                    data = pd.read_csv(self.fName[0],index_col='Date',parse_dates=True)
                    data[selectedValues].plot(figsize=(float(self.figSizeX.text() ), float(self.figSizeY.text()) ),
                                                                    xlim=[self.first_date, self.second_date],
                                                                    linewidth = int(self.lineWidth),
                                                                    marker = self.markerStyle, markersize = int(self.markerSize),
                                                                    linestyle = self.lineStyle
                                                                    )
                    plt.ylabel(self.yTitle.text(), fontsize = self.y_fontSize)
                    plt.xlabel(self.xTitle.text(), fontsize = self.x_fontSize)
                    plt.title(self.graphTitle.text(), fontsize = self.titleFontSize)
                    plt.show()
                else:
                    selectedValues = self.columns.currentItem().text()
                    data = pd.read_csv(self.fName[0],index_col='Date',parse_dates=True)
                    data[selectedValues].plot(figsize=(float(self.figSizeX.text() ), float(self.figSizeY.text()) ), 
                                              linewidth = int(self.lineWidth), 
                                              marker = self.markerStyle, markersize = int(self.markerSize),
                                              linestyle = self.lineStyle )

                    plt.ylabel(self.yTitle.text(), fontsize = self.y_fontSize)
                    plt.xlabel(self.xTitle.text(), fontsize = self.x_fontSize)
                    plt.title(self.graphTitle.text(), fontsize = self.titleFontSize)
                    plt.show()


            elif self.trendCheckBox.isChecked() == True and self.bollingerBandsCB.isChecked() == False:
                print("trendcheck box true!")

                if len(self.trendNoice.text() ) == 00:
                    font.adjust_font(self.trendNoice, "QLineEdit", bg_color="#F77561")
                else:
                    font.adjust_font(self.trendNoice, "QLineEdit", bg_color="#74F263")

                selectedValues = self.columns.currentItem().text()
                data = pd.read_csv(self.fName[0],index_col='Date',parse_dates=True)
                data['{} Trend'.format(selectedValues)] = data['{}'.format(selectedValues)].rolling(window=int(self.trendNoice.text()) ).mean()
                
                if len(self.first_date) > 7 or len(self.second_date) > 7:
                    data[[selectedValues, '{} Trend'.format(selectedValues)]].plot(figsize=(float(self.figSizeX.text() ), 
                                                                    float(self.figSizeY.text()) ),
                                                                    xlim=[self.first_date, self.second_date],
                                                                    linewidth = int(self.lineWidth),
                                                                    marker = self.markerStyle, markersize = int(self.markerSize),
                                                                    linestyle = self.lineStyle)
                else:
                    data[[selectedValues, '{} Trend'.format(selectedValues)]].plot(figsize=(float(self.figSizeX.text() ), 
                                                                    float(self.figSizeY.text()) ),
                                                                    linewidth = int(self.lineWidth),
                                                                    marker = self.markerStyle, markersize = int(self.markerSize),
                                                                    linestyle = self.lineStyle)
                plt.ylabel(self.yTitle.text(), fontsize = self.y_fontSize)
                plt.xlabel(self.xTitle.text(), fontsize = self.x_fontSize)
                plt.title(self.graphTitle.text(), fontsize = self.titleFontSize)
                plt.show()

            elif self.trendCheckBox.isChecked() == True and self.bollingerBandsCB.isChecked() == True:
                if len(self.trendNoice.text() ) == 00:
                    font.adjust_font(self.trendNoice, "QLineEdit", bg_color="#F77561")
                else:
                    font.adjust_font(self.trendNoice, "QLineEdit", bg_color="#74F263")
                
                selectedValues = self.columns.currentItem().text()
                data = pd.read_csv(self.fName[0],index_col='Date',parse_dates=True)
                data['{} Trend'.format(selectedValues)] = data['{}'.format(selectedValues)].rolling(window=int(self.trendNoice.text()) ).mean()
                data['Upper'] = data['{} Trend'.format(selectedValues)] + 2*data['{}'.format(selectedValues)].rolling(window=int(self.trendNoice.text()) ).std()
                data['Lower'] = data['{} Trend'.format(selectedValues)] - 2*data['{}'.format(selectedValues)].rolling(window=int(self.trendNoice.text()) ).std()
                
                if len(self.first_date) > 7 or len(self.second_date) > 7:
                    data[[selectedValues, '{} Trend'.format(selectedValues), 'Upper', 'Lower']].plot(figsize=(float(self.figSizeX.text() ), 
                                                                    float(self.figSizeY.text()) ),
                                                                    xlim=[self.first_date, self.second_date],
                                                                    linewidth = int(self.lineWidth),
                                                                    marker = self.markerStyle, markersize = int(self.markerSize),
                                                                    linestyle = self.lineStyle)
                else:
                    data[[selectedValues, '{} Trend'.format(selectedValues), 'Upper', 'Lower']].plot(figsize=(float(self.figSizeX.text() ), 
                                                                    float(self.figSizeY.text()) ),
                                                                    linewidth = int(self.lineWidth),
                                                                    marker = self.markerStyle, markersize = int(self.markerSize),
                                                                    linestyle = self.lineStyle)
                plt.ylabel(self.yTitle.text(), fontsize = self.y_fontSize)
                plt.xlabel(self.xTitle.text(), fontsize = self.x_fontSize)
                plt.title(self.graphTitle.text(), fontsize = self.titleFontSize)
                plt.show()

        except ValueError:
            if len(self.first_date) == 10 and len(self.second_date) == 10:
                data = pd.read_csv(self.fName[0],index_col='Date',parse_dates=True)
                data[self.columns.currentItem().text()].plot(xlim=[self.first_date, self.second_date])
                plt.ylabel(self.yTitle.text(), fontsize = self.y_fontSize)
                plt.xlabel(self.xTitle.text(), fontsize = self.x_fontSize)
                plt.title(self.graphTitle.text(), fontsize = self.titleFontSize)
                plt.show()
            else:
                data = pd.read_csv(self.fName[0],index_col='Date',parse_dates=True)
                data[self.columns.currentItem().text()].plot()
                plt.ylabel(self.yTitle.text(), fontsize = self.y_fontSize)
                plt.xlabel(self.xTitle.text(), fontsize = self.x_fontSize)
                plt.title(self.graphTitle.text(), fontsize = self.titleFontSize)
                plt.show()

    def lineGraph(self):
        if self.MULTIPLE_CHOICE == False:
            try:
                fig_lineGraph = plt.figure(figsize=(float(self.figSizeX.text() ), 
                                            float(self.figSizeY.text()) ), 
                                            dpi=100)
                axes = fig_lineGraph.add_axes([0.1, 0.1, 0.8, 0.8])
                self.singleColumn = self.mainDF['{}'.format(self.columns.currentItem().text() )]
                self.X = self.singleColumn

                axes.plot(self.X, linewidth = self.lineWidth, marker = self.markerStyle, 
                          markersize = int(self.markerSize), linestyle = self.lineStyle)
                axes.set_xlabel(str(self.xTitle.text()), fontsize = self.x_fontSize)
                axes.set_ylabel(str(self.yTitle.text()), fontsize = self.y_fontSize)
                axes.set_title(str(self.graphTitle.text()), fontsize = self.titleFontSize)
                axes.grid(True)
                plt.show()
                
            except ValueError:
                fig_lineGraph = plt.figure()
                axes = fig_lineGraph.add_axes([0.1, 0.1, 0.8, 0.8])
                axes.plot(self.X, linewidth = self.lineWidth, marker = self.markerStyle, 
                          markersize = int(self.markerSize), linestyle = self.lineStyle)
                axes.grid(True)
                plt.show()

        elif self.MULTIPLE_CHOICE == True:
            try:
                fig_lineGraph = plt.figure(figsize=(float(self.figSizeX.text() ), 
                                            float(self.figSizeY.text()) ), 
                                            dpi=100, linewidth = self.lineWidth, 
                                            marker = self.markerStyle, markersize = int(self.markerSize), 
                                            linestyle = self.lineStyle)

                axes = fig_lineGraph.add_axes([0.1, 0.1, 0.8, 0.8])

                for i in range(0, len(self.MULTIPLE_COLUMNS)):
                    axes.plot(self.mainDF[self.MULTIPLE_COLUMNS[i]], label=self.MULTIPLE_COLUMNS[i],
                                          linewidth = self.lineWidth, marker = self.markerStyle, 
                                          markersize = int(self.markerSize), linestyle = self.lineStyle)

                axes.set_xlabel(str(self.xTitle.text()), fontsize = self.x_fontSize)
                axes.set_ylabel(str(self.yTitle.text()), fontsize = self.y_fontSize)
                axes.set_title(str(self.graphTitle.text()), fontsize = self.titleFontSize)

                axes.grid(True)
                axes.legend()
                plt.show()

            except ValueError:
                fig_lineGraph = plt.figure()

                axes = fig_lineGraph.add_axes([0.1, 0.1, 0.8, 0.8])

                for i in range(0, len(self.MULTIPLE_COLUMNS)):
                    axes.plot(self.mainDF[self.MULTIPLE_COLUMNS[i]], label=self.MULTIPLE_COLUMNS[i])

                axes.grid(True)
                axes.legend()
                plt.show()

    def theme(self):
        font.adjust_font(self.loadFile_Label, "QLabel", "Trebuchet MS", 
                        font_size=14, bold=True, color="#0098FB")

        font.adjust_font(self.loadFile_Button, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#0098FB", 
                        bg_color="black")

        font.adjust_font(self.browseData_Button, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#0098FB", 
                        bg_color="black")

        font.adjust_font(self.infoLabel, "QLabel", "Candara", 
                        font_size=12, bold=True, color="black", 
                        bg_color="#5F5F5F")

        font.adjust_font(self.settingsLabel, "QLabel", "Trebuchet MS", 
                        font_size=14, bold=True, color="#0098FB")

        font.adjust_font(self.timeSeriesRB, "QRadioButton", "Trebuchet MS", 
                        font_size=11, color="#FFBD06")

        font.adjust_font(self.lineChartRB, "QRadioButton", "Trebuchet MS", 
                        font_size=11, color="#FFBD06")

        font.adjust_font(self.spinboxLabel, "QLabel", "Trebuchet MS", 
                        font_size=12, color="#FFBD06")

        font.adjust_font(self.markerLabel, "QLabel", "Trebuchet MS", 
                        font_size=12, color="#FFBD06")

        font.adjust_font(self.trendCheckBox, "QCheckBox", "Trebuchet MS", 
                        font_size=11, color="#FFBD06")

        font.adjust_font(self.yTitleLabel, "QLabel", "Candara", 
                        font_size=12, color="#3685FA")

        font.adjust_font(self.xTitleLabel, "QLabel", "Candara", 
                        font_size=12, color="#3685FA")

        font.adjust_font(self.graphTitleLabel, "QLabel", "Candara", 
                        font_size=12, color="#3685FA")

        font.adjust_font(self.figSizeLabelX, "QLabel", "Candara", 
                        font_size=12, color="#3685FA")

        font.adjust_font(self.figSizeLabelY, "QLabel", "Candara", 
                        font_size=12, color="#3685FA")

        font.adjust_font(self.graphTitle, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")

        font.adjust_font(self.xTitle, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")

        font.adjust_font(self.yTitle, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")

        font.adjust_font(self.figSizeX, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")

        font.adjust_font(self.figSizeY, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")
        
        font.adjust_font(self.lineThicknessTip, "QLabel", font_type= "Calibri", color="#DCDCDC", font_size= 10, italic=True)

        font.adjust_font(self.markerTip, "QLabel", font_type= "Calibri", color="#DCDCDC", font_size= 10, italic=True)

        font.adjust_font(self.dataSettingsLabel, "QLabel", "Trebuchet MS", 
                        font_size=14, bold=True, color="#0098FB")

        font.adjust_font(self.columns, "QListWidget", "Trebuchet MS", 
                        font_size=12, color="#FFBD06", bg_color="#5F5F5F")

        font.adjust_font(self.columnsLabel, "QLabel", "Candara", 
                        font_size=13, color="#DADADA")

        font.adjust_font(self.selectColButton, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#0098FB", 
                        bg_color="black")

        font.adjust_font(self.browseColumnButton, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#0098FB", 
                        bg_color="black")

        font.adjust_font(self.clearSelectedButt, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#0098FB", 
                        bg_color="black")

        font.adjust_font(self.printGraph, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#0098FB", 
                        bg_color="black")

        font.adjust_font(self.date1, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")

        font.adjust_font(self.date2, "QLineEdit", "Trebuchet MS", 
                        font_size=10, color="#000000", bg_color="#9E9E9E")

        font.adjust_font(self.dateLabel1, "QLabel", "Candara", 
                        font_size=12, color="white")

        font.adjust_font(self.datelabel2, "QLabel", "Candara", 
                        font_size=12, color="white")

        font.adjust_font(self.setDateButton, "QPushButton", "Candara", 
                        font_size=12, bold=True, color="#0098FB", 
                        bg_color="black")

        font.adjust_font(self.LChartLabel, "QLabel", "Trebuchet MS", 
                        font_size=11, color="#EEEE00")

        font.adjust_font(self.tSeriesLabel, "QLabel", "Trebuchet MS", 
                        font_size=11, color="#EEEE00")
        
        font.adjust_font(self.lineStyleCB, "QComboBox", font_type="Calibri",
                        font_size=11, bg_color="#B2B0B0", color="black")

        font.adjust_font(self.markerCB, "QComboBox", font_type="Calibri",
                        font_size=11, bg_color="#B2B0B0", color="black")

        font.adjust_font(self.spinbox, "QSpinBox", font_type="Calibri",
                        font_size=10, color="black")

        font.adjust_font(self.markerSizeSpinBox, "QSpinBox", font_type="Calibri",
                        font_size=10, color="black")

        font.adjust_font(self.titleFontSizeLB, "QLabel", font_type="Trebuchet MS",
                        font_size=10, color="#F0FFFF")

        font.adjust_font(self.x_fontSizeLabel, "QLabel", font_type="Trebuchet MS",
                        font_size=10, color="#F0FFFF")

        font.adjust_font(self.y_fontSizeLabel, "QLabel", font_type="Trebuchet MS",
                        font_size=10, color="#F0FFFF")

        font.adjust_font(self.titleFontSizeSB, "QSpinBox", font_type="Calibri",
                        font_size=10, color="black")

        font.adjust_font(self.x_fontSizeSpinBox, "QSpinBox", font_type="Calibri",
                        font_size=10, color="black")

        font.adjust_font(self.y_fontSizeSpinBox, "QSpinBox", font_type="Calibri",
                        font_size=10, color="black")


class DataBrowser(QtWidgets.QWidget):
    def __init__(self, df, condition):
        super().__init__()
        self.setWindowTitle("Data Browser")
        self.init_ui()
        self.setTable(df, condition)

    def init_ui(self):
        self.dataTable = QtWidgets.QTableWidget()
        font.adjust_font(self.dataTable, "QTableWidget", "Trebuchet MS", 14, 
                        bold=True, color="#0098FB", bg_color="#505050")
        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()

        vbox.addWidget(self.dataTable)

        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.show()

    def setTable(self, df, condition):
        if condition == False:
            self.df_row = df.shape[0]
            self.df_col = df.shape[1]

            self.dataTable.setRowCount(self.df_row)
            self.dataTable.setColumnCount(self.df_col)

            for rowIndex in range(0, self.df_row):
                for colIndex in range(0, self.df_col):
                    cell = df.iat[rowIndex,colIndex]
                    self.dataTable.setItem(rowIndex,colIndex, QtWidgets.QTableWidgetItem(str(cell)))
        else:
            self.df_row = df.shape[0]

            self.dataTable.setRowCount(self.df_row)
            self.dataTable.setColumnCount(1)

            for rowIndex in range(0, self.df_row):
                cell = df.iat[rowIndex]
                self.dataTable.setItem(rowIndex,0, QtWidgets.QTableWidgetItem(str(cell)))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    #window.move(400, 80)
    #window.setFixedSize(550, 850)
    app.setStyle("Fusion")
    window.setStyleSheet("Window {background : #505050;}")
    sys.exit(app.exec_())
