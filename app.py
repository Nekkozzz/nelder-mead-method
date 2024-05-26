import customtkinter as ctk
from vector import Vector
from method import nelder_mead_method
import time as t
from threading import Thread
import math as m
import re


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.init_widgets()

        self.function_entry.insert(0, 'x1^2 + x1*x2 + x2^2 - 6*x1 - 9*x2')
        self.simplex_field.insert('0.0', '0, 0\n1, 0\n2, 1')
        self.iter_entry.insert(0, '20')
        self.eps_entry.insert(0, '1e-5')
        self.speed_entry.insert(0, '4')

    def init_widgets(self):
        self.title("NelderMead Viewer")
        self.geometry(f"{1200}x{900}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self, bg='white')
        self.canvas.bind('<Configure>', self.canvas.redraw)
        self.side_frame = ctk.CTkFrame(self)
        self.settings_frame = ctk.CTkFrame(self.side_frame)
        self.run_frame = ctk.CTkFrame(self.side_frame)
        self.result_frame = ctk.CTkFrame(self.side_frame)

        self.function_label = ctk.CTkLabel(self.settings_frame, text='Функция:')
        self.function_entry = ctk.CTkEntry(self.settings_frame)
        self.iter_label = ctk.CTkLabel(self.settings_frame, text='Кол-во итераций:')
        self.iter_entry = ctk.CTkEntry(self.settings_frame)
        self.eps_label = ctk.CTkLabel(self.settings_frame, text='Точность:')
        self.eps_entry = ctk.CTkEntry(self.settings_frame)
        self.simplex_label = ctk.CTkLabel(self.settings_frame, text='Симплекс:')
        self.simplex_checkbox = ctk.CTkCheckBox(self.settings_frame)
        self.simplex_field = ctk.CTkTextbox(self.settings_frame)
        self.speed_label = ctk.CTkLabel(self.run_frame, text='Скорость:')
        self.speed_entry = ctk.CTkEntry(self.run_frame, width=200)
        self.run_button = ctk.CTkButton(self.run_frame, text='Запустить', command=self.runner)
        self.clear_button = ctk.CTkButton(self.run_frame, text='Очистить', command=self.canvas.clear)
        self.result_label = ctk.CTkLabel(self.result_frame, text='Результат:', width=220)
        self.result_x_label = ctk.CTkLabel(self.result_frame, text='')
        self.result_f_label = ctk.CTkLabel(self.result_frame, text='')

        self.canvas.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.side_frame.grid(row=0, column=1, sticky='ns')
        self.settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        self.run_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='new')
        self.function_label.grid(row=0, column=0)
        self.function_entry.grid(row=1, column=0, padx=10, sticky='ew')
        self.simplex_label.grid(row=2, column=0)
        self.simplex_field.grid(row=3, column=0, padx=10, sticky='nsew')
        self.iter_label.grid(row=4, column=0)
        self.iter_entry.grid(row=5, column=0, padx=10, sticky='ew')
        self.eps_label.grid(row=6, column=0)
        self.eps_entry.grid(row=7, column=0, padx=10, pady=(0, 10), sticky='ew')
        self.speed_label.grid(row=0, column=0)
        self.speed_entry.grid(row=1, column=0, padx=10, sticky='ew')
        self.run_button.grid(row=2, column=0, pady=(10, 0))
        self.clear_button.grid(row=3, column=0, pady=10)
        self.result_label.grid(row=0, column=0)
        self.result_x_label.grid(row=1, column=0)
        self.result_f_label.grid(row=2, column=0)

    def runner(self): 
        Thread(target=self.run, daemon=True).start()

    def run(self):
        self.run_button.configure(state='disabled')
        self.result_frame.grid_forget()
        self.canvas.clear()
        f = self._parse_function(self.function_entry.get())
        simplex = self._parse_simplex(self.simplex_field.get('0.0', ctk.END))
        n = int(self.iter_entry.get())
        eps = float(self.eps_entry.get())
        speed = float(self.speed_entry.get())
        for points in nelder_mead_method(f, simplex, n, eps):
            self.canvas.add_points(points)
            t.sleep(1 / speed)
        x = points[0]
        self.result_x_label.configure(text=f'{"\n".join(f"x{i+1} = {x[i]}" for i in range(len(x)))}')
        self.result_f_label.configure(text=f'f(x) = {f(x)}')
        self.result_frame.grid(row=2, column=0, padx=10, sticky='new')
        self.run_button.configure(state='normal')

    def _parse_function(self, expr):
        res = re.sub(r'x(\d+)', lambda x: f'x[{int(x.group(1))-1}]', expr)
        for func in ['sin', 'cos', 'pi', 'sqrt', 'exp', 'log']:
            res = re.sub(func, f'm.{func}', res)
        res = re.sub(r'\^', '**', res)
        return lambda x: eval(res)

    def _parse_simplex(self, expr):
        points = [map(lambda x: float(x), line.split(',')) for line in expr.strip().split('\n')]
        return list(map(lambda x: Vector(*x), points))

