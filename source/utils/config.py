from utils.math_ import cos, sin, tau

functions_to_be_animated = {
    'heart': lambda t: 20 * (
        16 * (sin(tau * t) ** 3)
        + 1j * (13 * cos(tau * t) - 5 * cos(2 * tau * t) - 2 * cos(3 * tau * t) - cos(4 * tau * t))
    ),
    'off-origin ellipse': lambda t: 100 + 200 * (
        cos(tau * t)
        + 2j * sin(tau * t)
    ),
    'figure-eight': lambda t: 300 * (
        sin(tau * t)
        + 1j * sin(tau * t) * cos(tau * t)
    ),
    'cardioid': lambda t: 200 * (
        cos(tau * t) * (1 - cos(tau * t))
        + 1j * sin(tau * t) * (1 - cos(tau * t))
    ),
    'lissajous': lambda t: 100 * (
        4 * cos(tau * t)
        + 3j * sin(4 * tau * t)
    ),
}
functions_to_be_animated = list(functions_to_be_animated.items())
animation_duration = 3
num_terms_in_series = 10
animation_endpoint_radius = 10

window_shape = (1900, 1000)
window_fullscreen = False
window_background = (0.1, 0.1, 0.1)
window_frames_per_second = 60

line_width = 3
primary_opacity = 128
secondary_opacity = 50
primary_highlight = (255, 0, 0)
secondary_highlight = (0, 255, 255)

time_marker_radius = 10
time_line_start = 100, 100
time_line_end = 700, 100

label_font_name = 'Arial'
label_font_size = 36
label_color = (255, 255, 255, 255)

key_exit = 'ESCAPE'
key_pause = 'P'
key_slow_down = 'DOWN'
key_speed_up = 'UP'
key_show_components = 'S'
key_go_to_next = 'N'
