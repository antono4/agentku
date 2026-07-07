#!/usr/bin/env python3
"""
3D Dinosaur Animation - Fixed Version
Creates an animated scene with various dinosaurs
Output: MP4 video, 5 minutes duration
"""

import numpy as np
from PIL import Image, ImageDraw
import os
import math
from tqdm import tqdm

try:
    from moviepy import *
except ImportError:
    from moviepy.editor import ImageSequenceClip, concatenate_videoclips

# Animation settings
FPS = 24
DURATION = 300  # 5 minutes = 300 seconds
TOTAL_FRAMES = FPS * DURATION
FRAME_DIR = "/workspace/project/frames"
OUTPUT_FILE = "/workspace/project/dinosaur_animation.mp4"
WIDTH, HEIGHT = 1280, 720  # HD resolution for faster rendering

# Colors
GROUND_COLOR = (34, 139, 34)
MOUNTAIN_COLORS = [(139, 69, 19), (160, 82, 45), (210, 180, 140)]
TREE_COLORS = [(0, 100, 0), (34, 139, 34), (50, 205, 50)]

def setup_frame_directory():
    if not os.path.exists(FRAME_DIR):
        os.makedirs(FRAME_DIR)

def draw_sky(draw, frame_num):
    """Draw gradient sky with day/night cycle"""
    total_frames = FPS * 60
    cycle_pos = (frame_num % total_frames) / total_frames
    
    if cycle_pos < 0.25:
        t = cycle_pos / 0.25
        r = int(135 + (255 - 135) * t)
        g = int(206 + (200 - 206) * t)
        b = int(235 + (100 - 235) * t)
    elif cycle_pos < 0.5:
        r, g, b = 135, 206, 235
    elif cycle_pos < 0.75:
        t = (cycle_pos - 0.5) / 0.25
        r = int(135 + (255 - 135) * t)
        g = int(206 + (100 - 206) * t)
        b = int(235 + (80 - 235) * t)
    else:
        t = (cycle_pos - 0.75) / 0.25
        r = int(255 + (20 - 255) * t)
        g = int(100 + (30 - 100) * t)
        b = int(80 + (50 - 80) * t)
    
    for y in range(HEIGHT // 2):
        ratio = y / (HEIGHT // 2)
        cr = int(r + (255 - r) * ratio * 0.3)
        cg = int(g + (255 - g) * ratio * 0.3)
        cb = int(b + (255 - b) * ratio * 0.3)
        draw.line([(0, y), (WIDTH, y)], fill=(cr, cg, cb))
    
    draw.rectangle([(0, HEIGHT // 2), (WIDTH, HEIGHT)], fill=(r, g, b))
    
    sun_y = int(HEIGHT * 0.15 - math.sin(cycle_pos * 2 * math.pi) * HEIGHT * 0.1)
    sun_x = int(WIDTH * (0.2 + cycle_pos * 0.6))
    
    if cycle_pos < 0.75:
        for i in range(30, 0, -1):
            draw.ellipse([(sun_x - i, sun_y - i), (sun_x + i, sun_y + i)], fill=(255, 255, 0))
        draw.ellipse([(sun_x - 20, sun_y - 20), (sun_x + 20, sun_y + 20)], fill=(255, 220, 50))
    else:
        moon_x = int(WIDTH * 0.8)
        moon_y = int(HEIGHT * 0.15)
        for i in range(25, 0, -1):
            draw.ellipse([(moon_x - i, moon_y - i), (moon_x + i, moon_y + i)], fill=(255, 255, 220))
        draw.ellipse([(moon_x - 15, moon_y - 15), (moon_x + 15, moon_y + 15)], fill=(255, 255, 255))

def draw_mountains(draw):
    mountains = [
        ((0, HEIGHT//2), (WIDTH*0.15, HEIGHT*0.25), (WIDTH*0.3, HEIGHT//2)),
        ((WIDTH*0.2, HEIGHT//2), (WIDTH*0.35, HEIGHT*0.2), (WIDTH*0.5, HEIGHT//2)),
        ((WIDTH*0.4, HEIGHT//2), (WIDTH*0.55, HEIGHT*0.28), (WIDTH*0.7, HEIGHT//2)),
        ((WIDTH*0.6, HEIGHT//2), (WIDTH*0.8, HEIGHT*0.22), (WIDTH, HEIGHT//2)),
    ]
    for i, (p1, p2, p3) in enumerate(mountains):
        color = MOUNTAIN_COLORS[i % len(MOUNTAIN_COLORS)]
        draw.polygon([(int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (int(p3[0]), int(p3[1]))], fill=color)

def draw_trees(draw, x, y, scale=1.0):
    h = int(40 * scale)
    w = int(20 * scale)
    draw.rectangle([(int(x - w//4), int(y - h//2)), (int(x + w//4), int(y))], fill=(139, 69, 19))
    for i, color in enumerate([TREE_COLORS[0], TREE_COLORS[1], TREE_COLORS[2]]):
        layer_h = int(h * 0.4 * (1 - i * 0.2))
        layer_w = int(w * (1.5 - i * 0.3))
        draw.polygon([
            (int(x), int(y - h//2 - i * layer_h * 0.6 - layer_h)),
            (int(x - layer_w//2), int(y - h//2 - i * layer_h * 0.6)),
            (int(x + layer_w//2), int(y - h//2 - i * layer_h * 0.6))
        ], fill=color)

def draw_ground(draw):
    draw.rectangle([(0, int(HEIGHT * 0.65)), (WIDTH, HEIGHT)], fill=GROUND_COLOR)
    np.random.seed(42)
    for _ in range(150):
        x = np.random.randint(0, WIDTH)
        y = np.random.randint(int(HEIGHT * 0.65), HEIGHT)
        h = np.random.randint(5, 15)
        draw.line([(x, y), (x + np.random.randint(-3, 3), y - h)], fill=(50, np.random.randint(120, 180), 50), width=1)

def draw_tyrannosaurus(draw, x, y, scale=1.0, direction=1, action='walk', frame=0):
    s = scale * 100
    body_shifts = [(-3, -3), (-2, -2), (-1, -1), (0, 0)]
    for shift_x, shift_y in body_shifts:
        alpha = 1.0 - abs(shift_x) * 0.15
        color = (int(100 * alpha), int(50 * alpha), int(50 * alpha))
        draw.ellipse([(int(x - s*0.4 + shift_x), int(y - s*0.3 + shift_y)), 
                     (int(x + s*0.4 + shift_x), int(y + s*0.2 + shift_y))], fill=color)
    
    head_x = x + direction * s * 0.35
    head_y = y - s * 0.25
    draw.ellipse([(int(head_x - s*0.2), int(head_y - s*0.15)), 
                 (int(head_x + s*0.2), int(head_y + s*0.1))], fill=(120, 60, 60))
    
    jaw_open = 0.1 if action == 'roar' else 0.02
    draw.ellipse([(int(head_x - s*0.15), int(head_y + s*0.05)), 
                 (int(head_x + s*0.15), int(head_y + s*0.05 + s*jaw_open))], fill=(100, 50, 50))
    
    eye_x = head_x + direction * s * 0.08
    draw.ellipse([(int(eye_x - s*0.03), int(head_y - s*0.08)), 
                 (int(eye_x + s*0.03), int(head_y - s*0.02))], fill=(255, 255, 0))
    draw.ellipse([(int(eye_x - s*0.015), int(head_y - s*0.055)), 
                 (int(eye_x + s*0.015), int(head_y - s*0.025))], fill=(0, 0, 0))
    
    for i in range(5):
        tx = head_x - s*0.12 + i * s*0.05
        draw.polygon([(int(tx), int(head_y + s*0.02)), (int(tx + s*0.015), int(head_y + s*0.08)), 
                     (int(tx - s*0.015), int(head_y + s*0.08))], fill=(255, 255, 255))
    
    leg_phase = frame * 0.1
    leg_offset1 = math.sin(leg_phase) * 15 if action == 'walk' else 0
    leg_offset2 = math.sin(leg_phase + math.pi) * 15 if action == 'walk' else 0
    
    draw.ellipse([(int(x - s*0.25), int(y + s*0.15 + leg_offset1)), 
                 (int(x - s*0.05), int(y + s*0.45 + leg_offset1))], fill=(100, 50, 50))
    draw.ellipse([(int(x + s*0.05), int(y + s*0.15 + leg_offset2)), 
                 (int(x + s*0.25), int(y + s*0.45 + leg_offset2))], fill=(100, 50, 50))
    
    for i in range(10):
        t = i / 9
        tx = x - direction * s * (0.4 + t * 0.6)
        ty = y - s * 0.2 + s * 0.1 * math.sin(t * math.pi) - t * s * 0.1
        size = s * 0.15 * (1 - t * 0.7)
        draw.ellipse([(int(tx - size), int(ty - size)), (int(tx + size), int(ty + size))], 
                    fill=(int(100 - t * 20), int(50 - t * 10), int(50 - t * 10)))
    
    arm_x = head_x - direction * s * 0.15
    draw.line([(int(arm_x), int(head_y + s*0.05)), (int(arm_x + direction * s*0.1), int(head_y + s*0.15))], 
             fill=(100, 50, 50), width=int(s*0.05))

def draw_triceratops(draw, x, y, scale=1.0, direction=1, action='walk', frame=0):
    s = scale * 80
    for shift_x, shift_y in [(-2, -2), (-1, -1), (0, 0)]:
        alpha = 1.0 - abs(shift_x) * 0.15
        color = (int(80 * alpha), int(100 * alpha), int(60 * alpha))
        draw.ellipse([(int(x - s*0.5 + shift_x), int(y - s*0.3 + shift_y)), 
                     (int(x + s*0.5 + shift_x), int(y + s*0.2 + shift_y))], fill=color)
    
    frill_x = x - direction * s * 0.3
    frill_y = y - s * 0.3
    draw.ellipse([(int(frill_x - s*0.35), int(frill_y - s*0.25)), 
                 (int(frill_x + s*0.35), int(frill_y + s*0.15))], fill=(70, 90, 50))
    
    head_x = x - direction * s * 0.45
    head_y = y - s * 0.1
    draw.ellipse([(int(head_x - s*0.25), int(head_y - s*0.2)), 
                 (int(head_x + s*0.15), int(head_y + s*0.15))], fill=(90, 110, 70))
    
    for i in range(3):
        hx = head_x - direction * s * 0.1 + direction * i * s * 0.1
        hy = head_y - s * 0.25
        draw.line([(int(hx), int(hy)), (int(hx + direction * s * 0.05), int(hy - s * 0.3))], 
                 fill=(200, 200, 180), width=4)
    
    draw.line([(int(head_x - direction * s * 0.2), int(head_y)), 
              (int(head_x - direction * s * 0.25), int(head_y - s * 0.15))], 
             fill=(200, 200, 180), width=3)
    
    eye_x = head_x + direction * s * 0.1
    draw.ellipse([(int(eye_x - s*0.05), int(head_y - s*0.1)), 
                 (int(eye_x + s*0.05), int(head_y))], fill=(255, 255, 200))
    
    leg_phase = frame * 0.08
    for i, offset in enumerate([math.sin(leg_phase) * 10, math.sin(leg_phase + math.pi) * 10]):
        draw.ellipse([(int(x - s*0.3 + i*s*0.4), int(y + s*0.15 + offset)), 
                     (int(x - s*0.1 + i*s*0.4), int(y + s*0.4 + offset))], fill=(80, 100, 60))
    
    for i in range(8):
        t = i / 7
        tx = x + direction * s * (0.4 + t * 0.3)
        ty = y + s * 0.05 * math.sin(t * math.pi)
        size = s * 0.12 * (1 - t * 0.6)
        draw.ellipse([(int(tx - size), int(ty - size)), (int(tx + size), int(ty + size))], 
                    fill=(int(80 - t * 15), int(100 - t * 20), int(60 - t * 15)))

def draw_brachiosaurus(draw, x, y, scale=1.0, direction=1, action='walk', frame=0):
    s = scale * 60
    for shift_x, shift_y in [(-2, -2), (-1, -1), (0, 0)]:
        alpha = 1.0 - abs(shift_x) * 0.15
        color = (int(60 * alpha), int(90 * alpha), int(60 * alpha))
        draw.ellipse([(int(x - s*0.6 + shift_x), int(y - s*0.2 + shift_y)), 
                     (int(x + s*0.6 + shift_x), int(y + s*0.3 + shift_y))], fill=color)
    
    neck_segments = 12
    for i in range(neck_segments):
        t = i / (neck_segments - 1)
        nx = x - direction * s * (0.5 + t * 0.8)
        ny = y - s * 0.3 - t * s * 1.5
        neck_radius = s * 0.15 * (1 - t * 0.3)
        color = (int(60 - t * 20), int(90 - t * 30), int(60 - t * 20))
        draw.ellipse([(int(nx - neck_radius), int(ny - neck_radius)), 
                     (int(nx + neck_radius), int(ny + neck_radius))], fill=color)
    
    head_x = x - direction * s * 1.3
    head_y = y - s * 1.8
    draw.ellipse([(int(head_x - s*0.15), int(head_y - s*0.1)), 
                 (int(head_x + s*0.15), int(head_y + s*0.1))], fill=(50, 80, 50))
    
    eye_x = head_x + direction * s * 0.05
    draw.ellipse([(int(eye_x - s*0.03), int(head_y - s*0.05)), 
                 (int(eye_x + s*0.03), int(head_y + s*0.02))], fill=(255, 255, 200))
    
    leg_phase = frame * 0.06
    leg_offsets = [math.sin(leg_phase) * 5, math.sin(leg_phase + math.pi) * 5,
                   math.sin(leg_phase + 0.5) * 5, math.sin(leg_phase + math.pi + 0.5) * 5]
    
    for i, offset in enumerate(leg_offsets):
        lx = x - s*0.4 + i * s*0.25
        draw.rectangle([(int(lx - s*0.08), int(y + s*0.2 + offset)), 
                       (int(lx + s*0.08), int(y + s*0.7 + offset))], fill=(55, 85, 55))
    
    for i in range(15):
        t = i / 14
        tx = x + direction * s * (0.5 + t * 1.0)
        ty = y - s * 0.1 + s * 0.15 * math.sin(t * math.pi * 0.5)
        size = s * 0.15 * (1 - t * 0.8)
        draw.ellipse([(int(tx - size), int(ty - size)), (int(tx + size), int(ty + size))], 
                    fill=(55, 85, 55))

def draw_velociraptor(draw, x, y, scale=1.0, direction=1, action='walk', frame=0):
    s = scale * 50
    for shift_x, shift_y in [(-1, -1), (0, 0)]:
        alpha = 1.0 - abs(shift_x) * 0.2
        color = (int(150 * alpha), int(100 * alpha), int(50 * alpha))
        draw.ellipse([(int(x - s*0.35 + shift_x), int(y - s*0.25 + shift_y)), 
                     (int(x + s*0.35 + shift_x), int(y + s*0.15 + shift_y))], fill=color)
    
    head_x = x - direction * s * 0.4
    head_y = y - s * 0.15
    draw.ellipse([(int(head_x - s*0.25), int(head_y - s*0.1)), 
                 (int(head_x + s*0.1), int(head_y + s*0.08))], fill=(170, 110, 60))
    
    eye_x = head_x + direction * s * 0.05
    draw.ellipse([(int(eye_x - s*0.05), int(head_y - s*0.06)), 
                 (int(eye_x + s*0.05), int(head_y + s*0.02))], fill=(255, 200, 0))
    draw.ellipse([(int(eye_x - s*0.02), int(head_y - s*0.03)), 
                 (int(eye_x + s*0.02), int(head_y))], fill=(0, 0, 0))
    
    for i in range(4):
        tx = head_x - s*0.2 + i * s*0.06
        draw.polygon([(int(tx), int(head_y + s*0.03)), (int(tx + s*0.02), int(head_y + s*0.1)), 
                     (int(tx - s*0.02), int(head_y + s*0.1))], fill=(255, 255, 255))
    
    for i in range(3):
        fx = head_x - direction * s * 0.1 + i * direction * s * 0.05
        fy = head_y - s * 0.12
        draw.polygon([(int(fx), int(fy + s*0.08)), (int(fx + direction * s*0.03), int(fy - s*0.05)), 
                     (int(fx - direction * s*0.03), int(fy - s*0.05))], fill=(120, 80, 40))
    
    leg_phase = frame * 0.2
    if action == 'run':
        leg_phase *= 1.5
    
    for i, phase in enumerate([leg_phase, leg_phase + math.pi]):
        offset = math.sin(phase) * 15 if action == 'walk' else math.sin(phase) * 20
        lx = x - s*0.2 + i * s*0.35
        draw.line([(int(lx), int(y + s*0.1)), (int(lx + direction * s*0.1), int(y + s*0.3 + offset))], 
                 fill=(140, 90, 50), width=4)
        draw.polygon([(int(lx + direction * s*0.1), int(y + s*0.3 + offset)),
                     (int(lx + direction * s*0.15), int(y + s*0.35 + offset)),
                     (int(lx + direction * s*0.08), int(y + s*0.38 + offset))], 
                    fill=(100, 70, 40))
    
    for i in range(12):
        t = i / 11
        tx = x + direction * s * (0.3 + t * 0.7)
        ty = y - s * 0.15 + s * 0.1 * math.sin(t * math.pi)
        size = s * 0.1 * (1 - t * 0.7)
        draw.ellipse([(int(tx - size), int(ty - size)), (int(tx + size), int(ty + size))], 
                    fill=(int(140 - t * 30), int(90 - t * 20), int(50 - t * 15)))
    
    arm_x = head_x + direction * s * 0.15
    draw.line([(int(arm_x), int(head_y + s*0.05)), (int(arm_x + direction * s*0.15), int(head_y + s*0.15))], 
             fill=(140, 90, 50), width=3)

def draw_pteranodon(draw, x, y, scale=1.0, direction=1, frame=0):
    s = scale * 40
    wing_angle = math.sin(frame * 0.15) * 0.4
    y_offset = math.sin(frame * 0.1) * 5
    
    draw.ellipse([(int(x - s*0.3), int(y + y_offset - s*0.1)), 
                 (int(x + s*0.3), int(y + y_offset + s*0.1))], fill=(180, 150, 120))
    
    head_x = x - direction * s * 0.35
    draw.ellipse([(int(head_x - s*0.2), int(y + y_offset - s*0.08)), 
                 (int(head_x + s*0.15), int(y + y_offset + s*0.08))], fill=(190, 160, 130))
    
    crest_x = head_x - direction * s * 0.1
    draw.polygon([(int(crest_x), int(y + y_offset + s*0.05)), 
                 (int(crest_x - direction * s*0.4), int(y + y_offset - s*0.2)),
                 (int(crest_x - direction * s*0.2), int(y + y_offset + s*0.1))], 
                fill=(200, 170, 140))
    
    draw.polygon([(int(head_x + s*0.1), int(y + y_offset)), 
                 (int(head_x + s*0.35), int(y + y_offset + s*0.02)),
                 (int(head_x + s*0.1), int(y + y_offset + s*0.04))], 
                fill=(220, 180, 100))
    
    eye_x = head_x + direction * s * 0.05
    draw.ellipse([(int(eye_x - s*0.03), int(y + y_offset - s*0.04)), 
                 (int(eye_x + s*0.03), int(y + y_offset + s*0.02))], fill=(0, 0, 0))
    
    wing_span = s * 1.5
    for side in [1, -1]:
        points = [(int(x), int(y + y_offset))]
        segments = 8
        for i in range(segments + 1):
            t = i / segments
            wx = x + side * wing_span * t
            wy = y + y_offset + wing_angle * side * wing_span * t * 0.3 * (1 - t * 0.5)
            points.append((int(wx), int(wy)))
        draw.polygon(points, fill=(160, 130, 100))
        
        for i in range(4):
            t = (i + 1) / 5
            wx1 = x + side * wing_span * (t - 0.1)
            wy1 = y + y_offset + wing_angle * side * wing_span * (t - 0.1) * 0.3 * (1 - (t - 0.1) * 0.5)
            wx2 = x + side * wing_span * t
            wy2 = y + y_offset + wing_angle * side * wing_span * t * 0.3 * (1 - t * 0.5)
            draw.line([(int(wx1), int(wy1)), (int(wx2), int(wy2))], fill=(100, 80, 60), width=2)
    
    for i, offset in enumerate([-8, 8]):
        draw.line([(int(x + offset), int(y + y_offset + s*0.1)), 
                  (int(x + offset), int(y + y_offset + s*0.25))], 
                 fill=(150, 120, 90), width=2)

def draw_stegosaurus(draw, x, y, scale=1.0, direction=1, action='walk', frame=0):
    s = scale * 70
    for shift_x, shift_y in [(-2, -2), (-1, -1), (0, 0)]:
        alpha = 1.0 - abs(shift_x) * 0.15
        color = (int(70 * alpha), int(100 * alpha), int(50 * alpha))
        draw.ellipse([(int(x - s*0.5 + shift_x), int(y - s*0.2 + shift_y)), 
                     (int(x + s*0.5 + shift_x), int(y + s*0.25 + shift_y))], fill=color)
    
    for i in range(8):
        t = i / 7
        px = x - direction * s * (0.3 - t * 0.7)
        py = y - s * 0.25 - s * 0.15 * math.sin(t * math.pi)
        plate_size = s * 0.15 * (1 - abs(t - 0.5) * 0.5)
        for shift in [(-1, -1), (0, 0)]:
            alpha = 1.0 - abs(shift[0]) * 0.2
            color = (int(180 * alpha), int(80 * alpha), int(60 * alpha))
            draw.polygon([(int(px), int(py - plate_size*1.5)), 
                         (int(px - plate_size), int(py + plate_size*0.5)),
                         (int(px + plate_size), int(py + plate_size*0.5))], fill=color)
    
    head_x = x - direction * s * 0.55
    head_y = y - s * 0.05
    draw.ellipse([(int(head_x - s*0.15), int(head_y - s*0.1)), 
                 (int(head_x + s*0.1), int(head_y + s*0.08))], fill=(60, 90, 40))
    
    eye_x = head_x + direction * s * 0.05
    draw.ellipse([(int(eye_x - s*0.03), int(head_y - s*0.05)), 
                 (int(eye_x + s*0.03), int(head_y))], fill=(255, 255, 200))
    
    leg_phase = frame * 0.07
    for i, offset in enumerate([math.sin(leg_phase) * 8, math.sin(leg_phase + math.pi) * 8]):
        draw.ellipse([(int(x - s*0.35 + i*s*0.5), int(y + s*0.2 + offset)), 
                     (int(x - s*0.15 + i*s*0.5), int(y + s*0.45 + offset))], fill=(65, 95, 45))
    
    for i in range(6):
        t = i / 5
        tx = x + direction * s * (0.4 + t * 0.5)
        ty = y + s * 0.05 * math.sin(t * math.pi)
        size = s * 0.1 * (1 - t * 0.5)
        draw.ellipse([(int(tx - size), int(ty - size)), (int(tx + size), int(ty + size))], 
                    fill=(65, 95, 45))
        if i > 2:
            spike_x = tx + direction * s * 0.08
            spike_y = ty - s * 0.15
            draw.polygon([(int(spike_x), int(spike_y + s*0.15)), 
                         (int(spike_x - s*0.04), int(spike_y - s*0.15)),
                         (int(spike_x + s*0.04), int(spike_y - s*0.15))], 
                        fill=(150, 60, 40))

def add_particles(draw, frame_num):
    np.random.seed(frame_num // 10)
    for _ in range(20):
        x = np.random.randint(0, WIDTH)
        y = np.random.randint(int(HEIGHT * 0.3), int(HEIGHT * 0.7))
        size = np.random.randint(1, 3)
        draw.ellipse([(x, y), (x + size, y + size)], fill=(200, 200, 180))

def create_scene(scene_num, frame_num):
    img = Image.new('RGB', (WIDTH, HEIGHT), (135, 206, 235))
    draw = ImageDraw.Draw(img)
    
    draw_sky(draw, frame_num)
    draw_mountains(draw)
    draw_ground(draw)
    
    np.random.seed(scene_num * 1000 + frame_num // 100)
    for _ in range(6):
        tx = np.random.randint(50, WIDTH - 50)
        ty = int(HEIGHT * 0.65) + np.random.randint(-20, 40)
        scale = np.random.uniform(0.5, 1.0)
        draw_trees(draw, tx, ty, scale)
    
    add_particles(draw, frame_num)
    
    center_y = int(HEIGHT * 0.72)
    
    if scene_num == 0:
        draw_tyrannosaurus(draw, WIDTH * 0.3, center_y, scale=1.2, direction=1, action='walk', frame=frame_num)
        draw_triceratops(draw, WIDTH * 0.7, center_y + 30, scale=0.9, direction=-1, action='walk', frame=frame_num)
    elif scene_num == 1:
        for i in range(4):
            bx = WIDTH * (0.2 + i * 0.2)
            by = center_y - i * 35
            draw_brachiosaurus(draw, bx, by, scale=0.9 - i * 0.1, direction=1, action='walk', frame=frame_num + i * 20)
    elif scene_num == 2:
        for i in range(5):
            rx = WIDTH * (0.15 + i * 0.18)
            ry = center_y + math.sin(i * 0.8 + frame_num * 0.05) * 25
            draw_velociraptor(draw, rx, ry, scale=0.7, direction=1, action='run', frame=frame_num + i * 15)
    elif scene_num == 3:
        for i in range(6):
            px = (WIDTH * 0.1 + i * WIDTH * 0.15 + frame_num * (1 + i * 0.2)) % (WIDTH + 200) - 100
            py = HEIGHT * (0.25 + 0.1 * math.sin(i + frame_num * 0.02))
            draw_pteranodon(draw, px, py, scale=0.8, direction=1 if (px < WIDTH/2) else -1, frame=frame_num + i * 30)
    elif scene_num == 4:
        draw_stegosaurus(draw, WIDTH * 0.5, center_y, scale=1.0, direction=1, action='walk', frame=frame_num)
        for i in range(2):
            sx = WIDTH * (0.3 - i * 0.25)
            sy = center_y + 35
            draw_stegosaurus(draw, sx, sy, scale=0.6, direction=1, action='walk', frame=frame_num + i * 30)
    elif scene_num == 5:
        draw_tyrannosaurus(draw, WIDTH * 0.25, center_y, scale=1.0, direction=1, action='roar', frame=frame_num)
        draw_brachiosaurus(draw, WIDTH * 0.5, center_y + 20, scale=0.8, direction=-1, action='walk', frame=frame_num)
        draw_triceratops(draw, WIDTH * 0.75, center_y + 10, scale=0.85, direction=-1, action='walk', frame=frame_num)
        draw_pteranodon(draw, WIDTH * 0.4, HEIGHT * 0.3, scale=0.6, direction=1, frame=frame_num)
        draw_pteranodon(draw, WIDTH * 0.6, HEIGHT * 0.25, scale=0.5, direction=-1, frame=frame_num + 20)
    
    return img

def create_video():
    print("Creating video from frames...")
    frame_files = sorted([f"{FRAME_DIR}/{f}" for f in os.listdir(FRAME_DIR) if f.endswith('.png')])
    
    try:
        clip = ImageSequenceClip(frame_files, fps=FPS)
        clip.write_videofile(OUTPUT_FILE, codec='libx264', audio=False, logger=None)
    except TypeError:
        clip = ImageSequenceClip(frame_files, fps=FPS)
        clip.write_videofile(OUTPUT_FILE, codec='libx264', audio=False, verbose=False)
    
    print(f"Video saved to: {OUTPUT_FILE}")

def main():
    print("=" * 60)
    print("3D Dinosaur Animation Generator")
    print("=" * 60)
    print(f"Duration: {DURATION} seconds ({DURATION/60:.1f} minutes)")
    print(f"Frame rate: {FPS} FPS")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    print(f"Total frames: {TOTAL_FRAMES}")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)
    
    setup_frame_directory()
    
    scenes = [(0, FPS * 50), (FPS * 50, FPS * 100), (FPS * 100, FPS * 150),
              (FPS * 150, FPS * 200), (FPS * 200, FPS * 250), (FPS * 250, FPS * 300)]
    scene_names = ["T-Rex Hunting", "Brachiosaurus Herd", "Velociraptor Pack", 
                   "Pteranodon Flight", "Stegosaurus Family", "Peaceful Valley"]
    
    print("\nRendering frames...")
    print("-" * 40)
    
    for idx, (start, end) in enumerate(scenes):
        print(f"\nScene {idx+1}: {scene_names[idx]}")
        for frame_num in tqdm(range(start, end)):
            img = create_scene(idx, frame_num)
            img.save(f"{FRAME_DIR}/frame_{frame_num:06d}.png", "PNG")
    
    print("\n" + "-" * 40)
    print("All frames rendered successfully!")
    
    print("\nCreating video...")
    create_video()
    
    print("\nCleaning up frames...")
    for f in os.listdir(FRAME_DIR):
        os.remove(f"{FRAME_DIR}/{f}")
    os.rmdir(FRAME_DIR)
    
    print("\n" + "=" * 60)
    print("Animation complete!")
    print(f"Output file: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()
