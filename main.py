from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QTextEdit, QListWidget, QInputDialog
import sys
import json

def show_note():
    key = notes_list.selectedItems()[0].text()
    note_field.setText(notes[key]['text'])
    tags_list.clear()
    tags_list.addItems(notes[key]['tags'])

def load_notes():
    try:
        with open('notes.json', 'r') as file:
            notes = json.load(file)
        notes_list.addItems(notes)
        return notes
    except:
        notes = {
            'Приветственная заметка':{
                'text': 'Это первая заметка',
                'tags': ['начало', 'крут'] 
            }
        }
        with open('notes.json', 'w') as file:
            json.dump(notes, file)
        notes_list.addItems(notes)
        return notes

def del_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        del notes[key]
        notes_list.clear()
        tags_list.clear()
        note_field.clear()
        notes_list.addItems(notes)
        with open('notes.json','w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys= True)

def add_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = tag_field.text()
        if not tag in notes[key]['tags'] and len(tag)>0:
            notes[key]['tags'].append(tag)
            tags_list.addItem(tag)
            tag_field.clear()
            with open('notes.json','w', encoding='utf-8') as file:
                json.dump(notes, file, sort_keys= True)

def remove_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = tags_list.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        tags_list.clear()
        tags_list.addItems(notes[key]['tags'])
        with open('notes.json','w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys= True)

def search_by_tag():
    tag = tag_field.text()
    if btn_search_tag.text() != 'сбросить поиск' and len(tag) > 0:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['tags']:
                notes_filtered[note] = notes[note]
        notes_list.clear()
        tags_list.clear()
        note_field.clear()
        notes_list.addItems(notes_filtered)
        btn_search_tag.setText('сбросить поиск')
    else:
        tag_field.clear()
        notes_list.clear()
        tags_list.clear()
        note_field.clear()
        notes_list.addItems(notes)
        btn_search_tag.setText('Искать по тегу')

def save_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        notes[key]['text'] = note_field.toPlainText()
        with open('notes.json','w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys= True)

def add_note():
    note_name, ok = QInputDialog.getText(window,'Добавить заметку', 'Название заметки:')
    if ok and len(note_name) > 0:
        notes[note_name] = {'text': '', 'tags': []}
        notes_list.addItem(note_name)
        tags_list.addItems(notes[note_name]['tags'])

notes = {"Приветствие": {
    'текст': 'Что хотите то и делайте',
    'теги': ['начало', 'приветствие']
}}

#with open('notes_data.json', 'w', encoding= 'utf-8') as file:
#    json.dump(notes, file)

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Smart-notes')
window.resize(900,600)

note_field = QTextEdit()
notes_list = QListWidget()
tags_list = QListWidget()

btn_create_note = QPushButton('Создать заметку')
btn_delete_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')

btn_add_tag = QPushButton('Добавить к заметке')
btn_remove_tag = QPushButton('Открепить от заметки')
btn_search_tag = QPushButton('Искать по тегу')

lbl_for_notes = QLabel('Список заметок')
lbl_for_tags = QLabel('Список тегов')
tag_field = QLineEdit()

main_line = QHBoxLayout()
left_side = QVBoxLayout()
right_side = QVBoxLayout()

h_1_line = QHBoxLayout()
h_2_line = QHBoxLayout()
h_3_line = QHBoxLayout()
h_4_line = QHBoxLayout()
h_5_line = QHBoxLayout()
h_6_line = QHBoxLayout()
h_7_line = QHBoxLayout()
h_8_line = QHBoxLayout()
h_9_line = QHBoxLayout()

h_1_line.addWidget(lbl_for_notes)
h_2_line.addWidget(notes_list)
h_3_line.addWidget(btn_create_note)
h_3_line.addWidget(btn_delete_note)
h_4_line.addWidget(btn_save_note)
h_5_line.addWidget(lbl_for_tags)
h_6_line.addWidget(tags_list)
h_7_line.addWidget(tag_field)
h_8_line.addWidget(btn_add_tag)
h_8_line.addWidget(btn_remove_tag)
h_9_line.addWidget(btn_search_tag)

right_side.addLayout(h_1_line)
right_side.addLayout(h_2_line)
right_side.addLayout(h_3_line)
right_side.addLayout(h_4_line)
right_side.addLayout(h_5_line)
right_side.addLayout(h_6_line)
right_side.addLayout(h_7_line)
right_side.addLayout(h_8_line)
right_side.addLayout(h_9_line)

left_side.addWidget(note_field)

main_line.addLayout(left_side)
main_line.addLayout(right_side)

window.setLayout(main_line)
tag_field.setPlaceholderText('Введите тег...')


notes_list.itemClicked.connect(show_note)
btn_save_note.clicked.connect(save_note)
btn_create_note.clicked.connect(add_note)
btn_delete_note.clicked.connect(del_note)
btn_add_tag.clicked.connect(add_tag)
btn_remove_tag.clicked.connect(remove_tag)
btn_search_tag.clicked.connect(search_by_tag)

notes = load_notes()
window.show()
app.exec()