import pygame as pg
from matrix_functions import *


class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.3
        self.rotation_speed = 0.015
        self.mouse_sensitivity = 0.001  # Adjust mouse sensitivity for rotation

        # Initialize angles for rotation
        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0

        # Lock the mouse to the center of the screen
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

    def control(self):
        key = pg.key.get_pressed()

        # Keyboard movement (WASD + QE for up and down)
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        # Mouse control for camera rotation
        mx, my = pg.mouse.get_rel()  # Get relative mouse movement since last call
        self.camera_yaw(-mx * self.mouse_sensitivity)  # Left-right movement controls yaw
        self.camera_pitch(-my * self.mouse_sensitivity)  # Up-down movement controls pitch

    def camera_yaw(self, angle):
        """Rotate around the Y axis (yaw)."""
        self.angleYaw += angle

    def camera_pitch(self, angle):
        """Rotate around the X axis (pitch), limit the pitch to avoid flipping."""
        max_pitch = math.pi / 2 - 0.01  # Prevent flipping over at vertical extremes
        self.anglePitch = max(-max_pitch, min(max_pitch, self.anglePitch + angle))

    def axiiIdentity(self):
        """Reset the camera's axis to default directions."""
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        """Update the camera's forward, right, and up vectors based on yaw and pitch."""
        # Apply rotation to the camera
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        self.axiiIdentity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        """Return the final camera matrix (translation + rotation)."""
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):
        """Generate the translation matrix for the camera's position."""
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        """Generate the rotation matrix based on the camera's orientation."""
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
