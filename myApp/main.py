import flet as ft
import http.client
import json

host = "flaskApi:5000" # direccion del servidor 

def getResponse(conn: http.client.HTTPConnection):
    jsonData = {"error": "Failed to get data from API"}
    response = conn.getresponse()
    if response.status == 200:
        data = response.read().decode()
        jsonData = json.loads(data)
    else:
        print(response.read().decode())
        print("Failed to get data from API")
    return jsonData

def listSighting():
    conn = http.client.HTTPConnection(host)
    conn.request("GET", "/home-view/sightings")
    return getResponse(conn)

def listAlert():
    conn = http.client.HTTPConnection(host)
    conn.request("GET", "/home-view/alerts")
    return getResponse(conn)

def listIncident(idIndividual):

    dataIncident = {
        "idIndividual": idIndividual
    }
    
    json_data = json.dumps(dataIncident)
    conn = http.client.HTTPConnection(host)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("GET", "/home-view/incidents", body=json_data, headers=headers)
    return getResponse(conn)

def createIncident(e, id, idAlert, idSighting, text, page):
    description = text.value

    dataIncident = {
        "idSighting": idSighting,
        "idAlert":  idAlert,
        "idUser": 1,
        "description": description
    }

    json_data = json.dumps(dataIncident)
    conn = http.client.HTTPConnection(host)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/home-view/incident", body=json_data, headers=headers)
    text_field.value = ""
    text_field_incidene.value = ""
    page.go("/")
    return getResponse(conn)

text_field = ft.TextField(multiline=True, width=300, height=100)
text_field_incidene = ft.TextField(multiline=True, width=300, height=100)

