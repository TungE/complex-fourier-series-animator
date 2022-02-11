import pyglet

import utils.config as config
from utils.complex_fourier_series_animation import ComplexFourierSeriesAnimation
from utils.defaults import set_attributes
from utils.math_ import array, get_distance


@set_attributes(counter=0)
def get_function_to_be_animated():
    counter = get_function_to_be_animated.counter
    get_function_to_be_animated.counter += 1
    get_function_to_be_animated.counter %= len(config.functions_to_be_animated)

    return config.functions_to_be_animated[counter]

@set_attributes(default_kwargs=dict(width=config.line_width))
def line(*args, opacity=None, **kwargs):
    line_ = pyglet.shapes.Line(*args, **kwargs, **line.default_kwargs)

    if opacity is not None:
        line_.opacity = opacity

    return line_

def key(name):
    return getattr(pyglet.window.key, name)

def draw_label(label, text):
        label.text = text
        label.draw()

def main():
    # create window
    window = pyglet.window.Window()
    origin = array(config.window_shape) // 2
    show_components = True
    is_paused = False

    # create labels
    label_pause = pyglet.text.Label(anchor_x='right')
    label_pause.x = config.window_shape[0]
    label_pause.text = 'paused'

    label_fps = pyglet.text.Label(anchor_x='right')
    label_fps.x = config.window_shape[0]
    label_fps_text = lambda: f'{pyglet.clock.get_fps():.0f} fps'

    label_animation_duration = pyglet.text.Label()
    label_animation_duration_text = lambda duration: f'{duration} seconds'

    label_function_name = pyglet.text.Label(anchor_y='top')
    label_function_name.y = config.window_shape[1]

    labels = (
        label_pause,
        label_fps,
        label_animation_duration,
        label_function_name,
    )

    for label in labels:
        label.font_name = config.label_font_name
        label.font_size = config.label_font_size
        label.color = config.label_color

    # initialize animation
    function_to_be_animated = function_name = animation_duration = None
    animation_path_maxlen = animation = timer = None

    def initialize_animation():
        nonlocal function_to_be_animated, function_name, animation_duration
        nonlocal animation_path_maxlen, animation, timer

        function_name, function_to_be_animated = get_function_to_be_animated()
        animation_duration = config.animation_duration
        animation_path_maxlen = animation_duration * config.window_frames_per_second

        animation = ComplexFourierSeriesAnimation(
            function_to_be_animated,
            num_terms=config.num_terms_in_series,
            path_maxlen=animation_path_maxlen
        )

        timer = 0
    
    initialize_animation()

    # define function for drawing the complex fourier series animation
    def draw_animation(animation):
        batch = pyglet.graphics.Batch()
        lines = list()
        arcs = list()

        start = origin.copy()
        
        # draw the components or the direct vector
        if show_components:
            for vector in animation.vectors:
                end = start + vector.vector

                lines.append(line(*start, *end, opacity=config.primary_opacity, batch=batch))
                arcs.append(pyglet.shapes.Arc(*start, get_distance(start, end), batch=batch))
                arcs[-1].opacity = config.primary_opacity

                start = end.copy()
        else:
            for vector in animation.vectors:
                start += vector.vector

            lines.append(line(*origin, *start, opacity=config.primary_opacity, batch=batch))

        # draw the trailing path of the endpoint
        path = animation.path
        path_segments = list()

        if len(path) > 1:
            previous_point = None
            for current_point in path:
                current_shifted_point = current_point + origin

                if previous_point is None:
                    previous_point = current_shifted_point
                    continue

                path_segments.append(line(
                    *previous_point, *current_shifted_point,
                    color=config.primary_highlight, batch=batch
                ))

                previous_point = current_shifted_point.copy()

        # draw the endpoint
        circle = pyglet.shapes.Circle(
            *start,
            color=config.secondary_highlight,
            radius=config.animation_endpoint_radius,
            batch=batch
        )

        batch.draw()

    # define function for drawing the window
    @window.event
    def on_draw():
        window.clear()
        pyglet.gl.glClearColor(*config.window_background, 1)

        batch = pyglet.graphics.Batch()

        # define x-axis and y-axis
        x_axis = line(
            0, origin[1], config.window_shape[0], origin[1],
            opacity=config.secondary_opacity, batch=batch
        )
        y_axis = line(
            origin[0], 0, origin[0], config.window_shape[1],
            opacity=config.secondary_opacity, batch=batch
        )

        # define timeline and time marker
        x_difference = config.time_line_end[0] - config.time_line_start[0]
        y_difference = config.time_line_end[1] - config.time_line_start[1]
        time_line = line(
            *config.time_line_start, *config.time_line_end,
            opacity=config.secondary_opacity, batch=batch
        )
        time_marker = pyglet.shapes.Circle(
            config.time_line_start[0] + (x_difference * timer),
            config.time_line_start[1] + (y_difference * timer),
            radius=config.time_marker_radius, batch=batch
        )
        time_marker.opacity = config.primary_opacity

        batch.draw()

        # draw the complex fourier series animation
        draw_animation(animation)

        # draw labels
        draw_label(label_animation_duration, label_animation_duration_text(animation_duration))
        draw_label(label_function_name, function_name)
        if is_paused:
            label_pause.draw()
        else:
            draw_label(label_fps, label_fps_text())

    # record the keyboard input states
    key_state_current = key_state_previous = set()

    @window.event
    def on_key_press(symbol, modifiers):
        key_state_current.add(symbol)
    
    @window.event
    def on_key_release(symbol, modifiers):
        key_state_current.discard(symbol)

    is_key_pressed = lambda key_: key_ in key_state_current
    was_key_pressed = lambda key_: key_ in key_state_previous
    just_key_pressed = lambda key_: is_key_pressed(key_) and not was_key_pressed(key_)

    # handle input and update the animation
    def update(time_elapsed):
        if is_key_pressed(key(config.key_exit)):
            pyglet.app.exit()

        nonlocal is_paused, animation_duration, show_components, key_state_previous

        if just_key_pressed(key(config.key_pause)):
            is_paused = not is_paused
        elif just_key_pressed(key(config.key_slow_down)):
            animation_duration = max(animation_duration - 1, 1)
        elif just_key_pressed(key(config.key_speed_up)):
            animation_duration += 1
        elif just_key_pressed(key(config.key_show_components)):
            show_components = not show_components
        elif just_key_pressed(key(config.key_go_to_next)):
            initialize_animation()

        key_state_previous = key_state_current.copy()

        if not is_paused:
            nonlocal timer
            time_step = time_elapsed / animation_duration

            timer += time_step
            timer %= 1

            animation.update(time_step)

    # run the application
    def run():
        window.set_size(*config.window_shape)
        window.set_fullscreen(config.window_fullscreen)

        pyglet.gl.glLineWidth(config.line_width)
        pyglet.clock.schedule_interval(update, 1 / config.window_frames_per_second)
        pyglet.app.run()

    run()

if __name__ == '__main__':
    main()
