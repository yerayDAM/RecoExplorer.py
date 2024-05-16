from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox
import portScanv2
import subd, directoryListingFunction, FuncVirusTotalApi
import webCrawlingv2
import os
from db.insertarDatos import conectar_db, cerrar_db, insertar_ultimas_ejecuciones, insertar_informacion_direcciones_ip, insertar_informacion_dominios, insertar_informacion_web_crawling, insertar_informacion_escaneo_directorios
from db.consultas import conectar_db,cerrar_db, consultar_ultimas_ejecuciones, consultar_ultimas_ejecuciones_valor, consultar_ultimas_ejecuciones_where_tipo, consultar_ultimas_ejecuciones_where_tipo_valor, consultar_informacion_direcciones_ip, consultar_informacion_direcciones_ip_valor, consultar_informacion_dominios, consultar_informacion_dominios_valor, consultar_informacion_escaneo_directorios, consultar_informacion_escaneo_directorios_valor, consultar_informacion_web_crawling, consultar_informacion_web_crawling_valor

class Worker(QThread):
    finished = pyqtSignal(list)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip

    def run(self):
        resultado = portScanv2.scan_ip(self.ip)
        if resultado is not None:
            self.finished.emit(resultado)

class WorkerInfoIp(QThread):
    finished = pyqtSignal(list)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip

    def run(self):
        resultado = FuncVirusTotalApi.consultar_ip(self.ip)
        if resultado is not None:
            self.finished.emit(resultado)

class Worker1(QThread):
    finished = pyqtSignal(list,object)

    def __init__(self, dominio):
        super().__init__()
        self.dominio = dominio

    def run(self):
        resultado = subd.subDomain(self.dominio)
        resultado_imagen = subd.obtener_imagen_dns_dumpster(self.dominio)
        if resultado is not None:
            self.finished.emit(resultado,resultado_imagen)
class Worker2(QThread):
    finished = pyqtSignal(list)

    def __init__(self, url, wordlist):
        super().__init__()
        self.url = url
        self.wordlist = wordlist

    def run(self):
        resultado = directoryListingFunction.check_wordlist_for_domain(self.url,self.wordlist)
        if resultado is not None:
            self.finished.emit(resultado)

class CustomTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.rootItem = self.createTree(data)

    def createTree(self, data):
        rootItem = TreeItem(None)
        self.populateTree(data, rootItem)
        return rootItem

    def populateTree(self, data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                childItem = TreeItem([key, None])
                parent.appendChild(childItem)
                self.populateTree(value, childItem)
        elif isinstance(data, list):
            for item in data:
                childItem = TreeItem([None, item])
                parent.appendChild(childItem)
                self.populateTree(item, childItem)
        else:
            if data is not None and data != '':
                parent.itemData[1] = data

    def rowCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().childCount()
        return self.rootItem.childCount()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parentItem
        if parentItem is None:
            return QtCore.QModelIndex()  # Devolver un índice inválido si parentItem es None
        return self.createIndex(parentItem.row(), 0, parentItem)

class TreeItem:
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def data(self, column):
        return self.itemData[column]

class myMainWindow(object):
    def __init__(self, app):
        self.app = app # call init of QMainWindow, or QWidget or whatever)

        # se añade la intefaz que se desee
        self.ui = uic.loadUi('view/GUI_dominiosYipsv2.UI')

        """ Sirve para quitar la parte de arriba de la applicaion añadida de forma nativa self.ui.setWindowFlags(self.ui.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.ui.setWindowFlags(self.ui.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.ui.setWindowFlags(self.ui.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)
        self.ui.setWindowFlags(self.ui.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.ui.setWindowFlag(QtCore.Qt.FramelessWindowHint)"""
#       Inicializar el texto original de los labels
        self.originalLabelTexts = {
        self.ui.label_9: self.ui.label_9.text(),
        self.ui.label_8: self.ui.label_8.text(),
        self.ui.label_2: self.ui.label_2.text(),
        self.ui.label_11: self.ui.label_11.text(),
        self.ui.label_10: self.ui.label_10.text(),
        self.ui.label_3: self.ui.label_3.text(),
        self.ui.label_4: self.ui.label_4.text(),
        }
        resultadoPuertoCa = "Puerto"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoPuerto = QtWidgets.QTableWidgetItem(resultadoPuertoCa)
        resultadoOpenCa = "Estado"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoOpen = QtWidgets.QTableWidgetItem(resultadoOpenCa)
        resultadoServiceCa = "Servicio"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoService = QtWidgets.QTableWidgetItem(resultadoServiceCa)

        self.ui.tableWidget.setHorizontalHeaderItem(0, resultadoPuerto)
        self.ui.tableWidget.setHorizontalHeaderItem(1, resultadoOpen)
        self.ui.tableWidget.setHorizontalHeaderItem(2, resultadoService)

        # Configurar el tamaño de las columna
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.frame_toggle.hide()
            self.ui.frame_left_menu.hide()
        else:
            self.ui.frame_toggle.show()
            self.ui.frame_left_menu.show()
        resultadoUrlCa = "URL"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoUrl = QtWidgets.QTableWidgetItem(resultadoUrlCa)
        resultadoCodeCa = "Codigo de respuesta"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoCode = QtWidgets.QTableWidgetItem(resultadoCodeCa)

        self.ui.tableWidget_4.setHorizontalHeaderItem(0, resultadoUrl)
        self.ui.tableWidget_4.setHorizontalHeaderItem(1, resultadoCode)
        # se añade la funcionalidad de los botones es decir se enlaza con su función
        self.ui.stackedWidget.currentChanged.connect(self.actualizar_visibilidad)

        #boton home
        self.ui.pushButton_9.clicked.connect(self.paginaHome)
        
        self.ui.pushButton_2.clicked.connect(self.paginaEscanerPuerto)#boton lateral
        self.ui.pushButton_13.clicked.connect(self.paginaEscanerDominio)#boton lateral
        self.ui.pushButton_3.clicked.connect(self.paginaEscanerDirectorios)#boton lateral
        self.ui.pushButton_6.clicked.connect(self.paginaWebcrawling)#boton lateral
        self.ui.pushButton_8.clicked.connect(self.paginaResultados)#boton lateral

        self.ui.pushButton_5.clicked.connect(self.paginaEscanerPuerto)#boton principal
        self.ui.pushButton_4.clicked.connect(self.paginaEscanerDominio)#boton principal
        self.ui.pushButton_7.clicked.connect(self.paginaEscanerDirectorios)#boton principal
        self.ui.pushButton.clicked.connect(self.paginaWebcrawling)#boton principal
        self.ui.pushButton_14.clicked.connect(self.paginaResultados)#boton principal

        self.ui.btn_close.clicked.connect(self.cerrar_aplicacion)


        self.ui.btn_toggle_menu.clicked.connect(self.menu)
        self.ui.escanear.clicked.connect(self.iniciar_escaneo)
        self.ui.escanear_3.clicked.connect(self.iniciar_escaneo_dominio)
        self.ui.escanear_9.clicked.connect(self.iniciar_webcrawling)
        self.ui.escanear_5.clicked.connect(self.iniciar_escaneo_directorios)

# botones radios consultas ultimas ejecuciones
        self.ui.buscar_2.clicked.connect(self.actualizar_tabla_desde_radio_button)
        self.ui.buscar.clicked.connect(self.actualizar_tabla_ip)
        self.ui.buscar_3.clicked.connect(self.actualizar_tabla_dominios)
        self.ui.buscar_7.clicked.connect(self.actualizar_tabla_escanerDirectorios)
        self.ui.buscar_8.clicked.connect(self.actualizar_tabla_webcrawling)

        current_directory = os.getcwd()
        dicc_directory = os.path.join(current_directory, "dicc")
        file_list = os.listdir(dicc_directory)
        for file_name in file_list:
            full_path = os.path.join(dicc_directory, file_name)
            self.ui.comboBox.addItem(full_path)

        # se crean las variables qUe se van a usar dentro de las funciones usadas por los botones.
        self.front_wid= 1
        self.front_wid2= 1
        self.menu_num = 0
        self.resultadoVirusTotal = ''

        # se muestra la interfaz
        self.ui.show()
        self.run()

    def run(self):
        self.app.exec_()

#/////////////////////////////////////////////
#                                          ///
# START FUNCIONES AÑADIDAS                 ///
#                                          ///
#/////////////////////////////////////////////
    def cerrar_aplicacion(self):
        QtCore.QCoreApplication.quit()  # Cerrar la aplicación

    #/////////////////////////////////////////////
    #                                          ///
    # START LLAMAR ESCANER DOMINIOS            ///
    #                                          ///
    #/////////////////////////////////////////////
    def iniciar_escaneo_dominio(self):
        dominio = self.ui.lineEdit_3.text()
        self.worker = Worker1(dominio)
        self.worker.finished.connect(self.actualizar_tabla_dominio)
        self.worker.start()
        self.ui.escanear_3.setEnabled(False)

    def actualizar_tabla_dominio(self, resultado, resultado_imagen):
        # Habilitar el botón de escaneo
        self.ui.escanear_3.setEnabled(True)
    
        # Limpiar la tabla antes de llenarla
        self.ui.tableWidget_2.clearContents()
        pixmap = QPixmap(resultado_imagen)
        self.ui.label_14.setPixmap(pixmap)
    
        # Calcular el número de registros por cada campo
        registros_por_campo = (len(resultado) + 3) // 4
    
        # Establecer el número de columnas en la tabla
        num_columnas = 4
        self.ui.tableWidget_2.setColumnCount(num_columnas)
        # Antes de llenar la tabla
        self.ui.tableWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
        # Rellenar la tabla en columnas con el número calculado de registros por campo
        for i in range(num_columnas):
            # Calcular el índice inicial y final del bloque actual
            start_index = i * registros_por_campo
            end_index = min(start_index + registros_por_campo, len(resultado))
        
            # Crear una lista de registros para el campo actual
            registros_campo = resultado[start_index:end_index]
        
            # Llenar la columna actual con los registros del campo actual
            for row, registro in enumerate(registros_campo):
                item = QtWidgets.QTableWidgetItem(registro)
                self.ui.tableWidget_2.setItem(row, i, item)
        conexion = conectar_db()
        insertar_ultimas_ejecuciones(conexion, "Dominio", self.ui.lineEdit_3.text())
        insertar_informacion_dominios(conexion, self.ui.lineEdit_3.text(), resultado_imagen, str(resultado))
#    resultados_ultimas_ejecuciones_dominios = consultar_informacion_dominios(conexion)
#    print("Últimas Ejecuciones:")
#    for resultado in resultados_ultimas_ejecuciones_dominios:
#        print(resultado)
        cerrar_db(conexion)
    #/////////////////////////////////////////////
    #                                          ///
    # END LLAMAR ESCANER DOMINIOS              ///
    #                                          ///
    #/////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START ESCANER DE PUERTOS IP              ///
    #                                          ///
    #/////////////////////////////////////////////
    def iniciar_escaneo(self):
        ip = self.ui.lineEdit.text()
        self.workerInfo = WorkerInfoIp(ip)
        self.worker = Worker(ip)
        self.workerInfo.finished.connect(self.actualizar_labels)
        self.worker.finished.connect(self.actualizar_tabla)
        self.workerInfo.start()
        self.worker.start()
        self.ui.escanear.setEnabled(False)

    def actualizar_labels(self, resultado):
        ip, tipo, owner, common_name, network, continent, country, reputation_malicious, reputation_suspicious, reputation_harmless = resultado[0]
        # Obtener el texto original de los labels
        originalTexts = self.originalLabelTexts
        # Actualizar cada label agregando los nuevos datos al texto original
        self.ui.label_9.setText(originalTexts[self.ui.label_9] + "" + ip)
        self.ui.label_8.setText(originalTexts[self.ui.label_8] + "" + tipo)
        self.ui.label_2.setText(originalTexts[self.ui.label_2] + " " + str(owner) if owner is not None else " N/A")
        self.ui.label_11.setText(originalTexts[self.ui.label_11] + "" + str(common_name) if common_name is not None else " N/A")
        self.ui.label_10.setText(originalTexts[self.ui.label_10] + "" + network if network is not None else " N/A")
        self.ui.label_3.setText(originalTexts[self.ui.label_3] + "" + continent if continent is not None else " N/A"  + " - " + country if country is not None else " N/A")
        self.ui.label_4.setText(originalTexts[self.ui.label_4] + "(Harmless) - " + str(reputation_harmless) + " (Malicious) - " + str(reputation_malicious) + " (Suspicious) - " + str(reputation_suspicious))
        print("IP:", ip)
        print("Tipo:", tipo)
        print("Owner:", owner)
        print("Common Name:", common_name)
        print("Network:", network)
        print("Continent:", continent)
        print("Country:", country)
        print("Reputation (Malicious):", reputation_malicious)
        print("Reputation (Suspicious):", reputation_suspicious)
        print("Reputation (Harmless):", reputation_harmless)
        self.resultadoVirusTotal = resultado[0]
        self.workerInfo.deleteLater()

    def actualizar_tabla(self, resultado):
        print("aaaaaaaaaaaaaaaaaaaaa")
        self.ui.tableWidget.setRowCount(len(resultado))
        resultadoPuertoCa = "Puerto"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoPuerto = QtWidgets.QTableWidgetItem(resultadoPuertoCa)
        resultadoOpenCa = "Estado"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoOpen = QtWidgets.QTableWidgetItem(resultadoOpenCa)
        resultadoServiceCa = "Servicio"  # El nuevo nombre que deseas asignar a la cabecera
        resultadoService = QtWidgets.QTableWidgetItem(resultadoServiceCa)
        for row, data in enumerate(resultado):
            for col, value in enumerate(data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(row, col, item)
        self.ui.tableWidget.setHorizontalHeaderItem(0, resultadoPuerto)
        self.ui.tableWidget.setHorizontalHeaderItem(1, resultadoOpen)
        self.ui.tableWidget.setHorizontalHeaderItem(2, resultadoService)
        conexion = conectar_db()
        if hasattr(self, 'resultadoVirusTotal'):
            print(str(self.resultadoVirusTotal))
            virusT = self.resultadoVirusTotal
            insertar_ultimas_ejecuciones(conexion, "DireccionIP", self.ui.lineEdit.text())
            insertar_informacion_direcciones_ip(conexion, self.ui.lineEdit.text(), str(resultado), str(virusT))
        else:
            print("Error: resultadoVirusTotal no está disponible.")
        #insertar_ultimas_ejecuciones(conexion, "DireccionIP", self.ui.lineEdit.text())
        #insertar_informacion_direcciones_ip(conexion, self.ui.lineEdit.text(), str(resultado),str(self.resultadoVirusTotal))
        cerrar_db(conexion)
        self.ui.escanear.setEnabled(True)
        self.worker.deleteLater()
    #/////////////////////////////////////////////
    #                                          ///
    # END ESCANER DE PUERTOS IP / DOMINOS      ///
    #                                          ///
    #/////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START ESCANER DE DIRECTORIOS             ///
    #                                          ///
    #/////////////////////////////////////////////
    def iniciar_escaneo_directorios(self):
        url = self.ui.lineEdit_5.text()
        wordlist = self.ui.comboBox.currentText()
        print(wordlist)
        self.worker = Worker2(url,wordlist)
        self.worker.finished.connect(lambda result: self.actualizar_tabla_directorio(result, url))
        self.worker.start()
        self.ui.escanear_5.setEnabled(False)


    def actualizar_tabla_directorio(self, resultado, url):
        self.ui.tableWidget_4.setRowCount(len(resultado))

        max_length = 0  # Para almacenar la longitud máxima del texto en la primera columna
        for row, data in enumerate(resultado):
            for col, value in enumerate(data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.ui.tableWidget_4.setItem(row, col, item)
                if col == 0 and len(str(value)) > max_length:
                    max_length = len(str(value))
        if max_length > 0:
            self.ui.tableWidget_4.setColumnWidth(0, max_length * 10)  # Ajusta el multiplicador según sea necesario

        conexion = conectar_db()
        insertar_ultimas_ejecuciones(conexion, "RutaEscaneo", url)
        insertar_informacion_escaneo_directorios(conexion, url, str(resultado))
#        resultados_ultimas_ejecuciones = consultar_informacion_escaneo_directorios(conexion)
#        print("Últimas Ejecuciones:")
#        for resultado in resultados_ultimas_ejecuciones:
#            print(resultado)
        cerrar_db(conexion)
        self.ui.escanear_5.setEnabled(True)
    #/////////////////////////////////////////////
    #                                          ///
    # END ESCANER DE DIRECTORIOS               ///
    #                                          ///
    #/////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START OCULTAR MENU                       ///
    #                                          ///
    #/////////////////////////////////////////////
    def actualizar_visibilidad(self, index):
        # Si se muestra el primer widget, ocultar los elementos
        if index == 0:
            self.ui.frame_toggle.hide()
            self.ui.frame_left_menu.hide()
        else:
            self.ui.frame_toggle.show()
            self.ui.frame_left_menu.show()
    #/////////////////////////////////////////////
    #                                          ///
    # END OCULTAR MENU                         ///
    #                                          ///
    #/////////////////////////////////////////////

    
    #/////////////////////////////////////////////
    #                                          ///
    # START WEBCRAWLING                        ///
    #                                          ///
    #/////////////////////////////////////////////
#    def sort_and_clean_json(self, data):
#        # Función para ordenar el JSON por el número de elementos y limpiar los valores vacíos
#        def sort_and_clean(item):
#            if isinstance(item, dict):
#                # Ordenar el diccionario por el número de elementos en los valores
#                sorted_items = sorted(item.items(), key=lambda x: len(x[1]), reverse=True)
#                # Eliminar valores vacíos
#                cleaned_items = [(k, sort_and_clean(v)) for k, v in sorted_items if v]
#                return dict(cleaned_items)
#            elif isinstance(item, list):
#                # Eliminar elementos vacíos de la lista
#                return [sort_and_clean(elem) for elem in item if elem]
#            else:
#                # Mantener otros tipos de datos
#                return item
#
#        return sort_and_clean(data)

    def iniciar_webcrawling(self):
        url = self.ui.lineEdit_9.text()

        arbol_directorios = webCrawlingv2.obtener_contenido_html(url)
        print("aaaaaaaaaaaaaaaaasdddddddddddddddddddddddddsa\n\n")
        print(arbol_directorios)
        # Lista para almacenar los segundos valores
        second_values = []
        # Iterar sobre cada tupla y obtener el segundo valor
        for _, value in arbol_directorios:
            second_values.append(value)
        print("aaaaaaaaaaaaaaaaasdddddddddddddddddddddddddsa\n\n")
        print(second_values)
        sorted_data = sorted(second_values, reverse=True)
        self.ui.tableWidget_8.setRowCount(len(sorted_data))
        self.ui.tableWidget_8.setColumnCount(1)  # Ajusta el número de columnas según tus necesidades

        # Iterar sobre cada valor y agregarlos al QTableWidget
        for i, value in enumerate(sorted_data):
            # Establecer el valor en la celda correspondiente
            self.ui.tableWidget_8.setItem(i, 0, QTableWidgetItem(value))

        conexion = conectar_db()
        insertar_ultimas_ejecuciones(conexion, "URL", url)
        insertar_informacion_web_crawling(conexion, url, str(arbol_directorios))
#        resultados_ultima_ejecucion_web_crawling = consultar_informacion_web_crawling(conexion)
#        print("Últimas Ejecuciones:")
#        for resultado in resultados_ultima_ejecucion_web_crawling:
#            print(resultado)
        cerrar_db(conexion)
        #if arbol_directorios:
        #    sorted_data = self.sort_and_clean_json(arbol_directorios)
        #    print(sorted_data)
        #    self.model = CustomTreeModel(sorted_data)
        #    print(self.model)
        #    self.ui.treeView_3.setModel(self.model)
    #/////////////////////////////////////////////
    #                                          ///
    # END WEBCRAWLING          https://e00-marca.uecdn.es/assets/v33/js/desktop-70a5a07e9a07e88413f717089a674ce5e937a110.min.js                ///
    #                                          ///
    #/////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START CAMBIAR VENTANAS MENU              ///
    #                                          ///
    #/////////////////////////////////////////////
    def paginaHome(self):# FUNCION PARA CAMBIAR DE VENTANA AL PULSAR EL BOTON.
        self.ui.stackedWidget.setCurrentIndex(0)
        print("Widget actual:", self.ui.stackedWidget.currentIndex())

    def paginaEscanerPuerto(self):# FUNCION PARA CAMBIAR DE VENTANA AL PULSAR EL BOTON.
        self.ui.stackedWidget.setCurrentIndex(1)
        print("Widget actual:", self.ui.stackedWidget.currentIndex())

    def paginaEscanerDominio(self):# FUNCION PARA CAMBIAR DE VENTANA AL PULSAR EL BOTON.
        self.ui.stackedWidget.setCurrentIndex(3)
        print("Widget actual:", self.ui.stackedWidget.currentIndex())

    def paginaEscanerDirectorios(self):# FUNCION PARA CAMBIAR DE VENTANA AL PULSAR EL BOTON.
        self.ui.stackedWidget.setCurrentIndex(4)
        print("Widget actual:", self.ui.stackedWidget.currentIndex())

    def paginaWebcrawling(self):# FUNCION PARA CAMBIAR DE VENTANA AL PULSAR EL BOTON.
        self.ui.stackedWidget.setCurrentIndex(5)
        print("Widget actual:", self.ui.stackedWidget.currentIndex())

    def paginaResultados(self):# FUNCION PARA CAMBIAR DE VENTANA AL PULSAR EL BOTON.
        self.ui.stackedWidget.setCurrentIndex(2)
        print("Widget actual:", self.ui.stackedWidget.currentIndex())
    #/////////////////////////////////////////////
    #                                          ///
    # END CAMBIAR VENTANAS MENU                ///
    #                                          ///
    #/////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START MOSTRAR / ESCONDER MENU            ///
    #                                          ///
    #/////////////////////////////////////////////
    def menu(self):# FUNCIÓN DESPLEGAR MENU DE LA IZQUIERDA AL PULSAR EL BOTON DE LA HAMBURGUESA LAS TRES BARRAS
        if self.menu_num == 0:
            self.ui.animation = QtCore.QPropertyAnimation(self.ui.frame_left_menu, b'maximumWidth')
            self.ui.animation.setDuration(300)
            self.ui.animation.setStartValue(70)
            self.ui.animation.setEndValue(200)
            self.ui.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.ui.animation.start()

            self.ui.animation1 = QtCore.QPropertyAnimation(self.ui.frame_left_menu, b'minimumWidth')
            self.ui.animation1.setDuration(300)
            self.ui.animation1.setStartValue(70)
            self.ui.animation1.setEndValue(200)
            self.ui.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.ui.animation1.start()
            self.menu_num = 1
        else:
            self.ui.animation = QtCore.QPropertyAnimation(self.ui.frame_left_menu, b'maximumWidth')
            self.ui.animation.setDuration(300)
            self.ui.animation.setStartValue(200)
            self.ui.animation.setEndValue(70)
            self.ui.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.ui.animation.start()

            self.ui.animation1 = QtCore.QPropertyAnimation(self.ui.frame_left_menu, b'minimumWidth')
            self.ui.animation1.setDuration(300)
            self.ui.animation1.setStartValue(200)
            self.ui.animation1.setEndValue(70)
            self.ui.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.ui.animation1.start()
            self.menu_num = 0
    #/////////////////////////////////////////////
    #                                          ///
    # END MOSTRAR / ESCONDER MENU              ///
    #                                          ///
    #/////////////////////////////////////////////


    #/////////////////////////////////////////////
    #                                          ///
    # START TABS ultimas CONSULTAS             ///
    #                                          ///
    #/////////////////////////////////////////////

    def actualizar_tabla_desde_radio_button(self):
        # Verificar cuál de los QRadioButton está seleccionado
        if self.ui.radioButton_ip.isChecked():
            valor_seleccionado = "DireccionIP"
        elif self.ui.radioButton_dominios.isChecked():
            valor_seleccionado = "Dominio"
        elif self.ui.radioButton_url.isChecked():
            valor_seleccionado = "RutaEscaneo"
        elif self.ui.radioButton_rutas.isChecked():
            valor_seleccionado = "URL"
        elif self.ui.radioButton_todo.isChecked():
            valor_seleccionado = "TODO"
        
        # Consultar los datos usando el valor seleccionado
        conexion = conectar_db()
        inputUE = self.ui.lineEdit_4.text()
        if inputUE:
            if valor_seleccionado == "TODO":
                resultados = consultar_ultimas_ejecuciones_valor(conexion,inputUE)
            else:
                resultados = consultar_ultimas_ejecuciones_where_tipo_valor(conexion, valor_seleccionado,inputUE)
        else:
            if valor_seleccionado == "TODO":
                resultados = consultar_ultimas_ejecuciones(conexion)
            else:
                resultados = consultar_ultimas_ejecuciones_where_tipo(conexion, valor_seleccionado)
        cerrar_db(conexion)
        
        # Llenar el QTableWidget con los resultados
        if resultados:
            self.llenar_tabla_con_resultados(resultados)
        else:
            # Si no hay resultados, limpiar la tabla
            self.limpiar_tabla()
    
    def llenar_tabla_con_resultados(self, resultados):
        # Limpiar la tabla antes de llenarla
        self.ui.tableWidget_UltimoResultado.clearContents()
        self.ui.tableWidget_UltimoResultado.setRowCount(len(resultados))
        
        # Llenar la tabla con los resultados
        for row, data in enumerate(resultados):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget_UltimoResultado.setItem(row, col, item)
    
    def limpiar_tabla(self):
        # Limpiar la tabla
        self.ui.tableWidget_UltimoResultado.clearContents()
        self.ui.tableWidget_UltimoResultado.setRowCount(0)
    #/////////////////////////////////////////////
    #                                          ///
    # END TABS ultimas CONSULTAS               ///
    #                                          ///
    #/////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START TABS  CONSULTAS  ip                ///
    #                                          ///
    #/////////////////////////////////////////////

    def actualizar_tabla_ip(self):
        # Verificar cuál de los QRadioButton está seleccionado
        # Consultar los datos usando el valor seleccionado
        conexion = conectar_db()
        inputUE = self.ui.lineEdit_2.text()
        if inputUE:
            resultados = consultar_informacion_direcciones_ip_valor(conexion,inputUE)
        else:
            resultados = consultar_informacion_direcciones_ip(conexion)
        cerrar_db(conexion)
        
        # Llenar el QTableWidget con los resultados
        if resultados:
            self.llenar_tabla_con_resultados_ip(resultados)
        else:
            # Si no hay resultados, limpiar la tabla
            self.limpiar_tabla_ip()
    
    def llenar_tabla_con_resultados_ip(self, resultados):
        # Limpiar la tabla antes de llenarla
        self.ui.tableWidget_ip.clearContents()
        self.ui.tableWidget_ip.setRowCount(len(resultados))
        
        # Llenar la tabla con los resultados
        for row, data in enumerate(resultados):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget_ip.setItem(row, col, item)
    
    def limpiar_tabla_ip(self):
        # Limpiar la tabla
        self.ui.tableWidget_ip.clearContents()
        self.ui.tableWidget_ip.setRowCount(0)
    #/////////////////////////////////////////////
    #                                          ///
    # END TABS ultimas CONSULTAS ip            ///
    #                                          ///
    #/////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START TABS  CONSULTAS  dominios          ///
    #                                          ///
    #/////////////////////////////////////////////

    def actualizar_tabla_dominios(self):

        # Consultar los datos usando el valor seleccionado
        conexion = conectar_db()
        inputUE = self.ui.lineEdit_6.text()
        if inputUE:
            resultados = consultar_informacion_dominios_valor(conexion,inputUE)
        else:
            resultados = consultar_informacion_dominios(conexion)
        cerrar_db(conexion)
        
        # Llenar el QTableWidget con los resultados
        if resultados:
            self.llenar_tabla_con_resultados_dominios(resultados)
        else:
            # Si no hay resultados, limpiar la tabla
            self.limpiar_tabla_dominios()
    
    def llenar_tabla_con_resultados_dominios(self, resultados):
        # Limpiar la tabla antes de llenarla
        self.ui.tableWidget_dominios.clearContents()
        self.ui.tableWidget_dominios.setRowCount(len(resultados))
        
        # Llenar la tabla con los resultados
        for row, data in enumerate(resultados):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget_dominios.setItem(row, col, item)
    
    def limpiar_tabla_dominios(self):
        # Limpiar la tabla
        self.ui.tableWidget_dominios.clearContents()
        self.ui.tableWidget_dominios.setRowCount(0)
    #/////////////////////////////////////////////
    #                                          ///
    # END TABS ultimas CONSULTAS dominios      ///
    #                                          ///
    #/////////////////////////////////////////////


    #/////////////////////////////////////////////
    #                                          ///
    # START TABS  CONSULTAS   escaner directorios ///
    #                                          ///
    #/////////////////////////////////////////////

    def actualizar_tabla_escanerDirectorios(self):
        conexion = conectar_db()
        inputUE = self.ui.lineEdit_11.text()
        if inputUE:
            resultados = consultar_informacion_escaneo_directorios_valor(conexion,inputUE)
        else:
            resultados = consultar_informacion_escaneo_directorios(conexion)
        cerrar_db(conexion)
        
        # Llenar el QTableWidget con los resultados
        if resultados:
            self.llenar_tabla_con_resultados_escanerDirectorios(resultados)
        else:
            # Si no hay resultados, limpiar la tabla
            self.limpiar_tabla_escanerDirectorios()
    
    def llenar_tabla_con_resultados_escanerDirectorios(self, resultados):
        # Limpiar la tabla antes de llenarla
        self.ui.tableWidget_EscanerDirectorios.clearContents()
        self.ui.tableWidget_EscanerDirectorios.setRowCount(len(resultados))
        
        # Llenar la tabla con los resultados
        for row, data in enumerate(resultados):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget_EscanerDirectorios.setItem(row, col, item)
    
    def limpiar_tabla_escanerDirectorios(self):
        # Limpiar la tabla
        self.ui.tableWidget_EscanerDirectorios.clearContents()
        self.ui.tableWidget_EscanerDirectorios.setRowCount(0)
    #//////////////////////////////////////////////////
    #                                               ///
    # END TABS ultimas CONSULTAS escaner directorios///
    #                                               ///
    #//////////////////////////////////////////////////

    #/////////////////////////////////////////////
    #                                          ///
    # START TABS  CONSULTAS webcrawling        ///
    #                                          ///
    #/////////////////////////////////////////////

    def actualizar_tabla_webcrawling(self):
        conexion = conectar_db()
        inputUE = self.ui.lineEdit_12.text()
        if inputUE:
            resultados = consultar_informacion_web_crawling_valor(conexion,inputUE)
        else:
            resultados = consultar_informacion_web_crawling(conexion)
        cerrar_db(conexion)
        
        # Llenar el QTableWidget con los resultados
        if resultados:
            self.llenar_tabla_con_resultados_webcrawling(resultados)
        else:
            # Si no hay resultados, limpiar la tabla
            self.limpiar_tabla_webcrawling()
    
    def llenar_tabla_con_resultados_webcrawling(self, resultados):
        # Limpiar la tabla antes de llenarla
        self.ui.tableWidget_webcrawling.clearContents()
        self.ui.tableWidget_webcrawling.setRowCount(len(resultados))
        
        # Llenar la tabla con los resultados
        for row, data in enumerate(resultados):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget_webcrawling.setItem(row, col, item)
    
    def limpiar_tabla_webcrawling(self):
        # Limpiar la tabla
        self.ui.tableWidget_webcrawling.clearContents()
        self.ui.tableWidget_webcrawling.setRowCount(0)
    #//////////////////////////////////////////////////
    #                                               ///
    # END TABS ultimas CONSULTAS webcrawling        ///
    #                                               ///
    #//////////////////////////////////////////////////


#/////////////////////////////////////////////
#                                          ///
# END FUNCIONES AÑADIDAS                   ///
#                                          ///
#/////////////////////////////////////////////

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myMainWindow(app)
