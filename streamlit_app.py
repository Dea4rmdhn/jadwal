import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
from datetime import datetime
import time
from PIL import Image
import imageio


st.markdown("<h1 style='text-align: center; font-family:"Comic Sans MS"; font-style: italic;'>Jadwal Santuy Deak</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>TODAY'S TIME TABLE</p>", unsafe_allow_html=True)

#Create placeholder for the clock
clock_placeholder = st.empty()

def draw_clock():
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw outer circle
    circle = plt.Circle((0, 0), 1.2, color='black', fill=False)
    ax.add_artist(circle)
    
    # Add hour markers
    for hour in range(24):
        angle = (hour / 24) * 360
        x = np.cos(np.deg2rad(90 - angle))
        y = np.sin(np.deg2rad(90 - angle))
        if hour == 0:
            hour = 24
        ax.text(
            1.4 * x, 1.4 * y, f'{hour}',
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=12,
            fontfamily='Lucida Fax'
        )
        line_length = 0.95
        x_start = 1.16 * x  
        y_start = 1.16 * y 
        x_end = line_length * 1.3 * x
        y_end = line_length * 1.3 * y
        ax.plot([x_start, x_end], [y_start, y_end], color='black', linestyle='-', linewidth=0.8)

    circle2 = plt.Circle((0, 0), 1.17, color='black', fill=False)
    ax.add_artist(circle2)

    # Add schedule
    durasi_kegiatan = [4, 3, 1, 1, 6, 4, 3, 2]
    kegiatan = ['Scroll IG','Belajar','Mangan','Beberes', 'Turu','Scroll TT', 'Nonton Film', 'Free']
    warna = ['white'] * 8

    ukuran_pie = 0.6
    rotasi_pie = 135
    total = sum(durasi_kegiatan)
    angle_sekarang = rotasi_pie

    for durasi, color, label in zip(durasi_kegiatan, warna, kegiatan):
        theta1 = angle_sekarang
        theta2 = angle_sekarang + (durasi / total) * 360
        wedge = Wedge(center=(0, 0), r=ukuran_pie, theta1=theta1, theta2=theta2,
                      color=color, fill=False, edgecolor=color)
        ax.add_patch(wedge)
        
        mid_angle = (theta1 + theta2) / 2
        x = 1.1 * 0.75 * np.cos(np.deg2rad(mid_angle))
        y = 1.1 * 0.75 * np.sin(np.deg2rad(mid_angle))
        rotation_angle = (mid_angle - 180) % 360
        
        fontsizes = 8
        if durasi < 2:
            x = 0.95 * 0.9 * np.cos(np.deg2rad(mid_angle))
            y = 0.95 * 0.9 * np.sin(np.deg2rad(mid_angle))
            fontsizes = 6
        if label == 'Turu':
            rotation_angle += 160
            fontsizes = 11
            y = 0.8 * 0.75 * np.sin(np.deg2rad(mid_angle + 20))   
            y = 0.9 * 0.75 * np.sin(np.deg2rad(mid_angle - 30))
            try:
                # Baca gambar
                img = plt.imread('tai.gif')  # Ganti dengan path gambar Anda
                
                # Hitung posisi gambar
                img_size = 0.2  # Sesuaikan ukuran gambar
                x_img = 0.51 # Geser ke kanan nilai positif, ke kiri nilai negatif 
                y_img = 0.31 
                
                # Tambahkan gambar sebagai axes baru
                img_ax = fig.add_axes([x_img, y_img, img_size, img_size ])
                img_ax.imshow(img)
                img_ax.axis('off')

                img_ax.set_frame_on(False)  # Hilangkan frame
                img_ax.patch.set_alpha(0)

                img_ax.set_zorder(-2)
                
                # Sesuaikan posisi teks
                y = y - 0.1  # Geser teks ke bawah
                fontsizes = 11
                rotation_angle += 160
            except Exception as e:
                print(f"Error loading image: {e}")


        ax.text(
            x, y, label,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=fontsizes,
            weight='bold',
            color='black',
            rotation=rotation_angle,
            rotation_mode='anchor',
            fontfamily='Comic Sans MS'
        )
        

        x_start = 0.2 * np.cos(np.deg2rad(theta1))
        y_start = 0.2 * np.sin(np.deg2rad(theta1))
        x_end = 1.1 * np.cos(np.deg2rad(theta1))
        y_end = 1.1 * np.sin(np.deg2rad(theta1))

        ax.plot([x_start, x_end], [y_start, y_end], color='black', lw=1)

        x_start = 0.3 * np.cos(np.deg2rad(theta2))
        y_start = 0.3 * np.sin(np.deg2rad(theta2))
        x_end = 0.9 * np.cos(np.deg2rad(theta2))
        y_end = 0.9 * np.sin(np.deg2rad(theta2))
        
        ax.plot([x_start, x_end], [y_start, y_end], color='black', lw=1)
        
        angle_sekarang += (durasi / total) * 360

    # Get current time
    now = datetime.now()
    hour = now.hour % 12 + now.minute / 60
    minute = now.minute + now.second / 60
    second = now.second

    # Calculate angles
    hour_angle = (hour / 12) * 360
    minute_angle = (minute / 60) * 360
    second_angle = (second / 60) * 360

    # Draw clock hands
    hour_x = 0.7 * np.cos(np.deg2rad(90 - hour_angle))
    hour_y = 0.7 * np.sin(np.deg2rad(90 - hour_angle))
    ax.plot([0, hour_x], [0, hour_y], color='red', linewidth=6, zorder=5)

    minute_x = 0.9 * np.cos(np.deg2rad(90 - minute_angle))
    minute_y = 0.9 * np.sin(np.deg2rad(90 - minute_angle))
    ax.plot([0, minute_x], [0, minute_y], color='red', linewidth=4, zorder=5)

    second_x = 1.1 * np.cos(np.deg2rad(90 - second_angle))
    second_y = 1.1 * np.sin(np.deg2rad(90 - second_angle))
    ax.plot([0, second_x], [0, second_y], color='red', linewidth=2, zorder=5)

    # Add center circle
    edge = plt.Circle((0, 0), 0.127, color='black', fill=False, linewidth=0.5, zorder=6) 
    mulai = plt.Circle((0, 0), 0.127, color='yellow', fill=True, zorder=6)
    ax.add_artist(mulai)
    ax.add_artist(edge)

    ax.text(0, 0, 'PLAY', horizontalalignment='center', verticalalignment='center',
            fontsize=9, weight='bold', color='black', zorder=7)

    # Set plot properties
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Display the clock
    clock_placeholder.pyplot(fig)

# Run the clock
while True:
    draw_clock()
    time.sleep(1)
