import flet as ft

TEAL        = "#1D9E75"
TEAL_LIGHT  = "#9FE1CB"
AMBER       = "#EF9F27"
AMBER_LIGHT = "#FAEEDA"
GRAY_BG     = "#F8F9FA"
BORDER      = "#E5E7EB"
TEXT_MUTED  = "#6B7280"
TEXT_MAIN   = "#111827"
WHITE       = "#FFFFFF"
RED_LIGHT   = "#FEE2E2"
GREEN_LIGHT = "#DCFCE7"
GREEN_DARK  = "#166534"

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

def make_field(label, hint):
    """Buat TextField dengan label dan hint range."""
    return ft.TextField(
        label=label,
        hint_text=hint,
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=BORDER,
        focused_border_color=TEAL,
        label_style=ft.TextStyle(size=12, color=TEXT_MUTED),
        text_style=ft.TextStyle(size=13, color=TEXT_MAIN),
        hint_style=ft.TextStyle(size=11, color="#C0C8D0"),
        height=56,
        expand=True,
    )

def field_row(tf_a, tf_b):
    """Dua field dalam satu baris."""
    return ft.Row(controls=[tf_a, tf_b], spacing=10)

def status_badge(label, bg, fg):
    return ft.Container(
        content=ft.Text(label, size=12, weight=ft.FontWeight.W_500, color=fg),
        bgcolor=bg,
        border_radius=8,
        padding=ft.Padding(left=14, right=14, top=5, bottom=5),
    )

def get_val(tf, decimals=None):
    """Ambil nilai float dari TextField. Raise ValueError jika tidak valid."""
    raw = tf.value.strip().replace(",", ".")
    v = float(raw)
    return round(v, decimals) if decimals else v

def get_status_co(value):
    if value < 4.0:
        return "🟢 Baik",       GREEN_LIGHT, GREEN_DARK
    elif value < 8.0:
        return "🟡 Sedang",     AMBER_LIGHT, "#633806"
    return "🔴 Berbahaya",      RED_LIGHT,   "#991B1B"

def gauge_ring(value, max_val=12.0):
    size = 150
    ratio = min(max(value / max_val, 0.0), 1.0)
    _, _, fg = get_status_co(value)

    return ft.Container(
        width=size,
        height=size,

        content=ft.Stack(
            width=size,
            height=size,

            controls=[

                ft.ProgressRing(
                    value=1,
                    width=size,
                    height=size,
                    stroke_width=16,
                    color=BORDER,
                ),

                ft.ProgressRing(
                    value=ratio,
                    width=size,
                    height=size,
                    stroke_width=16,
                    color=fg,
                ),

                ft.Container(
                    width=size,
                    height=size,
                    alignment=ft.Alignment.CENTER,

                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"{value:.2f}",
                                size=30,
                                weight=ft.FontWeight.W_600,
                                color=TEXT_MAIN,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "mg/m³",
                                size=11,
                                color=TEXT_MUTED,
                                text_align=ft.TextAlign.CENTER,
                            ),

                        ],

                        spacing=-2,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ),
            ]
        )
    )