def main(page: ft.Page):
    print("Start front on http://127.0.0.1:8551")
    page.title = "Routes Example"

    def route_change(route):

        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()
        
        def go_to_home():
            page.go(f"/")
    
        def go_to_store(e, id, hora, imagenURL, idSighting):
            page.go(f"/store?id {id}&hora {hora}&imagenURL {imagenURL}&idSighting {idSighting}")
            
        def go_to_incidence(e, id, hora, idAlert, imagenURL):
            page.go(f"/incidence?id {id}&hora {hora}&idAlert {idAlert}&imagenURL {imagenURL}")

        def go_to_notifications(e):
            page.go(f"/notifications")
            
        def create_row(hora, robo, trabajador):
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(f"Date: {hora}", size=16, color="#000000"),
                        padding=10,
                        bgcolor=ft.colors.GREY_200,
                        border_radius=ft.border_radius.all(5),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Text(f"Stole: ${robo}", size=16, color="#000000"),
                        padding=10,
                        bgcolor=ft.colors.GREY_200,
                        border_radius=ft.border_radius.all(5),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Text(f"Id user: {trabajador}", size=16, color="#000000"),
                        padding=10,
                        bgcolor=ft.colors.GREY_200,
                        border_radius=ft.border_radius.all(5),
                        expand=True
                    )
                ]
            )

        page.views.clear()
        def create_list_home():
            individuals = listSighting()
            list_view_content = []
            for sujeto in individuals:
                image = sujeto['mugshot']
                idIndividual = sujeto['individual_id']
                idSighting = sujeto['id']

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
                                            ft.Text(f"ID: {idSighting}", color="#000000"),
                                            ft.Text(f"Date: {sujeto['creation_time']}", color="#000000")
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                        tight=False
                                    ),
                                    bgcolor=ft.colors.GREY_300,
                                    width=100,
                                    height=50
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.IconButton(
                                                ft.icons.ADD_BOX, 
                                                icon_color=ft.colors.GREEN_200,
                                                on_click=lambda e, id=idIndividual, hora=sujeto['creation_time'], imagenURL=image, idSighting=idSighting: go_to_store(e, id, hora, imagenURL, idSighting)
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
            return list_view_content

        notifications = listAlert()
        list_view_notifications = []
        for notification in notifications:
            sighting = notification["sighting"]
            image = sighting["individual"]["mugshot"]
            id = sighting["individual"]["id"] 
            creation_time = sighting["individual"]["creation_time"]
            idAlert = notification["id"]
            objectCordinates = sighting["object_coordinates"]
            typeAlert = "without dangerous object"
            
            if(len(objectCordinates) > 0):
                typeAlert = "dangerous object"
            

            list_view_notifications.append(
                ft.TextButton(
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
                                width=80,
                                height=80,
                                margin=10
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(f"{typeAlert}", size=10, color="#C70039"),
                                        ft.Text(f"The individual with id {id} has committed a repeat offense", color="#000000"),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                    tight=False
                                ),
                                bgcolor=ft.colors.GREY_300,
                                width=150,
                                height=70
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    on_click=lambda e, id=id, hora=creation_time, idAlert=idAlert, imagenURL=image: go_to_incidence(e, id, hora, idAlert, imagenURL),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                        bgcolor=ft.colors.GREY_300
                    ),
                )
            )
        
        ########################Home page###############################
        page.views.append(
            ft.View(
                "/",
                [   
                    ft.AppBar(
                        leading=ft.Icon(ft.icons.PANORAMA_FISH_EYE_ROUNDED),
                        leading_width=40,
                        title=ft.Text("EyeonU", size=30, color=ft.colors.WHITE, italic=True),
                        center_title=True,
                        bgcolor=ft.colors.GREEN_200,
                        actions=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            content=ft.Badge(content=ft.Icon(ft.icons.NOTIFICATIONS, color=ft.colors.WHITE), 
                                            text=str(len(listAlert()))),
                                            icon_size=30,
                                            tooltip="Alert",
                                            selected_icon_color=ft.colors.BLACK,
                                            on_click=lambda e: go_to_notifications(e)
                                        ),
                                    ]   
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(right=10)
                            )
                        ]
                    ), 
                    ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False, controls=create_list_home())
                ],
                bgcolor=ft.colors.WHITE  # Establecer el fondo blanco aquí
            )
        ) 

        ########################Notifications page###############################
        if page.route.startswith("/notifications"):
            page.views.append(
                ft.View(
                     "/notifications",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(
                                            ft.icons.ARROW_BACK , 
                                            on_click=lambda _: go_to_home()
                                        ),
                            leading_width=40,
                            title=ft.Text("Notifications", size=20, color=ft.colors.WHITE, italic=True),
                            center_title=False,
                            bgcolor=ft.colors.GREEN_200,
                        ), 
                        ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False, controls=list_view_notifications)
                    ],
                    bgcolor=ft.colors.WHITE  # Establecer el fondo blanco aquí
                )
            )

        ########################Incident page###############################
        if page.route.startswith("/store"):
            # Obtener parámetros de la URL
            params = {param.split(" ")[0]: param.split(" ")[1] for param in page.route.split("?")[1].split("&")}
            id = params.get("id", "N/A")
            hora = params.get("hora", "N/A")
            imagenURL = params.get("imagenURL", "")
            idSighting = params.get("idSighting", "N/A")

            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(
                                            ft.icons.ARROW_BACK , 
                                            on_click=lambda _: go_to_home()
                                        ),
                            leading_width=40,
                            title=ft.Text("Incident registry", size=20, color=ft.colors.WHITE, italic=True),
                            center_title=False,
                            bgcolor=ft.colors.GREEN_200,
                        ), 
                        ft.Container(
                            padding=20,
                            content=
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Image(
                                                src_base64=imagenURL,
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
                                                ft.Text(f"ID: {idSighting}", size=20, weight=ft.FontWeight.BOLD),
                                                ft.Text(f"Hour: {hora}", size=20, weight=ft.FontWeight.BOLD)
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
                                    text_field,
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("Save", on_click=lambda e, id=id, idAlert=None, idSighting=idSighting, text=text_field, page=page: createIncident(e, id, idAlert, idSighting, text, page), bgcolor=ft.colors.GREEN_200, color=ft.colors.WHITE)
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
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

        ########################Reincidence page###############################
        if page.route.startswith("/incidence"):
            # Obtener parámetros de la URL
            params = {param.split(" ")[0]: param.split(" ")[1] for param in page.route.split("?")[1].split("&")}
            idIncidence = params.get("id", "N/A")
            hourIncidence = params.get("hora", "N/A")
            idAlert = params.get("idAlert", "N/A")
            imageIncidence = params.get("imagenURL", "")
            sujetoReincidencia = listIncident(idIncidence)

            
            page.views.append(
                ft.View(
                    "/incidence",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(
                                ft.icons.ARROW_BACK,
                                on_click=lambda _: page.go("/notifications")
                            ),
                            leading_width=40,
                            title=ft.Text("Incident history", size=20, color=ft.colors.WHITE, italic=True),
                            center_title=False,
                            bgcolor=ft.colors.GREEN_200,
                        ),
                        ft.ListView(
                            expand=1, 
                            spacing=10, 
                            padding=20,
                            auto_scroll=False,
                            controls=[
                                ft.Container(
                                    padding=20,
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Image(
                                                    src_base64=imageIncidence,
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
                                                        ft.Text(f"ID: {idIncidence}", size=20, weight=ft.FontWeight.BOLD),
                                                        ft.Text(f"Hour: {hourIncidence}", size=20, weight=ft.FontWeight.BOLD)
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.START
                                                )
                                            )
                                        ],
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                ),
                                ft.Text("Last incidents", size=20, weight=ft.FontWeight.BOLD, color="#7F858C"),
                                ft.Column(
                                    controls=[
                                        create_row(entry["creation_time"], entry["description"], entry["user_id"]) for entry in sujetoReincidencia
                                    ],
                                    spacing=10
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("Incident description:", size=20, weight=ft.FontWeight.BOLD),
                                            text_field_incidene,
                                            ft.Row(
                                                controls=[
                                                    ft.ElevatedButton("Save", on_click=lambda e, id=id, idAlert=idAlert, idSighting=None, text=text_field_incidene, page=page: createIncident(e, id, idAlert, idSighting, text, page), bgcolor=ft.colors.GREEN_200, color=ft.colors.WHITE)
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
                        )
                    ],
                    bgcolor=ft.colors.WHITE,  # Establecer el fondo blanco aquí
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

# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main, port=8551, host="0.0.0.0")