class Canvas(ctk.CTkCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.points = set()
        self.history = []
        self.x_left = 50
        self.x_right = 20
        self.y_top = 20
        self.y_bottom = 40
        self.lb = Vector(0, 0)
        self.rt = Vector(1, 1)

    def add_points(self, points: list[Vector]):
        self.points.update(points)
        self.history.append(list(points))

        lb, rt = self.corner(min), self.corner(max)
        if self.lb != lb or self.rt != rt:
            self.lb, self.rt = lb, rt
            self.redraw('reset')
        else:
            self.redraw()

    def draw_tri(self, points: list[Vector], color):
        points = list(map(self.scale_point, points))
        self.create_polygon(*points, fill='', outline=color, width = 2)
        for point in points:
            self.create_oval(*(point - Vector(5, 5)), *(point + Vector(5, 5)), fill='white', outline=color, width=2)
        self.update()
    
    def corner(self, f):
        x = f(self.points, key=lambda v: v[0])[0]
        y = f(self.points, key=lambda v: v[1])[1]
        return Vector(x, y)

    def scale_point(self, point: Vector):
        return Vector(
            self.x_left + round((point[0] - self.lb[0]) * self.draw_width / (self.rt[0] - self.lb[0])),
            self.y_top + round((self.rt[1] - point[1]) * self.draw_height / (self.rt[1] - self.lb[1]))
        )
    
    def redraw(self, event=None):
        if len(self.history) == 0: return
        if event == 'reset':
            self.draw_width = self.winfo_width() - self.x_left - self.x_right
            self.draw_height = self.winfo_height() - self.y_top - self.y_bottom
            self.delete('all')
            self.redraw_axes()
            for step in self.history[:-1]:
                self.draw_tri(step, 'grey')
        elif len(self.history) > 1:
            self.draw_tri(self.history[-2], 'grey')
        self.draw_tri(self.history[-1], 'red')

    def redraw_axes(self):
        x_axis_pos = self.y_top + self.draw_height + 15
        y_axis_pos = self.x_left - 15
        self.create_line(0, x_axis_pos, self.winfo_width(), x_axis_pos)
        self.create_line(y_axis_pos, 0, y_axis_pos, self.winfo_width())
        for i in range(11):
            x_pos = self.x_left + i * self.draw_width / 10
            y_pos = self.y_top + i * self.draw_height / 10
            self.create_line(x_pos, x_axis_pos - 5, x_pos, x_axis_pos + 5)
            self.create_text(x_pos, x_axis_pos + 15, text=f'{round(self.lb[0] + (self.rt[0] - self.lb[0]) * i / 10, 3)}', anchor='c')
            self.create_line(y_axis_pos - 5, y_pos, y_axis_pos + 5, y_pos)
            self.create_text(y_axis_pos - 20, y_pos, text=f'{round(self.rt[1] - (self.rt[1] - self.lb[1]) * i / 10, 3)}', anchor='c')

    def clear(self):
        self.history.clear()
        self.points.clear()
        self.delete('all')

if __name__ == "__main__":
    app = App()
    app.mainloop()