import flet as ft

# ── Warna & konstanta ────────────────────────────────────────────────────────
TEAL        = "#1D9E75"
TEAL_LIGHT  = "#9FE1CB"
AMBER       = "#EF9F27"
AMBER_LIGHT = "#FAEEDA"
GRAY_BG     = "#F8F9FA"
BORDER      = "#E5E7EB"
TEXT_MUTED  = "#6B7280"
TEXT_MAIN   = "#111827"
WHITE       = "#FFFFFF"

SENSOR_FIELDS = [
    ("PT08.S1 (CO)",   500, 2500, 1360),
    ("PT08.S2 (NMHC)", 500, 2500, 1046),
    ("PT08.S3 (NOx)",  500, 2500, 1056),
    ("PT08.S4 (NO2)",  500, 2500, 1692),
    ("PT08.S5 (O3)",   500, 2500, 1268),
]

MONTHS = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]

def make_border():
    side = ft.BorderSide(width=0.5, color=BORDER)
    return ft.Border(top=side, right=side, bottom=side, left=side)

def card(content, padding=16):
    return ft.Container(
        content=content,
        bgcolor=WHITE,
        border=make_border(),
        border_radius=12,
        padding=padding,
    )

def divider():
    return ft.Divider(height=1, color=BORDER, thickness=0.5)

def section_label(text, icon):
    return ft.Row(
        controls=[
            ft.Icon(icon, size=14, color=TEXT_MUTED),
            ft.Text(text, size=11, weight=ft.FontWeight.W_500, color=TEXT_MUTED),
        ],
        spacing=4,
    )