def build_input_panel(page, on_predict):
    from services.predictor import AirQualityPredictor
    predictor = AirQualityPredictor()

    # Sensor PT08
    tf_co   = make_field("PT08.S1 – Sensor CO",   "600–2100")
    tf_nmhc = make_field("PT08.S2 – Sensor NMHC", "350–2250")
    tf_nox  = make_field("PT08.S3 – Sensor NOx",  "300–2700")
    tf_no2  = make_field("PT08.S4 – Sensor NO2",  "500–2800")
    tf_o3   = make_field("PT08.S5 – Sensor O3",   "200–2550")

    # Konsentrasi GT
    tf_nmhc_gt = make_field("NMHC(GT) µg/m³",  "0–1400")
    tf_c6h6    = make_field("C6H6(GT) µg/m³",  "0–60")
    tf_nox_gt  = make_field("NOx(GT) ppb",      "0–1500")
    tf_no2_gt  = make_field("NO2(GT) µg/m³",   "0–340")

    # Atmosfer
    tf_temp = make_field("Temperatur °C",         "-5–45")
    tf_rh   = make_field("Kelembaban Relatif %",  "0–100")
    tf_ah   = make_field("Kelembaban Absolut",    "0.1–2.5")

    # Error text
    err_text = ft.Text("", color="#EF4444", size=11)

    # Waktu
    hour_dropdown = ft.Dropdown(
        label="Jam",
        value="18",
        options=[ft.dropdown.Option(key=str(h), text=f"{h:02d}:00") for h in range(24)],
        border_color=BORDER, focused_border_color=TEAL,
        label_style=ft.TextStyle(size=12, color=TEXT_MUTED),
        text_style=ft.TextStyle(size=13, color=TEXT_MAIN),
        expand=True,
    )
    month_dropdown = ft.Dropdown(
        label="Bulan",
        value="Maret",
        options=[ft.dropdown.Option(key=m, text=m) for m in MONTHS],
        border_color=BORDER, focused_border_color=TEAL,
        label_style=ft.TextStyle(size=12, color=TEXT_MUTED),
        text_style=ft.TextStyle(size=13, color=TEXT_MAIN),
        expand=True,
    )

    def set_error(tf, msg):
        tf.border_color = "#EF4444"
        tf.update()
        err_text.value = msg
        err_text.update()

    def clear_errors():
        err_text.value = ""
        err_text.update()
        for tf in [tf_co, tf_nmhc, tf_nox, tf_no2, tf_o3,
                   tf_nmhc_gt, tf_c6h6, tf_nox_gt, tf_no2_gt,
                   tf_temp, tf_rh, tf_ah]:
            tf.border_color = BORDER
            tf.update()

    def jalankan_prediksi(e):
        clear_errors()
        try:
            hasil = predictor.predict(
                sensor_co=get_val(tf_co),
                nmhc_gt=get_val(tf_nmhc_gt),
                c6h6_gt=get_val(tf_c6h6),
                sensor_nmhc=get_val(tf_nmhc),
                nox_gt=get_val(tf_nox_gt),
                sensor_nox=get_val(tf_nox),
                no2_gt=get_val(tf_no2_gt),
                sensor_no2=get_val(tf_no2),
                sensor_o3=get_val(tf_o3),
                temperature=get_val(tf_temp),
                rh=get_val(tf_rh),
                ah=get_val(tf_ah),
                month=MONTHS.index(month_dropdown.value) + 1,
                hour=int(hour_dropdown.value),
            )
            on_predict(hasil)
            page.update()
        except ValueError as ex:
            err_text.value = f"⚠ Input tidak valid: {ex}"
            err_text.update()

    predict_btn = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=WHITE),
                ft.Text("Jalankan Prediksi", color=WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=TEAL,
        on_click=jalankan_prediksi,
        width=float("inf"),
    )

    return card(
        ft.Column(
            controls=[
                section_label("INPUT SENSOR (PT08)", ft.Icons.MEMORY_ROUNDED),
                field_row(tf_co,   tf_nmhc),
                field_row(tf_nox,  tf_no2),
                ft.Row(controls=[tf_o3], spacing=10),

                divider(),

                section_label("KONSENTRASI POLUTAN REFERENSI", ft.Icons.SCIENCE_ROUNDED),
                field_row(tf_nmhc_gt, tf_c6h6),
                field_row(tf_nox_gt,  tf_no2_gt),

                divider(),

                section_label("KONDISI ATMOSFER", ft.Icons.THERMOSTAT_ROUNDED),
                field_row(tf_temp, tf_rh),
                ft.Row(controls=[tf_ah], spacing=10),

                divider(),

                section_label("WAKTU PENGUKURAN", ft.Icons.SCHEDULE_ROUNDED),
                ft.Row([hour_dropdown, month_dropdown]),

                err_text,
                ft.Container(height=4),
                predict_btn,
            ],
            spacing=10,
        )
    )

