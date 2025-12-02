import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy

class Diamond3D:
    """
    A class to create and manipulate a 3D diamond shape.
    Supports scaling, rotation, reflection, and translation transformations.
    """

    def __init__(self):
        
        # Diamond vertices (8 points forming a diamond/octahedron shape)
        self.vertices_original = np.array([
            [0, 0, 1],      # Top vertex (0)
            [1, 0, 0],      # Right vertex (1)
            [0, 1, 0],      # Front vertex (2)
            [-1, 0, 0],     # Left vertex (3)
            [0, -1, 0],     # Back vertex (4)
            [0, 0, -1]      # Bottom vertex (5)
        ])

        # A copy to apply transformations 
        self.vertices = copy.deepcopy(self.vertices_original)

        # faces of the diamond (triangles connecting vertices)
        self.faces = [
            [0, 1, 2],  # Top-right-front
            [0, 2, 3],  # Top-front-left
            [0, 3, 4],  # Top-left-back
            [0, 4, 1],  # Top-back-right
            [5, 2, 1],  # Bottom-front-right
            [5, 3, 2],  # Bottom-left-front
            [5, 4, 3],  # Bottom-back-left
            [5, 1, 4]   # Bottom-right-back
        ]

    def reset(self):
        """Reset to original diamond"""
        self.vertices = copy.deepcopy(self.vertices_original)
        return self

    def scale(self, factor):
        """Scale the diamond by a factor"""
        self.vertices = self.vertices * factor
        return self

    def translate(self, tx, ty, tz):
        """Translate (move) the diamond"""
        translation_matrix = np.array([tx, ty, tz])
        self.vertices = self.vertices + translation_matrix
        return self

    def rotate_x(self, angle_degrees):
        """Rotate around X-axis"""
        angle_rad = np.radians(angle_degrees)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle_rad), -np.sin(angle_rad)],
            [0, np.sin(angle_rad), np.cos(angle_rad)]
        ])
        self.vertices = self.vertices @ rotation_matrix.T
        return self

    def rotate_y(self, angle_degrees):
        """Rotate around Y-axis"""
        angle_rad = np.radians(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)]
        ])
        self.vertices = self.vertices @ rotation_matrix.T
        return self

    def rotate_z(self, angle_degrees):
        """Rotate around Z-axis"""
        angle_rad = np.radians(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1]
        ])
        self.vertices = self.vertices @ rotation_matrix.T
        return self

    def reflect_x(self):
        """Reflect across X-axis (YZ plane)"""
        reflection_matrix = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        self.vertices = self.vertices @ reflection_matrix.T
        return self

    def reflect_y(self):
        """Reflect across Y-axis (XZ plane)"""
        reflection_matrix = np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ])
        self.vertices = self.vertices @ reflection_matrix.T
        return self

    def reflect_z(self):
        """Reflect across Z-axis (XY plane)"""
        reflection_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, -1]
        ])
        self.vertices = self.vertices @ reflection_matrix.T
        return self

    def get_plot(self, title="3D Diamond"):
        """Return matplotlib figure with the 3D diamond"""
        fig = plt.Figure(figsize=(8, 7), dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        #  polygon collection from faces
        diamond_faces = []
        for face in self.faces:
            diamond_faces.append(self.vertices[face])

        #  and add the 3D polygon collection
        face_collection = Poly3DCollection(diamond_faces, alpha=0.7, linewidths=1, edgecolors='black')
        face_collection.set_facecolor('cyan')
        ax.add_collection3d(face_collection)

        # labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title, fontsize=12, fontweight='bold')

        # equal aspect ratio
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_zlim([-3, 3])

        return fig


class DiamondGUI:
    """Interactive GUI for 3D Diamond transformations"""

    def __init__(self, root):
        self.root = root
        self.root.title("3D Diamond Transformation Tool")
        self.root.geometry("1000x800")

        # Initialize diamond
        self.diamond = Diamond3D()
        self.canvas = None

        #  GUI elements
        self.create_widgets()
        self.update_plot()

    def create_widgets(self):
        """all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel for controls
        control_frame = ttk.LabelFrame(main_frame, text="Transformations", width=250)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

        # Scale controls
        scale_label = ttk.Label(control_frame, text="Scale Factor:")
        scale_label.pack()
        self.scale_var = tk.DoubleVar(value=1.0)
        scale_slider = ttk.Scale(control_frame, from_=0.1, to=3.0, variable=self.scale_var, orient=tk.HORIZONTAL)
        scale_slider.pack(fill=tk.X, padx=5, pady=2)
        self.scale_value = ttk.Label(control_frame, text="1.0")
        self.scale_value.pack()
        scale_slider.config(command=self.update_scale_display)

        ttk.Button(control_frame, text="Apply Scale", command=self.apply_scale).pack(fill=tk.X, padx=5, pady=5)

        # Rotation X
        ttk.Label(control_frame, text="Rotate X (degrees):").pack()
        self.rot_x_var = tk.DoubleVar(value=0)
        rot_x_spin = ttk.Spinbox(control_frame, from_=-360, to=360, textvariable=self.rot_x_var, width=10)
        rot_x_spin.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(control_frame, text="Apply Rotate X", command=self.apply_rotate_x).pack(fill=tk.X, padx=5, pady=5)

        # Rotation Y
        ttk.Label(control_frame, text="Rotate Y (degrees):").pack()
        self.rot_y_var = tk.DoubleVar(value=0)
        rot_y_spin = ttk.Spinbox(control_frame, from_=-360, to=360, textvariable=self.rot_y_var, width=10)
        rot_y_spin.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(control_frame, text="Apply Rotate Y", command=self.apply_rotate_y).pack(fill=tk.X, padx=5, pady=5)

        # Rotation Z
        ttk.Label(control_frame, text="Rotate Z (degrees):").pack()
        self.rot_z_var = tk.DoubleVar(value=0)
        rot_z_spin = ttk.Spinbox(control_frame, from_=-360, to=360, textvariable=self.rot_z_var, width=10)
        rot_z_spin.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(control_frame, text="Apply Rotate Z", command=self.apply_rotate_z).pack(fill=tk.X, padx=5, pady=5)

        # Translation
        ttk.Label(control_frame, text="Translate X:").pack()
        self.trans_x_var = tk.DoubleVar(value=0)
        ttk.Spinbox(control_frame, from_=-5, to=5, textvariable=self.trans_x_var, width=10).pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(control_frame, text="Translate Y:").pack()
        self.trans_y_var = tk.DoubleVar(value=0)
        ttk.Spinbox(control_frame, from_=-5, to=5, textvariable=self.trans_y_var, width=10).pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(control_frame, text="Translate Z:").pack()
        self.trans_z_var = tk.DoubleVar(value=0)
        ttk.Spinbox(control_frame, from_=-5, to=5, textvariable=self.trans_z_var, width=10).pack(fill=tk.X, padx=5, pady=2)

        ttk.Button(control_frame, text="Apply Translation", command=self.apply_translation).pack(fill=tk.X, padx=5, pady=5)

        # Reflections
        ttk.Label(control_frame, text="Reflections:").pack(pady=10)
        ttk.Button(control_frame, text="Reflect X", command=self.apply_reflect_x).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(control_frame, text="Reflect Y", command=self.apply_reflect_y).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(control_frame, text="Reflect Z", command=self.apply_reflect_z).pack(fill=tk.X, padx=5, pady=2)

        # Reset button
        ttk.Button(control_frame, text="RESET", command=self.reset_diamond).pack(fill=tk.X, padx=5, pady=10, ipadx=5)

        # Right panel for plot
        plot_frame = ttk.LabelFrame(main_frame, text="3D View")
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.plot_canvas_frame = ttk.Frame(plot_frame)
        self.plot_canvas_frame.pack(fill=tk.BOTH, expand=True)

    def update_scale_display(self, value):
        """Update scale display label"""
        self.scale_value.config(text=f"{float(value):.2f}")

    def apply_scale(self):
        """Apply scale transformation"""
        factor = self.scale_var.get()
        self.diamond.scale(factor)
        self.update_plot()

    def apply_rotate_x(self):
        """Apply X rotation"""
        angle = self.rot_x_var.get()
        self.diamond.rotate_x(angle)
        self.update_plot()
        self.rot_x_var.set(0)

    def apply_rotate_y(self):
        """Apply Y rotation"""
        angle = self.rot_y_var.get()
        self.diamond.rotate_y(angle)
        self.update_plot()
        self.rot_y_var.set(0)

    def apply_rotate_z(self):
        """Apply Z rotation"""
        angle = self.rot_z_var.get()
        self.diamond.rotate_z(angle)
        self.update_plot()
        self.rot_z_var.set(0)

    def apply_translation(self):
        """Apply translation"""
        tx = self.trans_x_var.get()
        ty = self.trans_y_var.get()
        tz = self.trans_z_var.get()
        self.diamond.translate(tx, ty, tz)
        self.update_plot()

    def apply_reflect_x(self):
        """Apply X reflection"""
        self.diamond.reflect_x()
        self.update_plot()

    def apply_reflect_y(self):
        """Apply Y reflection"""
        self.diamond.reflect_y()
        self.update_plot()

    def apply_reflect_z(self):
        """Apply Z reflection"""
        self.diamond.reflect_z()
        self.update_plot()

    def reset_diamond(self):
        """Reset to original diamond"""
        self.diamond.reset()
        self.scale_var.set(1.0)
        self.rot_x_var.set(0)
        self.rot_y_var.set(0)
        self.rot_z_var.set(0)
        self.trans_x_var.set(0)
        self.trans_y_var.set(0)
        self.trans_z_var.set(0)
        self.update_plot()

    def update_plot(self):
        """Update the 3D plot"""
        # Clear old canvas
        for widget in self.plot_canvas_frame.winfo_children():
            widget.destroy()

        #  new figure
        fig = self.diamond.get_plot("3D Diamond Transformation")

        #  canvas
        canvas = FigureCanvasTkAgg(fig, master=self.plot_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas = canvas


def main():
    """Main function to run the application"""
    root = tk.Tk()
    gui = DiamondGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
