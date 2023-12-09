import json, os, ctypes, torch, threading, mss, cv2, time, math, win32api, random, uuid
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


class Overlay:
    def __init__(self) -> None:
        dpg.create_viewport(
            title="overlay",
            always_on_top=True,
            decorated=False,
            clear_color=[
                0.0,
                0.0,
                0.0,
                0.0,
            ],
        )

        dpg.set_viewport_always_top(True)
        dpg.create_context()
        dpg.setup_dearpygui()

        dpg.add_viewport_drawlist(
            front=False,
            tag="Viewport_back",
        )

        with dpg.window(label="test", width=200, height=300):
            dpg.add_checkbox(
                label="Show Fov",
                callback=Overlay.show_fov,
            )
            dpg.add_slider_float(
                label="Fov",
                min_value=25,
                max_value=150,
                default_value=25,
                tag="slider1",
            )

        dpg.show_viewport()
        dpg.toggle_viewport_fullscreen()

    @staticmethod
    def show_fov(sender, data):
        global circle

        if data == True:
            sl_value = dpg.get_value("slider1")
            circle = dpg.draw_circle(
                (960, 540),
                sl_value,
                color=(255, 255, 255, 255),
                parent="Viewport_back",
            )

        if data == False:
            dpg.delete_item(circle)


class Gui(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        dpg.create_context()
        dpg.create_viewport(title="AIm", decorated=True, width=380, height=650,)

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
                                default_value=80,
                                min_value=4,
                                max_value=150,
                                tag="behaviours_increment",
                            )
                            dpg.add_slider_float(
                                label="smooth",
                                default_value=8,
                                max_value=100,
                                min_value=1,
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
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput),
    ]


class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I),
    ]


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long),
    ]