def build_result_panel(co_val=None):
    if co_val is None:
        return card(
            ft.Column(
                controls=[
                    section_label("HASIL PREDIKSI – CO(GT)", ft.Icons.TRACK_CHANGES_ROUNDED),
                    ft.Container(height=24),
                    ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.AIR_ROUNDED, size=52, color=BORDER),
                            ft.Text("Belum ada prediksi", size=14, color=TEXT_MUTED,
                                    text_align=ft.TextAlign.CENTER),
                            ft.Text("Isi input di panel kiri lalu\ntekan Jalankan Prediksi",
                                    size=12, color=BORDER, text_align=ft.TextAlign.CENTER),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    ft.Container(height=24),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    status_label, status_bg, status_fg = get_status_co(co_val)

    info_rows = [
        ("Parameter prediksi", "CO (Carbon Monoxide) – GT"),
        ("Algoritma",          "Random Forest Regressor"),
        ("Pipeline",           "Imputer → Scaler → RF"),
        ("Satuan output",      "mg/m³"),
    ]
    info_items = [
        ft.Row(controls=[
            ft.Text(k, size=11, color=TEXT_MUTED, expand=2),
            ft.Text(v, size=11, color=TEXT_MAIN, expand=3, weight=ft.FontWeight.W_500),
        ], spacing=8)
        for k, v in info_rows
    ]

    skala_items = [
        status_badge("🟢 Baik  (< 4 mg/m³)",       GREEN_LIGHT, GREEN_DARK),
        status_badge("🟡 Sedang  (4–8 mg/m³)",      AMBER_LIGHT, "#633806"),
        status_badge("🔴 Berbahaya  (> 8 mg/m³)",   RED_LIGHT,   "#991B1B"),
    ]

    return card(
        ft.Column(
            controls=[
                section_label("HASIL PREDIKSI – CO(GT)", ft.Icons.TRACK_CHANGES_ROUNDED),
                ft.Container(height=8),
                ft.Row(controls=[gauge_ring(co_val)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=4),
                ft.Row(controls=[status_badge(status_label, status_bg, status_fg)],
                       alignment=ft.MainAxisAlignment.CENTER),
                divider(),
                section_label("INFO MODEL", ft.Icons.INFO_OUTLINE_ROUNDED),
                ft.Container(height=4),
                ft.Column(controls=info_items, spacing=6),
                divider(),
                section_label("SKALA REFERENSI (WHO)", ft.Icons.HEALTH_AND_SAFETY_ROUNDED),
                ft.Container(height=4),
                ft.Column(controls=skala_items, spacing=6),
            ],
            spacing=8,
        )
    )

def build_trend_section():
    hourly = [1.79, 1.47, 1.10, 0.89, 0.76, 0.71, 0.92, 1.81,
              2.82, 2.97, 2.57, 2.26, 2.17, 2.20, 2.13, 2.05,
              2.27, 2.82, 3.44, 3.73, 3.47, 2.60, 1.98, 1.88]
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
                        tooltip=ft.Tooltip(message=f"{i:02d}:00 → {v} mg/m³"),
                    ),
                    ft.Text(
                        f"{i:02d}" if i % 6 == 0 else "",
                        size=9, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER, width=18,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            )
        )

    return card(
        ft.Column(
            controls=[
                section_label("TREN POLUSI HARIAN — RATA-RATA CO PER JAM (AirQualityUCI)", ft.Icons.SHOW_CHART_ROUNDED),
                ft.Container(height=4),
                ft.Container(
                    content=ft.Row(controls=bars, spacing=3, vertical_alignment=ft.CrossAxisAlignment.END),
                    height=120,
                    alignment=ft.Alignment(-1, 1),
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
                    ft.Text("Air Quality Predictor", size=22, weight=ft.FontWeight.W_500, color=TEXT_MAIN),
                    ft.Text("Prediksi konsentrasi CO berdasarkan pembacaan sensor & kondisi atmosfer",
                            size=13, color=TEXT_MUTED),
                ],
                spacing=2,
            ),
        ],
        spacing=12,
    )

    result_wrapper = ft.Container(content=build_result_panel(None), expand=3)

    def on_predict(co_val):
        result_wrapper.content = build_result_panel(co_val)
        result_wrapper.update()

    main_row = ft.Row(
        controls=[
            ft.Container(content=build_input_panel(page, on_predict), expand=2),
            result_wrapper,
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
            ],
            spacing=12,
            expand=True,
        )
    )