def sensor_slider_row(label, min_val, max_val, value):
    return ft.Column(
        controls=[
            ft.Text(label, size=12, color=TEXT_MUTED),
            ft.Row(
                controls=[
                    ft.Slider(
                        min=min_val, max=max_val, value=value,
                        divisions=int(max_val - min_val),
                        active_color=TEAL, thumb_color=TEAL,
                        expand=True,
                    ),
                    ft.Text(
                        str(int(value)), size=12,
                        weight=ft.FontWeight.W_500, color=TEXT_MAIN,
                        width=40, text_align=ft.TextAlign.RIGHT,
                    ),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        spacing=2,
    )

def atm_slider_row(label, unit, min_val, max_val, value, decimals=0):
    fmt = f"{value:.{decimals}f}"
    return ft.Column(
        controls=[
            ft.Text(label, size=12, color=TEXT_MUTED),
            ft.Row(
                controls=[
                    ft.Slider(
                        min=min_val, max=max_val, value=value,
                        divisions=int((max_val - min_val) * (10 ** decimals)),
                        active_color=TEAL, thumb_color=TEAL,
                        expand=True,
                    ),
                    ft.Text(
                        f"{fmt} {unit}", size=12,
                        weight=ft.FontWeight.W_500, color=TEXT_MAIN,
                        width=65, text_align=ft.TextAlign.RIGHT,
                    ),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        spacing=2,
    )

def metric_card(label, value):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(label, size=11, color=TEXT_MUTED),
                ft.Text(value, size=20, weight=ft.FontWeight.W_500, color=TEXT_MAIN),
            ],
            spacing=4,
        ),
        bgcolor=GRAY_BG,
        border_radius=8,
        padding=ft.Padding(left=12, right=12, top=10, bottom=10),
        expand=True,
    )

def status_badge(label, bg, fg):
    return ft.Container(
        content=ft.Text(label, size=12, weight=ft.FontWeight.W_500, color=fg),
        bgcolor=bg,
        border_radius=8,
        padding=ft.Padding(left=14, right=14, top=5, bottom=5),
    )

def gauge_arc():
    dummy_ratio = 8.3 / 20.0
    return ft.Stack(
        controls=[
            ft.Container(
                content=ft.ProgressRing(
                    value=1.0, width=140, height=140,
                    stroke_width=14, color=BORDER,
                ),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(
                content=ft.ProgressRing(
                    value=dummy_ratio, width=140, height=140,
                    stroke_width=14, color=AMBER,
                ),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("8.3", size=28, weight=ft.FontWeight.W_500,
                                color=TEXT_MAIN, text_align=ft.TextAlign.CENTER),
                        ft.Text("µg/m³", size=11, color=TEXT_MUTED,
                                text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                alignment=ft.Alignment.CENTER,
            ),
        ],
        width=160,
        height=160,
    )

def build_input_panel():
    sensor_rows = [sensor_slider_row(l, mn, mx, v) for l, mn, mx, v in SENSOR_FIELDS]
    atm_rows = [
        atm_slider_row("Temperatur", "°C", -5, 45, 13.6, decimals=1),
        atm_slider_row("Kelembaban relatif (RH)", "%", 0, 100, 48),
        atm_slider_row("Kelembaban absolut (AH)", "g/m³", 0, 2, 0.76, decimals=2),
    ]

    co_slider = ft.Slider(min=500, max=2500, value=1360)

    temp_slider = ft.Slider(
        min=-5,
        max=45,
        value=13.6
    )

    hour_dropdown = ft.Dropdown(
        label="Jam",
        value="12",
        options=[ft.dropdown.Option(key=str(h), text=f"{h:02d}:00") for h in range(0, 24, 3)],
        border_color=BORDER,
        focused_border_color=TEAL,
        label_style=ft.TextStyle(size=12, color=TEXT_MUTED),
        text_style=ft.TextStyle(size=13, color=TEXT_MAIN),
        expand=True,
    )

    month_dropdown = ft.Dropdown(
        label="Bulan",
        value="Maret",
        options=[ft.dropdown.Option(key=m, text=m) for m in MONTHS],
        border_color=BORDER,
        focused_border_color=TEAL,
        label_style=ft.TextStyle(size=12, color=TEXT_MUTED),
        text_style=ft.TextStyle(size=13, color=TEXT_MAIN),
        expand=True,
    )

    predict_btn = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=WHITE, size=18),
                ft.Text("Jalankan Prediksi", color=WHITE, size=14,
                        weight=ft.FontWeight.W_500),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=TEAL,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        width=float("inf"),
    )

    return card(
        ft.Column(
            controls=[
                section_label("INPUT SENSOR", ft.Icons.MEMORY_ROUNDED),
                ft.Column(controls=sensor_rows, spacing=10),
                divider(),
                section_label("KONDISI ATMOSFER", ft.Icons.THERMOSTAT_ROUNDED),
                ft.Column(controls=atm_rows, spacing=10),
                divider(),
                section_label("WAKTU PENGUKURAN", ft.Icons.SCHEDULE_ROUNDED),
                ft.Row(controls=[hour_dropdown, month_dropdown], spacing=12),
                ft.Container(height=4),
                predict_btn,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )
    )

def build_result_panel():
    result_card = card(
        ft.Column(
            controls=[
                section_label("HASIL PREDIKSI — BENZENA (C6H6)", ft.Icons.TRACK_CHANGES_ROUNDED),
                ft.Container(height=8),
                ft.Column(
                    controls=[
                        gauge_arc(),
                        ft.Text("C6H6 — Benzena", size=12, color=TEXT_MUTED),
                        status_badge("⚠  Sedang", AMBER_LIGHT, "#633806"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Container(height=4),
                divider(),
                ft.Container(height=8),
                ft.Text("Interpretasi", size=12, color=TEXT_MUTED),
                ft.Text(
                    "Konsentrasi Benzena berada di level sedang. "
                    "Disarankan membatasi aktivitas di luar ruangan.",
                    size=13, color=TEXT_MAIN,
                ),
            ],
            spacing=8,
        )
    )

    metrics_card = card(
        ft.Column(
            controls=[
                section_label("EVALUASI MODEL", ft.Icons.ANALYTICS_ROUNDED),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        metric_card("MAE", "0.82"),
                        metric_card("RMSE", "1.14"),
                        metric_card("R²", "0.91"),
                    ],
                    spacing=8,
                ),
                ft.Container(height=4),
                ft.Text(
                    "Algoritma: Linear Regression  ·  Dataset: UCI Air Quality 2004–2005",
                    size=11, color=TEXT_MUTED,
                ),
            ],
            spacing=8,
        )
    )

    return ft.Column(
        controls=[result_card, metrics_card],
        spacing=12,
        expand=True,
    )

def build_trend_section():
    hourly = [5.2,4.8,4.5,4.3,4.6,5.8,8.2,11.4,12.8,11.6,
              10.2,9.4,8.9,9.1,9.8,10.6,11.2,10.8,9.6,8.4,
              7.6,6.8,6.2,5.6]
    max_val = max(hourly)

    bars = []
    for i, v in enumerate(hourly):
        color = TEAL if 7 <= i <= 18 else TEAL_LIGHT
        bars.append(
            ft.Column(
                controls=[
                    ft.Container(
                        width=18,
                        height=max(4, 100 * v / max_val),
                        bgcolor=color,
                        border_radius=ft.BorderRadius(top_left=3, top_right=3, bottom_left=0, bottom_right=0),
                        tooltip=ft.Tooltip(message=f"{i:02d}:00 → {v} µg/m³"),
                    ),
                    ft.Text(
                        f"{i:02d}" if i % 6 == 0 else "",
                        size=9, color=TEXT_MUTED,
                        text_align=ft.TextAlign.CENTER,
                        width=18,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            )
        )

    return card(
        ft.Column(
            controls=[
                section_label("TREN POLUSI HARIAN — RATA-RATA PER JAM", ft.Icons.SHOW_CHART_ROUNDED),
                ft.Container(height=4),
                ft.Container(
                    content=ft.Row(
                        controls=bars,
                        spacing=3,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    height=120,
                    alignment=ft.Alignment.BOTTOM_LEFT,
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Container(width=10, height=10, bgcolor=TEAL, border_radius=2),
                        ft.Text("Siang (07:00–18:00)", size=11, color=TEXT_MUTED),
                        ft.Container(width=10, height=10, bgcolor=TEAL_LIGHT, border_radius=2),
                        ft.Text("Malam (19:00–06:00)", size=11, color=TEXT_MUTED),
                    ],
                    spacing=6,
                ),
            ],
            spacing=8,
        )
    )

def build_page(page: ft.Page):
    page.title   = "Air Quality Predictor"
    page.bgcolor = GRAY_BG
    page.padding = 24
    page.scroll  = ft.ScrollMode.AUTO

    header = ft.Row(
        controls=[
            ft.Icon(ft.Icons.AIR_ROUNDED, size=28, color=TEAL),
            ft.Column(
                controls=[
                    ft.Text("Air Quality Predictor", size=22,
                            weight=ft.FontWeight.W_500, color=TEXT_MAIN),
                    ft.Text(
                        "Prediksi konsentrasi polutan udara berdasarkan pembacaan sensor",
                        size=13, color=TEXT_MUTED,
                    ),
                ],
                spacing=2,
            ),
        ],
        spacing=12,
    )

    main_row = ft.Row(
        controls=[
            ft.Container(content=build_input_panel(), expand=2),
            ft.Container(content=build_result_panel(), expand=3),
        ],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(height=8),
                main_row,
                ft.Container(height=4),
                build_trend_section(),
                ft.Container(height=12),
                ft.Text(
                    "UAP Machine Learning  ·  Teknik Informatika  ·  Universitas Brawijaya",
                    size=11, color=TEXT_MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=12,
            expand=True,
        )
    )
