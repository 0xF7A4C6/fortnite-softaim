import json, os, ctypes, torch, threading, mss, cv2, time, math, win32api
import dearpygui.dearpygui as dpg
import numpy as np

__config__ = json.loads(open("../script/config.json", "r+").read())


class Console:
    @staticmethod
    def print(content: str):
        print(content)


class Configurator:
    @staticmethod
    def check():
        for paths in ["../script/", "../assets/"]:
            if not os.path.exists(paths):
                os.mkdir(paths)
                Console.print(f'[+] Created directory "{paths}"')

        if not os.path.exists("../script/config.json"):
            xy_sens = input("X-Axis and Y-Axis Sensitivity: ")
            targeting_sens = input("Targeting Sensitivity: ")

            with open("lib/config/config.json", "w") as outfile:
                json.dump(
                    {
                        "sensitivity": {
                            "xy_sens": xy_sens,
                            "targeting_sens": targeting_sens,
                            "xy_scale": 10 / int(xy_sens),
                            "targeting_scale": 1000
                            / (int(targeting_sens) * int(xy_sens)),
                        }
                    },
                    outfile,
                )


class Gui(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title="AIm", decorated=True, width=380, height=650)

        with dpg.window(tag="Primary Window"):
            with dpg.tab_bar():
                with dpg.tab(label="Configuration"):
                    """with dpg.tree_node(label="Visual"):
                    with dpg.tree_node(label="FOV"):
                        dpg.add_checkbox(label="Enabled", tag="fov_enabled")
                        dpg.add_slider_float(label="FOV", default_value=416, max_value=832, tag="fov_value")

                    with dpg.tree_node(label="ESP"):
                        dpg.add_checkbox(label="Enabled", tag="esp_enabled")
                        dpg.add_checkbox(label="Confidence", tag="esp_confidence")
                        dpg.add_checkbox(label="Optimal path", tag="esp_path")"""

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
                            label="Enabled", tag="aimbot_enabled", default_value=True
                        )
                        # dpg.add_radio_button(("Head", "Body", "Feet"), tag="aimbot_position")

                    with dpg.tree_node(label="Trigger bot"):
                        dpg.add_slider_int(
                            label="Treshold",
                            default_value=20,
                            max_value=50,
                            tag="triggerbot_treshold",
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
                                default_value=30,
                                max_value=200,
                                tag="behaviours_increment",
                            )
                            dpg.add_slider_float(
                                label="smooth",
                                default_value=2,
                                max_value=100,
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
                            dpg.add_slider_float(
                                label="Confidence",
                                default_value=0.70,
                                max_value=1,
                                tag="data_confidence",
                            )
                            # dpg.add_radio_button(("On detection", "On lock", "On lock + fire"),tag="data_detection_type")

            with dpg.theme() as global_theme:
                with dpg.theme_component(dpg.mvAll):
                    # mvAll (all components)
                    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 33, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (41, 41, 54, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (112, 94, 156, 74))
                    dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 61))

                    dpg.add_theme_color(dpg.mvThemeCol_Header, (33, 33, 43, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (49, 51, 63, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (41, 41, 54, 255))

                    dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (25, 25, 33, 235))

                    dpg.add_theme_color(dpg.mvPlotCol_FrameBg, (33, 33, 43, 255))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBgHovered, (49, 51, 63, 255)
                    )
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (41, 41, 54, 255))

                    dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (41, 41, 54, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (41, 41, 54, 255))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TitleBgCollapsed, (41, 41, 54, 255)
                    )

                    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (25, 25, 33, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (41, 41, 54, 255))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ScrollbarGrabActive, (49, 51, 63, 255)
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ScrollbarGrabActive, (61, 61, 82, 255)
                    )

                    dpg.add_theme_color(
                        dpg.mvThemeCol_DockingPreview, (112, 94, 156, 255)
                    )

                    # the theme styles etc
                    dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 4)
                    dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 9)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 7)
                    dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
                    dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 4)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)

                with dpg.theme_component(dpg.mvText):
                    dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TextDisabled, (128, 128, 128, 255)
                    )

                with dpg.theme_component(dpg.mvButton):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (33, 33, 43, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (49, 51, 63, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (41, 41, 54, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (188, 148, 250, 255))

                with dpg.theme_component(dpg.mvSliderInt):
                    dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (112, 94, 156, 138))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_SliderGrabActive, (188, 148, 250, 138)
                    )

                with dpg.theme_component(dpg.mvTab):
                    dpg.add_theme_color(dpg.mvThemeCol_Tab, (41, 41, 54, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (61, 61, 82, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TabActive, (51, 56, 69, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (41, 41, 54, 255))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_TabUnfocusedActive, (41, 41, 54, 255)
                    )

                with dpg.theme_component(dpg.mvSeparator):
                    dpg.add_theme_color(dpg.mvThemeCol_Separator, (112, 94, 156, 255))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_SeparatorHovered, (188, 148, 250, 255)
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_SeparatorActive, (214, 148, 255, 255)
                    )

                with dpg.theme_component(dpg.mvResizeHandler):
                    dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (112, 94, 156, 74))
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ResizeGripHovered, (188, 148, 250, 74)
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ResizeGripActive, (214, 148, 255, 74)
                    )

        dpg.bind_theme(global_theme)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class Aimbot(threading.Thread):
    def __init__(self):
        self.fov = 350

        self.screensize = {
            "X": ctypes.windll.user32.GetSystemMetrics(0),
            "Y": ctypes.windll.user32.GetSystemMetrics(1),
        }

        self.screen_x = int(self.screensize["X"] / 2)
        self.screen_y = int(self.screensize["Y"] / 2)

        self.detection_box = {
            "left": int((self.screensize["X"] / 2) - (self.fov // 2)),
            "top": int((self.screensize["Y"] / 2) - (self.fov // 2)),
            "width": self.fov,
            "height": self.fov,
        }

        self.model = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path="../assets/best.pt",
            force_reload=False,
        )

        self.screen = mss.mss()
        self.extra = ctypes.c_ulong(0)
        self.ii_ = Input_I()

        self.mouse_delay=0.0006

        self.sens_config = __config__['sensitivity']

        threading.Thread.__init__(self)

    def left_click(self):
        ctypes.windll.user32.mouse_event(0x0002)  # left mouse down
        self.sleep(0.0001)
        ctypes.windll.user32.mouse_event(0x0004)  # left mouse up

    def sleep(self, duration, get_now=time.perf_counter):
        if duration == 0:
            return
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    def is_aimbot_enabled(self):
        return bool(dpg.get_value("aimbot_enabled"))

    def is_targeted(self):
        return True if win32api.GetKeyState(0x02) in (-127, -128) else False

    def is_target_locked(self, x, y):
        threshold = int(dpg.get_value("triggerbot_treshold"))
        return (
            True
            if self.screen_x - threshold <= x <= self.screen_x + threshold
            and self.screen_y - threshold <= y <= self.screen_y + threshold
            else False
        )

    def move_crosshair(self, x, y):
        if self.is_targeted():
            scale = self.sens_config["targeting_scale"]
        else:
            return
        
        smooth = self.interpolate_coordinates_from_center((x, y), scale, int(dpg.get_value("behaviours_smooth"))) if int(dpg.get_value("behaviours_smooth")) != 0 else self.interpolate_coordinates_from_center_direct((x, y), scale)

        for rel_x, rel_y in smooth:  # , float(dpg.get_value("behaviours_speed"))
            self.ii_.mi = MouseInput(
                rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(self.extra)
            )

            input_obj = Input(ctypes.c_ulong(0), self.ii_)

            ctypes.windll.user32.SendInput(
                1, ctypes.byref(input_obj), ctypes.sizeof(input_obj)
            )

            self.sleep(self.mouse_delay)

    # generator yields pixel tuples for relative movement
    def ease_out_quad(self, t):
        return 1 - (1 - t) ** 2
    
    def interpolate_coordinates_from_center_direct(self, absolute_coordinates, scale):
        diff_x = (absolute_coordinates[0] - 960) * scale/self.pixel_increment
        diff_y = (absolute_coordinates[1] - 540) * scale/self.pixel_increment
        length = int(math.dist((0,0), (diff_x, diff_y)))
        if length == 0: return
        unit_x = (diff_x/length) * self.pixel_increment
        unit_y = (diff_y/length) * self.pixel_increment
        x = y = sum_x = sum_y = 0
        for k in range(0, length):
            sum_x += x
            sum_y += y
            x, y = round(unit_x * k - sum_x), round(unit_y * k - sum_y)
            yield x, y

    def interpolate_coordinates_from_center(
        self, absolute_coordinates, scale, smoothness
    ):
        diff_x = (absolute_coordinates[0] - self.screen_x) * scale / self.pixel_increment
        diff_y = (absolute_coordinates[1] - self.screen_y) * scale / self.pixel_increment
        length = int(math.dist((0, 0), (diff_x, diff_y)))

        if length == 0:
            return

        # Calculate fixed unit vectors without speed_factor
        unit_x = (diff_x / length) * self.pixel_increment
        unit_y = (diff_y / length) * self.pixel_increment

        x = y = sum_x = sum_y = 0

        for k in range(0, length):
            t = k / length
            eased_t = self.ease_out_quad(t)

            # Adjust the easing function using the smoothness parameter
            smoothed_t = t ** (smoothness / 100.0)
            eased_t = self.ease_out_quad(smoothed_t)

            sum_x += x
            sum_y += y
            x, y = round(unit_x * eased_t - sum_x), round(unit_y * eased_t - sum_y)
            yield x, y

    def run(self):
        if torch.cuda.is_available():
            Console.print("[+] Cuda is available")

        print(self.detection_box)

        while True:
            self.model.conf = float(dpg.get_value("aimbot_confidence"))  # base confidence threshold (or base detection (0-1)
            self.model.iou = float(dpg.get_value("aimbot_iou"))  # NMS IoU (0-1)
            self.pixel_increment = int(dpg.get_value("behaviours_increment"))

            frame = np.array(self.screen.grab(self.detection_box))
            # frame = cv2.resize(fr, None, fx=0.5, fy=0.5)
            start_time = time.perf_counter()

            results = self.model(frame)
            #print(results)

            if len(results.xyxy[0]) != 0:
                least_crosshair_dist = closest_detection = player_in_frame = False

                for *box, conf, _ in results.xyxy[0]:
                    x1y1 = [int(x.item()) for x in box[:2]]
                    x2y2 = [int(x.item()) for x in box[2:]]

                    x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
                    height = y2 - y1

                    relative_head_X, relative_head_Y = int((x1 + x2) / 2), int(
                        (y1 + y2) / 2 - height / int(dpg.get_value("aimbot_pos"))
                    )

                    own_player = x1 < 15 or (x1 < self.fov / 5 and y2 > self.fov / 1.2)

                    crosshair_dist = math.dist(
                        (relative_head_X, relative_head_Y), (self.fov / 2, self.fov / 2)
                    )

                    if not least_crosshair_dist:
                        least_crosshair_dist = crosshair_dist

                    if crosshair_dist <= least_crosshair_dist and not own_player:
                        least_crosshair_dist = crosshair_dist
                        closest_detection = {
                            "x1y1": x1y1,
                            "x2y2": x2y2,
                            "relative_head_X": relative_head_X,
                            "relative_head_Y": relative_head_Y,
                            "conf": conf,
                        }

                    if not own_player:
                        cv2.rectangle(frame, x1y1, x2y2, (255, 0, 6), 2)
                        cv2.putText(
                            frame,
                            f"{int(conf * 100)}%",
                            x1y1,
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (6, 0, 255),
                            1,
                        )
                    else:
                        own_player = False
                        if not player_in_frame:
                            player_in_frame = True

                if closest_detection:
                    cv2.circle(
                        frame,
                        (
                            closest_detection["relative_head_X"],
                            closest_detection["relative_head_Y"],
                        ),
                        5,
                        (115, 244, 113),
                        -1,
                    )

                    cv2.line(
                        frame,
                        (
                            closest_detection["relative_head_X"],
                            closest_detection["relative_head_Y"],
                        ),
                        (self.fov // 2, self.fov // 2),
                        (244, 242, 113),
                        1,
                    )

                    absolute_head_X, absolute_head_Y = (
                        closest_detection["relative_head_X"]
                        + self.detection_box["left"],
                        closest_detection["relative_head_Y"]
                        + self.detection_box["top"],
                    )

                    x1, y1 = closest_detection["x1y1"]
                    cv2.putText(
                        frame,
                        "TARGETING",
                        (x1 + 40, y1),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.5,
                        (115, 113, 244),
                        1,
                    )

                    if self.is_target_locked(absolute_head_X, absolute_head_Y):
                        if bool(dpg.get_value("triggerbot_enabled")):
                            self.left_click()
                        cv2.putText(
                            frame,
                            "LOCKED",
                            (x1 + 40, y1),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (115, 244, 113),
                            1,
                        )  # draw the confidence labels on the bounding boxes
                    else:
                        cv2.putText(
                            frame,
                            "TARGETING",
                            (x1 + 40, y1),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (115, 113, 244),
                            1,
                        )  # draw the confidence labels on the bounding boxes

                    if self.is_aimbot_enabled():
                        self.move_crosshair(absolute_head_X, absolute_head_Y)

            cv2.putText(
                frame,
                f"FPS: {int(1/(time.perf_counter() - start_time))}",
                (5, 30),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (256, 256, 256),
                1,
            )
            cv2.imshow("AI", frame)

            if cv2.waitKey(1) & 0xFF == ord("0"):
                break


if __name__ == "__main__":
    Configurator.check()

    Gui().start()
    Aimbot().run()