class Aimbot(threading.Thread):
    def __init__(self) -> None:
        self.fov = 350
        self.resize = self.fov

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

        self.mouse_delay = 0.0001
        self.sens_config = __config__["sensitivity"]

        threading.Thread.__init__(self)

    def left_click(self) -> None:
        ctypes.windll.user32.mouse_event(0x0002)
        self.sleep(0.0001)
        ctypes.windll.user32.mouse_event(0x0004)

    def sleep(self, duration: float, get_now: float = time.perf_counter) -> None:
        if duration == 0:
            return

        now = get_now()
        end = now + duration

        while now < end:
            now = get_now()

    def is_aimbot_enabled(self) -> bool:
        return bool(dpg.get_value("aimbot_enabled"))

    def is_targeted(self) -> bool:
        return True if win32api.GetKeyState(0x02) in (-127, -128) else False

    def is_target_locked(self, x: int, y: int) -> None:
        threshold = int(dpg.get_value("triggerbot_treshold"))

        return (
            True
            if self.screen_x - threshold <= x <= self.screen_x + threshold
            and self.screen_y - threshold <= y <= self.screen_y + threshold
            else False
        )

    def move_crosshair(self, target_x: int, target_y: int) -> None:
        if not self.is_targeted():
            return

        scale = self.sens_config["targeting_scale"]

        # Determine whether to use smooth movement or direct movement
        smoothness = int(dpg.get_value("behaviours_smooth"))
        coordinates_generator = self.interpolate_coordinates_from_center(
            (target_x, target_y),
            scale,
            smoothness,
        )

        # Move the mouse crosshair
        for rel_x, rel_y in coordinates_generator:
            self.move_mouse(rel_x, rel_y)
            self.sleep(self.mouse_delay)

    def move_mouse(self, rel_x: int, rel_y: int) -> None:
        self.ii_.mi = MouseInput(
            rel_x,
            rel_y,
            0,
            0x0001,
            0,
            ctypes.pointer(self.extra),
        )

        input_obj = Input(
            ctypes.c_ulong(0),
            self.ii_,
        )

        ctypes.windll.user32.SendInput(
            1,
            ctypes.byref(input_obj),
            ctypes.sizeof(input_obj),
        )

    def cubic_ease_out(self, t):
        return 1 - (1 - t) ** float(dpg.get_value("behaviours_smooth"))

    def bezier_cubic(self, t: float, p0: float, p1: float, p2: float, p3: float):
        # Formule de la courbe de Bézier cubique
        """
        P0 ---------- P1
               \
                \
                 \
                  \
                   \
                    P2 ---------- P3
        """
        return (
            (1 - t) ** 3 * p0
            + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t**2 * p2
            + t**3 * p3
        )

    def interpolate_coordinates_acceleration(self, t):
        # Fonction d'interpolation avec accélération au début
        return t**2

    def interpolate_coordinates_constant(self, t):
        # Fonction d'interpolation constante
        return t

    def interpolate_coordinates_deceleration(self, t):
        # Fonction d'interpolation avec décélération à la fin
        return 1 - (1 - t) ** 2

    def interpolate_coordinates_from_center(
        self, absolute_coordinates, scale, smoothness
    ):
        diff_x = (
            (absolute_coordinates[0] - self.screen_x) * scale / self.pixel_increment
        )
        diff_y = (
            (absolute_coordinates[1] - self.screen_y) * scale / self.pixel_increment
        )
        length = int(
            math.dist(
                (0, 0),
                (diff_x, diff_y),
            ),
        )

        if length == 0:
            return

        unit_x = (diff_x / length) * self.pixel_increment
        unit_y = (diff_y / length) * self.pixel_increment

        x = y = sum_x = sum_y = 0

        # Divisez le mouvement en trois segments avec des points de contrôle spécifiques pour chaque segment
        for k in range(0, smoothness):
            t = k / smoothness

            if t < 0.3:
                eased_t = self.interpolate_coordinates_acceleration(
                    random.uniform(
                        0.2,
                        0.8,
                    )
                )
            elif t < 0.7:
                eased_t = self.interpolate_coordinates_constant(
                    random.uniform(
                        0.2,
                        0.8,
                    )
                )
            else:
                eased_t = self.interpolate_coordinates_deceleration(
                    random.uniform(
                        0.2,
                        0.8,
                    )
                )

            sum_x += x
            sum_y += y
            x, y = round(unit_x * eased_t - sum_x), round(unit_y * eased_t - sum_y)
            yield x, y

    def run(self):
        if torch.cuda.is_available():
            Console.print("[+] Cuda is available")

        print(f"Box: {self.detection_box}")
        collect_pause = 0

        while True:
            self.model.conf = float(dpg.get_value("aimbot_confidence"))
            self.model.iou = float(dpg.get_value("aimbot_iou"))
            self.pixel_increment = int(dpg.get_value("behaviours_increment"))

            self.fov = int(dpg.get_value("fov_value"))
            self.detection_box = {
                "left": int((self.screensize["X"] / 2) - (self.fov // 2)),
                "top": int((self.screensize["Y"] / 2) - (self.fov // 2)),
                "width": self.fov,
                "height": self.fov,
            }

            fr = np.array(self.screen.grab(self.detection_box))
            frame = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            frame_base = np.copy((frame))

            start_time = time.perf_counter()

            st = time.time()
            results = self.model(frame)
            print("model", (time.time() - st))

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
                        (relative_head_X, relative_head_Y),
                        (self.fov / 2, self.fov / 2),
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
                        cv2.rectangle(
                            frame,
                            x1y1,
                            x2y2,
                            (255, 0, 6),
                            2,
                        )
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
                        int(dpg.get_value("triggerbot_treshold")),
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
                        )
                    else:
                        cv2.putText(
                            frame,
                            "TARGETING",
                            (x1 + 40, y1),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (115, 113, 244),
                            1,
                        )

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

            if (
                bool(dpg.get_value("datacollect_enabled"))
                and time.perf_counter() - collect_pause > 1
                and self.is_targeted()
                and self.is_aimbot_enabled()
                and not player_in_frame
                and int(conf * 100) >= float(dpg.get_value("data_confidence"))
            ):
                if bool(
                    dpg.get_value("datacollect_require_lock")
                ) and not self.is_target_locked(absolute_head_X, absolute_head_Y):
                    continue

                cv2.imwrite(f"../assets/collected/{str(uuid.uuid4())}.jpg", frame_base)
                collect_pause = time.perf_counter()

            if cv2.waitKey(1) & 0xFF == ord("0"):
                break


if __name__ == "__main__":
    Configurator.check()

    Gui().start()
    Aimbot().run()
