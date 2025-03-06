import flet as ft
import json
import os

# Variáveis globais
aba = "Fechado"
save_file = "notas.json"

# Função para salvar as notas no arquivo JSON
def save_to_json(notes):
    with open(save_file, "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

# Função para carregar as notas do arquivo JSON
def load_from_json():
    if os.path.exists(save_file):
        with open(save_file, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                # Garantir que todos os itens são dicionários válidos
                return [
                    note if isinstance(note, dict) else {"title": "", "text": note}
                    for note in data
                ]
            except json.JSONDecodeError:
                return []
    return []

def main(page: ft.Page):
    notes = load_from_json()  # Carregar todas as notas
    current_note_index = 0    # Índice da nota atual

    page.title = "NotePad"
    page.window.width = 500
    page.window.height = 600
    page.window.resizable = False
    page.window.maximizable = True
    page.scroll = True
    page.bgcolor = "#141414"
    page.window.center()

    def Save_note(e):
        nonlocal current_note_index
        if current_note_index < len(notes):
            notes[current_note_index]["title"] = note_title.value
            notes[current_note_index]["text"] = note_text.value
        else:
            notes.append({
                "title": note_title.value,
                "text": note_text.value,
            })
        save_to_json(notes)  # Salvar todas as notas no JSON
        page.snack_bar = ft.SnackBar(ft.Text("Nota salva com sucesso!", color=ft.colors.BLACK), bgcolor=ft.colors.ORANGE_ACCENT)
        page.snack_bar.open = True 
        update_saved_buttons()  
        page.update()

    def open_save(index):
        def handler(e):
            nonlocal current_note_index
            current_note_index = index
            note_title.value = notes[index]["title"]
            note_text.value = notes[index]["text"]
            fecha_aba(e)
            page.update()
        return handler

    def nova_nota(e):
        nonlocal current_note_index
        current_note_index = len(notes)  # Nova nota será no próximo índice
        note_title.value = ""
        note_text.value = ""
        notes.append({"title": "", "text": ""})
        update_saved_buttons()
        page.update()
    
    def abas(e):
        global aba
        if aba == "Fechado":
            abrir_abas(e)
        else:
            fecha_aba(e)
    
    def fecha_aba(e):
        global aba
        aba = "Fechado"
        aba_lateral.visible = False
        page.scroll = True
        page.update()
    
    def abrir_abas(e):
        global aba
        aba = "Aberto"
        aba_lateral.visible = True
        page.scroll = False
        page.update()
    
    def update_saved_buttons():
        saved_buttons.controls.clear()
        for i, note in enumerate(notes):
            button = ft.ElevatedButton(
                text=note["title"] if note["title"] else f"Nota {i + 1}",
                style=ft.ButtonStyle(color=ft.Colors.ORANGE_ACCENT),
                on_click=open_save(i),
                width=300,
                height=50,
            )
            saved_buttons.controls.append(
                ft.Container(
                    content=button,
                    border=ft.border.all(1, color=ft.Colors.ORANGE_ACCENT),
                    border_radius=10,
                    padding=10,
                    margin=10,
                )
            )
        page.update()

    saved_buttons = ft.Column()

    Lateral_Content = ft.Column([
        ft.Container(
            content=ft.ElevatedButton(
                text="Nova Nota",
                style=ft.ButtonStyle(color=ft.Colors.ORANGE_ACCENT),
                on_click=nova_nota,
                width=300,
                height=50,
            ),
            border=ft.border.all(1, color=ft.Colors.ORANGE_ACCENT),
            border_radius=10,
            padding=10,
            margin=10,
        ),
        saved_buttons
    ])

    aba_lateral = ft.Container(
        content=Lateral_Content,
        width=200,
        bgcolor="#141414",
        border=ft.border.all(1, color=ft.Colors.ORANGE_ACCENT),
        border_radius=10,
        visible=False,
        height=500,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("NotePad", color=ft.Colors.ORANGE_ACCENT),
        leading=ft.IconButton(
            ft.Icons.MENU,
            icon_color=ft.Colors.ORANGE_ACCENT,
            icon_size=20,
            on_click=abas
        ),
        center_title=True,
        bgcolor=ft.Colors.GREY_900
    )

    note_title = ft.TextField(
        label="Título Da Nota",
        width=250,
        focused_border_color=ft.Colors.ORANGE_ACCENT,
        border_color=ft.Colors.ORANGE_ACCENT,
        border_radius=10,
        label_style=ft.TextStyle(color=ft.Colors.ORANGE_ACCENT)
    )
    
    Save = ft.Container(
        content=ft.Icon(ft.Icons.SAVE, color=ft.Colors.ORANGE_ACCENT),
        on_click=Save_note,
        border=ft.border.all(1, color=ft.Colors.ORANGE_ACCENT),
        padding=10,
        border_radius=10,
        bgcolor=ft.Colors.BLACK12
    )
    
    divider1 = ft.Divider(thickness=2, color="#292929") 
    
    note_text = ft.TextField(
        label="Anotação",
        multiline=True,
        width=400,
        height=400,
        expand=True,
        border_radius=10,
        border_color=ft.Colors.ORANGE_ACCENT,
        focused_border_color=ft.Colors.ORANGE_ACCENT,
        label_style=ft.TextStyle(color=ft.Colors.ORANGE_ACCENT)
    )
    
    TextSave = ft.Row([note_title, Save], spacing=150)

    page.add(aba_lateral, TextSave, divider1, note_text)
    
    update_saved_buttons()
    page.update()

ft.app(target=main)
