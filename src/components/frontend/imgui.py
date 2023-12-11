import dearpygui.dearpygui as dpg
import threading


class Gui(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(
            title="Deep aim",
            decorated=True,
            width=380,
            height=650,
        )

        with dpg.window(tag="Primary Window"):
            with dpg.tab_bar():
                with dpg.tab(label="Configuration"):
                    with dpg.tree_node(label="Visual"):
                        with dpg.tree_node(label="FOV"):
                            dpg.add_slider_float(
                                label="FOV",
                                default_value=350,
                                max_value=850,
                                min_value=100,
                                tag="fov_value",
                            )

                    with dpg.tree_node(label="Aimbot"):
                        dpg.add_slider_float(
                            label="Confidence",
                            default_value=0.70,
                            max_value=1,
                            tag="aimbot_confidence",
                        )
                        dpg.add_slider_float(
                            label="NMS IoU",
                            default_value=0.45,
                            max_value=1,
                            tag="aimbot_iou",
                        )
                        dpg.add_slider_int(
                            label="Position",
                            default_value=30,
                            min_value=2,
                            max_value=45,
                            tag="aimbot_pos",
                        )
                        dpg.add_checkbox(
                            label="Enabled",
                            tag="aimbot_enabled",
                            default_value=True,
                        )
                        # dpg.add_radio_button(("Head", "Body", "Feet"), tag="aimbot_position")

                    with dpg.tree_node(label="Trigger bot"):
                        dpg.add_slider_int(
                            label="Treshold",
                            default_value=5,
                            max_value=25,
                            tag="triggerbot_threshold",
                        )
                        dpg.add_checkbox(
                            label="Enabled",
                            tag="triggerbot_enabled",
                            default_value=False,
                        )

                    with dpg.tree_node(label="Behaviours"):
                        with dpg.group(label="Behaviours"):
                            dpg.add_slider_int(
                                label="increment",
                                default_value=80,
                                min_value=4,
                                max_value=150,
                                tag="behaviours_increment",
                            )
                            dpg.add_slider_float(
                                label="smooth",
                                default_value=8,
                                max_value=100,
                                min_value=0,
                                tag="behaviours_smooth",
                            )

                            # dpg.add_slider_float(label="speed", default_value=0.80, max_value=100, tag="behaviours_speed")
                            # dpg.add_radio_button(label="algorithm", items=("direct", "Bézier"), tag="behaviours_algorithm")

                    with dpg.tree_node(label="Data collection"):
                        with dpg.group(label="Data collection"):
                            dpg.add_checkbox(
                                label="Enabled",
                                tag="datacollect_enabled",
                                default_value=True,
                            )
                            dpg.add_checkbox(
                                label="Require lock",
                                tag="datacollect_require_lock",
                                default_value=True,
                            )
                            dpg.add_slider_float(
                                label="Confidence",
                                default_value=0.75,
                                max_value=1,
                                tag="data_confidence",
                            )

            with dpg.theme() as global_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_WindowBg,
                        (25, 25, 33, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_MenuBarBg,
                        (41, 41, 54, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_Border,
                        (112, 94, 156, 74),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_BorderShadow,
                        (0, 0, 0, 61),
                    )

                    dpg.add_theme_color(
                        dpg.mvThemeCol_Header,
                        (33, 33, 43, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_HeaderHovered,
                        (49, 51, 63, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_HeaderActive,
                        (41, 41, 54, 255),
                    )

                    dpg.add_theme_color(
                        dpg.mvThemeCol_PopupBg,
                        (25, 25, 33, 235),
                    )

                    dpg.add_theme_color(
                        dpg.mvPlotCol_FrameBg,
                        (33, 33, 43, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBgHovered,
                        (49, 51, 63, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBgActive,
                        (41, 41, 54, 255),
                    )

                    dpg.add_theme_color(
                        dpg.mvThemeCol_TitleBg,
                        (41, 41, 54, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TitleBgActive,
                        (41, 41, 54, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TitleBgCollapsed,
                        (41, 41, 54, 255),
                    )

                    dpg.add_theme_color(
                        dpg.mvThemeCol_ScrollbarBg,
                        (25, 25, 33, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ScrollbarGrab,
                        (41, 41, 54, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ScrollbarGrabActive,
                        (49, 51, 63, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ScrollbarGrabActive,
                        (61, 61, 82, 255),
                    )

                    dpg.add_theme_color(
                        dpg.mvThemeCol_DockingPreview,
                        (112, 94, 156, 255),
                    )

                    # the theme styles etc
                    dpg.add_theme_style(
                        dpg.mvStyleVar_TabRounding,
                        4,
                    )
                    dpg.add_theme_style(
                        dpg.mvStyleVar_ScrollbarRounding,
                        9,
                    )
                    dpg.add_theme_style(
                        dpg.mvStyleVar_WindowRounding,
                        7,
                    )
                    dpg.add_theme_style(
                        dpg.mvStyleVar_GrabRounding,
                        3,
                    )
                    dpg.add_theme_style(
                        dpg.mvStyleVar_FrameRounding,
                        3,
                    )
                    dpg.add_theme_style(
                        dpg.mvStyleVar_PopupRounding,
                        4,
                    )
                    dpg.add_theme_style(
                        dpg.mvStyleVar_ChildRounding,
                        4,
                    )

                with dpg.theme_component(dpg.mvText):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_Text,
                        (255, 255, 255, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TextDisabled,
                        (128, 128, 128, 255),
                    )

                with dpg.theme_component(dpg.mvButton):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_Button,
                        (33, 33, 43, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ButtonHovered,
                        (49, 51, 63, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ButtonActive,
                        (41, 41, 54, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_CheckMark,
                        (188, 148, 250, 255),
                    )

                with dpg.theme_component(dpg.mvSliderInt):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_SliderGrab,
                        (112, 94, 156, 138),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_SliderGrabActive,
                        (188, 148, 250, 138),
                    )

                with dpg.theme_component(dpg.mvTab):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_Tab,
                        (41, 41, 54, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TabHovered,
                        (61, 61, 82, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TabActive,
                        (51, 56, 69, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TabUnfocused,
                        (41, 41, 54, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TabUnfocusedActive,
                        (41, 41, 54, 255),
                    )

                with dpg.theme_component(dpg.mvSeparator):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_Separator,
                        (112, 94, 156, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_SeparatorHovered,
                        (188, 148, 250, 255),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_SeparatorActive,
                        (214, 148, 255, 255),
                    )

                with dpg.theme_component(dpg.mvResizeHandler):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ResizeGrip,
                        (112, 94, 156, 74),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ResizeGripHovered,
                        (188, 148, 250, 74),
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ResizeGripActive,
                        (214, 148, 255, 74),
                    )

        dpg.bind_theme(global_theme)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
