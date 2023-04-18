.PHONY: run gui

run: main.py
	python3 main.py

gui : ./gui/gui.ui
	pyuic5 ./gui/gui.ui -o mainwindow.py
	mv mainwindow.py gui
