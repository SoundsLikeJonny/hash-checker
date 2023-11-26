import flet as ft
from pathlib import Path
import hashlib

from flet_core.file_picker import FilePickerFile


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.colors.LIGHT_BLUE)
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
    }

    downloads_path = Path.home() / 'Downloads'
    hash_text_field_hint: str = 'Paste the sha256 check sum hash from the website you downloaded the file'
    paste_text_field: ft.TextField = ft.TextField(
        hint_text=hash_text_field_hint,
        dense=True,
        on_change=lambda _: check_hash()
    )
    hash_text: ft.Text = ft.Text('', selectable=True)
    file_text: ft.Text = ft.Text('', selectable=True)
    hash_info: ft.Column = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text('File: '),
                    file_text
                ]
            ),
            ft.Row(
                controls=[
                    ft.Text('File Hash: '),
                    hash_text
                ]
            ),
        ]
    )

    result_icon: ft.Icon = ft.Icon()
    file_picker = ft.FilePicker(on_result=lambda e: set_hash(e))

    def set_hash(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        if not e.files[0]:
            return

        first_file: FilePickerFile = e.files[0]
        first_file_path: str = first_file.path
        first_file_name: str = first_file.name
        file_text.value = first_file_path
        sha256_hash = hashlib.sha256()

        with open(first_file_path, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(byte_block)

        if sha256_hash.hexdigest():
            hash_text.value = sha256_hash.hexdigest()
        check_hash()
        page.update()

    def check_hash():
        if hash_text.value == paste_text_field.value and hash_text.value != '':
            result_icon.name = ft.icons.CHECK
            result_icon.color = ft.colors.GREEN
            paste_text_field.error_text = None
            page.update()
            return
        if hash_text.value != paste_text_field.value:
            result_icon.name = ft.icons.ERROR
            result_icon.color = ft.colors.RED
            paste_text_field.error_text = 'Does not match'
            page.update()
            return
        result_icon.name = None
        result_icon.color = None
        paste_text_field.error_text = None
        page.update()

    def select_file():
        file_picker.pick_files(
            'Select a file to check',
            file_type=ft.FilePickerFileType.ANY,
            allow_multiple=False,
            initial_directory=str(downloads_path),
        )

    column_parent: ft.Column = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text('Hash Checker', style=ft.TextThemeStyle.TITLE_MEDIUM),
            ft.Row(
                controls=[
                    ft.IconButton(
                        ft.icons.FILE_OPEN,
                        tooltip='Select a downloaded file for checking',
                        on_click=lambda _: select_file(),
                    ),
                    file_picker,
                    hash_info,
                ],
            ),
            ft.Divider(opacity=0, height=5),
            paste_text_field,
            result_icon
        ]
    )

    page.add(
        ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                column_parent
            ]
        ),
    )
    page.update()
