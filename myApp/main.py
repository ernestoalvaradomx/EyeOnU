import flet as ft
import http.client
import json
import socketio

sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')

conn = http.client.HTTPConnection("127.0.0.1:5000")

def main(page: ft.Page):
    page.title = "Routes Example"

    icon = ft.Badge(content=ft.Icon(ft.icons.NOTIFICATIONS, color=ft.colors.WHITE), 
                    text="0")
    
    def listAlert():
        conn.request("GET", "/home-view/alerts/")
        response = conn.getresponse()

        if response.status == 200:
            data = response.read().decode()
            alerts = json.loads(data)
            # for individual in individuals:
            #     print(individual)
        else:
            print(response.read().decode())
            print("Failed to get data from API")
        return alerts

    @sio.event
    def connect():
        print('Conectado al servidor de notificaciones')

    @sio.event
    def disconnect():
        print('Desconectado del servidor de notificaciones')

    def closeDialog(page, notification):
        notification.open = False
        page.update()

    @sio.event
    def notification(data):
        print('\nNotificacion recibida')
        # Mostrar notificación en Flet
        # notification = ft.AlertDialog(
        #     title=ft.Text('Nueva notificación'),
        #     content=ft.Text(f"Detalles: {data['alert']}"),
        #     actions=[ft.TextButton("OK", on_click=lambda _: closeDialog(page, notification))],
        # )
        # page.overlay.append(notification)
        # notification.open = True
        # page.update()

        alerts = listAlert()
        icon.text = str(len(alerts))
        icon.update()    

    sujetosIdentificados = [
        {
            "id": 1,
            "hora": '09:39',
            "imagenURL": "https://s.yimg.com/ny/api/res/1.2/TZlm9wfiZSJ6hAud6pMKJg--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTQyNw--/https://media.zenfs.com/en/homerun/feed_manager_auto_publish_494/8570a2318fa156e2de6a1d4ca0610d0a"
        },
        {
            "id": 2,
            "hora": '09:54',
            "imagenURL": "https://holatelcel.com/wp-content/uploads/2018/11/HEAD-face-recognition.jpg"
        },
        {
            "id": 3,
            "hora": '10:19',
            "imagenURL": "https://media.istockphoto.com/id/155068180/es/foto/guy-real.jpg?s=612x612&w=0&k=20&c=VDSua2eTduOoccz7LZZWxNhGMur6hl6jZKIqAiY3w68="
        },
        {
            "id": 4,
            "hora": '10:39',
            "imagenURL": "https://img.freepik.com/foto-gratis/concepto-emociones-personas-foto-cabeza-hombre-guapo-aspecto-serio-barba-confiado-decidido_1258-26730.jpg"
        },
        {
            "id": 5,
            "hora": '11:23',
            "imagenURL": "https://media.istockphoto.com/id/1081389092/es/foto/hombre-cauc%C3%A1sico-real-con-expresi%C3%B3n-en-blanco.jpg?s=612x612&w=0&k=20&c=JKHYu94Mip2Kxloq-fiPGck7CnlUX9UFftsBwhon-0M="
        },
        {
            "id": 6,
            "hora": '11:59',
            "imagenURL": "https://media.istockphoto.com/id/507995592/es/foto/hombre-pensativo-observando-a-la-c%C3%A1mara.jpg?s=612x612&w=0&k=20&c=9roAIpAFmS2yIwR0T96RdfX0C7Dch2CU0HCb4VTD5R4="
        },
    ]

    def route_change(route):

        # conn = http.client.HTTPConnection("127.0.0.1:5000")
        conn.request("GET", "/home-view/individuals/")
        response = conn.getresponse()

        if response.status == 200:
            data = response.read().decode()
            individuals = json.loads(data)
            # for individual in individuals:
            #     print(individual)
        else:
            print(response.read().decode())
            print("Failed to get data from API")

        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()

        def go_to_store(e, id, hora, imagenURL):
            page.go(f"/store?id {id}&hora {hora}&imagenURL {imagenURL}")

        page.views.clear()
        list_view_content = []
        for sujeto in individuals:
            image = sujeto['mugshot']
            # print("image: ", image)

            list_view_content.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src_base64=image,
                                    width=100,
                                    height=90,
                                    fit=ft.ImageFit.COVER,
                                ),
                                bgcolor=ft.colors.GREY_300,
                                width=100,
                                height=90,
                                margin=10
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(f"ID: {sujeto['id']}", size=20, color="#000000", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Date: {sujeto['creation_time']}", size=20, color="#000000", weight=ft.FontWeight.BOLD)
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                    tight=False
                                ),
                                bgcolor=ft.colors.GREY_300,
                                width=120,
                                height=50
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.IconButton(
                                            ft.icons.ADD_BOX, 
                                            icon_color=ft.colors.GREEN_200,
                                            on_click=lambda e, id=sujeto['id'], hora=sujeto['creation_time'], imagenURL=image: go_to_store(e, id, hora, imagenURL)
                                        ),
                                    ]
                                ),
                                bgcolor=ft.colors.GREY_300,
                                width=100,
                                height=50
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    width=300,  # Ajusta el ancho según sea necesario
                    height=100,  # Ajusta la altura según sea necesario
                    bgcolor=ft.colors.GREY_300,
                    border_radius=ft.border_radius.all(5),
                )
            )

        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        leading=ft.Icon(ft.icons.PANORAMA_FISH_EYE_ROUNDED),
                        leading_width=40,
                        title=ft.Text("EyeOnU", size=30, color=ft.colors.WHITE, italic=True),
                        center_title=True,
                        bgcolor=ft.colors.GREEN_200,
                        actions=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            content=icon,
                                            icon_size=30,
                                            tooltip="Alert",
                                            selected_icon_color=ft.colors.BLACK,
                                            # padding=ft.padding.only(right=30),
                                        ),
                                    ]
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(right=10)
                            )
                        ]
                    ), 
                    ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False, controls=list_view_content),
                ],
                bgcolor=ft.colors.WHITE  # Establecer el fondo blanco aquí
            )
        )

        if page.route.startswith("/store"):
            # Obtener parámetros de la URL
            params = {param.split(" ")[0]: param.split(" ")[1] for param in page.route.split("?")[1].split("&")}
            id = params.get("id", "N/A")
            hora = params.get("hora", "N/A")
            image = params.get("imagenURL", "")
            incident_description = "Stole $20"

            # print("imagenURL: ", image)

            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(
                                            ft.icons.ARROW_BACK , 
                                            on_click=lambda _: page.go("/")
                                        ),
                            leading_width=40,
                            title=ft.Text("EyeonU", size=30, color=ft.colors.WHITE, italic=True),
                            center_title=True,
                            bgcolor=ft.colors.GREEN_200,
                        ), 
                        # ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        # ft.Text(f"ID: {id}"),
                        # ft.Text(f"Hora: {hora}"),
                        # ft.Image(src=imagenURL, width=200, height=180, fit=ft.ImageFit.COVER)
                        ft.Container(
                            padding=20,
                            content=
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Image(
                                                src_base64=image,
                                                width=100,
                                                height=100,
                                                fit=ft.ImageFit.COVER
                                            ),
                                            bgcolor=ft.colors.GREY_300,
                                            width=100,
                                            height=100,
                                            margin=10
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                            controls=[
                                                ft.Text(f"ID: {id}", size=20, color="#000000", weight=ft.FontWeight.BOLD),
                                                ft.Text(f"Date: {hora}", size=20, color="#000000", weight=ft.FontWeight.BOLD)
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.START
                                            )
                                        )
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Incident description:", size=20, weight=ft.FontWeight.BOLD),
                                    ft.TextField( multiline=True, width=300, height=100),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Save", on_click=lambda _: print("Save clicked"), bgcolor=ft.colors.GREEN_200, color=ft.colors.WHITE),
                                            ft.ElevatedButton("Back", on_click=lambda _: page.go("/"), bgcolor=ft.colors.GREEN_200, color=ft.colors.WHITE)
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        )
                    ],
                    bgcolor=ft.colors.WHITE  # Establecer el fondo blanco aquí
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
