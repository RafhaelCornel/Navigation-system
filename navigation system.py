# ============================================================================
# CAMPUS NAVIGATION SYSTEM
# ============================================================================
# A Tkinter-based GUI for exploring campus buildings, departments, and facilities
# with interactive map, search functionality, and detailed building information.
# ============================================================================

import tkinter as tk
from tkinter import messagebox
import re
import subprocess
import sys
import os
import random
import json

# Global login state
LOGIN_SUCCESS = False
LOGIN_EMAIL = None

# ============================================================================
# PHASE 1: LOGIN SCREEN
# ============================================================================

def login():
	"""
	Display login screen and validate Pillow availability.
	Proceeds to map UI only when user clicks Explore and Pillow is available.
	"""
	global LOGIN_SUCCESS, LOGIN_EMAIL

	# Check if Pillow is installed
	pil_available = _check_pillow_available()
	
	if not pil_available:
		if not _prompt_pillow_installation():
			return
	
	# Login successful — proceed to map
	LOGIN_SUCCESS = True
	LOGIN_EMAIL = "Student"
	_close_login_window()


def _check_pillow_available():
	"""Check if Pillow (PIL) module is installed."""
	try:
		import PIL  # noqa: F401
		return True
	except Exception:
		return False


def _prompt_pillow_installation():
	"""Prompt user to install Pillow and handle installation."""
	result = messagebox.askyesno(
		"Pillow Required",
		"Pillow (PIL) is required to use the campus map.\n\n"
		"Do you want to install it now?"
	)
	
	if not result:
		messagebox.showwarning(
			"Pillow Required",
			"Pillow is required to use the map. Installation cancelled."
		)
		return False
	
	# Attempt installation
	try:
		messagebox.showinfo("Installing", "Please wait while Pillow is being installed...")
		subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
		messagebox.showinfo("Installed", "Pillow installed successfully!")
		return True
	except Exception:
		messagebox.showerror(
			"Install Failed",
			"Could not install Pillow. Check Internet Connection or install manually."
		)
		return False


def _close_login_window():
	"""Withdraw and close the login window to proceed to map UI."""
	try:
		window.withdraw()
	except Exception:
		pass
	try:
		window.quit()
	except Exception:
		pass

# ============================================================================
# LOGIN WINDOW SETUP
# ============================================================================

window = tk.Tk()
window.title("Campus Navigation")
window.geometry("1000x800")
window.configure(bg="#f5f5f5")

# Main card container
center_frame = tk.Frame(window, bg="#FFF9E6")
center_frame.pack(expand=True, fill=tk.BOTH)

card = tk.Frame(
	center_frame, 
	bg="#FFF9E6", 
	bd=0, 
	highlightthickness=1, 
	highlightbackground="#e6e6e6"
)
card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.995, relheight=0.98)

# Accent stripe at top
accent = tk.Frame(card, bg="#ffd000", height=10)
accent.pack(fill=tk.X, side=tk.TOP)

# Content area with padding
content = tk.Frame(card, bg="#FFF9E6")
content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

# Centered content block
centered_block = tk.Frame(content, bg="#FFF9E6")
centered_block.place(relx=0.5, rely=0.5, anchor="center")

# Logo rendering
logo_label = tk.Label(centered_block, bg="#FFF9E6")
logo_label.pack(pady=(8, 12))


def _render_logo():
	"""Render logo using Pillow (PIL) with fallback to tkinter PhotoImage."""
	_render_logo_with_pillow()
	if logo_label.cget("image") == "":
		_render_logo_with_photoimage()
	if logo_label.cget("image") == "":
		_render_logo_fallback()


def _render_logo_with_pillow():
	"""Try to render logo using Pillow for high quality."""
	try:
		from PIL import Image, ImageTk
		logo_path = os.path.join(os.path.dirname(__file__), "phinma-logo.png")
		if os.path.exists(logo_path):
			target_size = 260
			im = Image.open(logo_path)
			w0, h0 = im.size
			scale = min(target_size / w0, target_size / h0)
			new_w = max(1, int(w0 * scale))
			new_h = max(1, int(h0 * scale))
			im2 = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
			photo = ImageTk.PhotoImage(im2)
			logo_label.image = photo
			logo_label.config(image=photo, text="")
	except Exception:
		pass


def _render_logo_with_photoimage():
	"""Try to render logo using tkinter PhotoImage."""
	try:
		logo_path = os.path.join(os.path.dirname(__file__), "phinma-logo.png")
		if os.path.exists(logo_path):
			img = tk.PhotoImage(file=logo_path)
			target_size = 260
			sx = max(1, int(img.width() / target_size))
			sy = max(1, int(img.height() / target_size))
			subsample = max(sx, sy)
			if subsample > 1:
				img = img.subsample(subsample, subsample)
			logo_label.image = img
			logo_label.config(image=img, text="")
	except Exception:
		pass


def _render_logo_fallback():
	"""Render logo as fallback text."""
	logo_label.config(
		image="", 
		text="PHINMA", 
		font=("Arial", 26, "bold"), 
		fg="#526240", 
		bg="#FFF9E6"
	)

# Render logo and bind to layout changes
content.after(50, _render_logo)
content.bind("<Configure>", lambda e: _render_logo())

# Login UI elements
title_label = tk.Label(
	centered_block, 
	text="Campus Navigation System", 
	font=("Arial", 28, "bold"),
	bg="#FFF9E6", 
	fg="#526240"
)
title_label.pack(pady=(6, 8))

subtitle_label = tk.Label(
	centered_block,
	text="Helping Students Find Their Way—Making Lives Better\nThrough Navigation",
	font=("Arial", 18, "italic"), 
	fg="#526240", 
	bg="#FFF9E6", 
	justify=tk.CENTER
)
subtitle_label.pack(pady=(0, 14))

explore_btn = tk.Button(
	centered_block, 
	text="🌍  Explore", 
	command=login,
	bg="#3a4f24", 
	fg="#ffffff",
	activebackground="#33501e", 
	activeforeground="#ffffff",
	font=("Arial", 20, "bold"), 
	bd=0, 
	relief=tk.FLAT,
	padx=36, 
	pady=14
)
explore_btn.pack(pady=(6, 6))

caption_label = tk.Label(
	centered_block, 
	text="Start exploring the campus map", 
	font=("Arial", 11),
	fg="#8a8a88", 
	bg="#FFF9E6"
)
caption_label.pack(pady=(6, 0))

# Login window close handler
def _on_login_close():
	"""Handle login window close event."""
	window.destroy()

window.protocol("WM_DELETE_WINDOW", _on_login_close)
window.mainloop()

# ============================================================================
# POST-LOGIN CHECK
# ============================================================================

# Exit if login was not successful and not in map mode (command-line args)
if not LOGIN_SUCCESS and len(sys.argv) <= 1:
	sys.exit(0)

# ============================================================================
# PHASE 2: MAP UI
# ============================================================================

import tkinter as tk
import sys
import os

# Determine logged-in user
USER_EMAIL = LOGIN_EMAIL if LOGIN_EMAIL else (
	sys.argv[1] if len(sys.argv) > 1 else "Student"
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

try:
	from PIL import Image, ImageTk
except ImportError:
	pass


def resource_path(filename: str) -> str:
	"""Resolve resource file path (handles both script and frozen exe modes)."""
	base = None
	try:
		if getattr(sys, 'frozen', False):
			base = os.path.dirname(sys.executable)
		else:
			base = os.path.dirname(__file__)
	except Exception:
		base = os.getcwd()
	return os.path.join(base, filename)


def display_name_from_email(email: str) -> str:
	"""Extract display name from email address (text before '@')."""
	if not email:
		return "Student"
	return email.split('@', 1)[0]


def _hex_to_rgb(hex_color: str) -> tuple:
	"""Convert hex color to RGB tuple."""
	return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb: tuple) -> str:
	"""Convert RGB tuple to hex color."""
	return "#%02x%02x%02x" % (
		max(0, min(255, int(rgb[0]))), 
		max(0, min(255, int(rgb[1]))), 
		max(0, min(255, int(rgb[2])))
	)

# ============================================================================
# MAIN WINDOW SETUP
# ============================================================================

# Reuse or create main window
try:
	window.deiconify()
	for child in window.winfo_children():
		child.destroy()
except Exception:
	window = tk.Tk()

window.title("Campus Map")
window.geometry("1600x900")
try:
	window.state("zoomed")
except Exception:
	pass

window.configure(bg="white")

# Left sidebar (20% width)
sidebar = tk.Frame(window, bg="#FFF9E6")
sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)

# Right content area (80% width)
right_frame = tk.Frame(window, bg="#FFF9E6")
right_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

# ============================================================================
# SIDEBAR: LOGO AND PROFILE
# ============================================================================

# Load logo image for sidebar
original_logo_img = None
try:
	for candidate in ("phinma-logo.png", "phinma-logo2.png"):
		try:
			logo_path = resource_path(candidate)
			if os.path.exists(logo_path):
				original_logo_img = Image.open(logo_path)
				break
		except Exception:
			pass
except Exception:
	pass

# Logo canvas with circular background
logo_canvas = tk.Canvas(sidebar, bg=sidebar['bg'], highlightthickness=0)
display_name = display_name_from_email(USER_EMAIL)
logo_canvas.place(relx=0.5, rely=0.04, anchor="n", relwidth=0.95, relheight=0.35)

# ============================================================================
# SIDEBAR: ROTATING PHRASE ANIMATION
# ============================================================================

PHRASES = [
	"Find What You Need Easily",
	"Let's Get You Started",
	"Explore Your Surroundings",
	"Begin Your Experience",
	"Discover What's Ahead"
]

# Rotating label for motivational phrases
rot_label = tk.Label(
	sidebar, 
	text=PHRASES[0], 
	font=("Arial", 14, "italic"),
	bg="#FFF9E6", 
	fg="#2e7d32", 
	wraplength=220, 
	justify=tk.CENTER
)
rot_label.place(relx=0.5, rely=0.38, anchor="n")

_current_phrase = [0]


def _animate_change(new_text, steps=20, fade_ms=600):
	"""Animate text change with fade out and fade in."""
	fg_start = (50, 125, 50)  # #2e7d32 in RGB
	bg_color = (255, 249, 230)  # #FFF9E6 (background)
	step_delay = max(5, int(fade_ms / steps))

	def _fade_out(i=0):
		if i >= steps:
			rot_label.config(text=new_text)
			rot_label.update()
			rot_label.after(step_delay, lambda: _fade_in(0))
			return
		t = i / float(steps)
		col = tuple(
			int(fg_start[j] + (bg_color[j] - fg_start[j]) * t) 
			for j in range(3)
		)
		rot_label.config(fg=_rgb_to_hex(col))
		rot_label.after(step_delay, lambda: _fade_out(i+1))

	def _fade_in(i=0):
		if i >= steps:
			rot_label.config(fg=_rgb_to_hex(fg_start))
			return
		t = i / float(steps)
		col = tuple(
			int(bg_color[j] + (fg_start[j] - bg_color[j]) * t) 
			for j in range(3)
		)
		rot_label.config(fg=_rgb_to_hex(col))
		rot_label.after(step_delay, lambda: _fade_in(i+1))

	_fade_out(0)


def _rotate_phrases():
	"""Rotate through motivational phrases every 8 seconds."""
	try:
		current = _current_phrase[0]
		next_i = current
		if len(PHRASES) > 1:
			while next_i == current:
				next_i = random.randrange(len(PHRASES))
		else:
			next_i = 0
		_current_phrase[0] = next_i
		_animate_change(PHRASES[next_i], steps=50, fade_ms=1600)
	finally:
		rot_label.after(8000, _rotate_phrases)

_rotate_phrases()

# ============================================================================
# SIDEBAR: SEARCH BAR
# ============================================================================

search_frame = tk.Frame(sidebar, bg="#FFF9E6", bd=0, relief=tk.FLAT)
search_frame.place(relx=0.5, rely=0.45, anchor="n", relwidth=0.84, height=40)

search_bar = tk.Entry(
	search_frame, 
	font=("Arial", 14), 
	fg="gray", 
	justify="left", 
	bd=1, 
	relief=tk.SOLID, 
	highlightthickness=0, 
	bg="white"
)
search_bar.insert(0, "Search")
search_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), pady=4)

# Magnifier button aligned with search entry
magnifier_btn = tk.Button(
	search_frame,
	text="🔍",
	command=lambda: on_search_click(),
	bg="white",
	fg="#000000",
	font=("Arial", 14),
	bd=1,
	relief=tk.SOLID,
	activebackground="#f0f0f0",
	highlightthickness=0
)
magnifier_btn.pack(side=tk.RIGHT, padx=(4, 6), pady=4, ipadx=4)


def _search_on_click(event):
	"""Clear placeholder when search field is focused."""
	if search_bar.get() == "Search":
		search_bar.delete(0, tk.END)
		search_bar.config(fg="black")


def _search_on_focus_out(event):
	"""Restore placeholder when search field is empty."""
	if not search_bar.get().strip():
		search_bar.insert(0, "Search")
		search_bar.config(fg="gray")


search_bar.bind("<FocusIn>", _search_on_click)
search_bar.bind("<FocusOut>", _search_on_focus_out)

# ============================================================================
# BUILDINGS DATABASE
# ============================================================================

BUILDINGS = {
    "Basic Education": {
        "aliases": ["Basic ED", "Basic Education", "SHS", "Senior High School", "STEM", "ABM", "HUMSS", "GAS", "TVL", "Technical-Vocational-Livelihood"],
        "location_desc": "Positioned just past the main vehicle entrance.",
        "programs_and_facilities": """📚 College of Education and Liberal Arts (CELA) - Senior High School (SHS)

🎓 PROGRAMS:
• STEM (Science, Technology, Engineering, Mathematics)
• ABM (Accountancy, Business, and Management)
• HUMSS (Humanities and Social Sciences)
• GAS (General Academic Strand)
• TVL (Technical-Vocational-Livelihood)

📎 DEGREE PROGRAMS:
• Bachelor of Arts in Political Science (AB PolSci)
• Bachelor of Education (optional/general program if applicable)
• Bachelor of Science in Elementary Education (BEEd)
• Bachelor of Secondary Education (BSEd)
  - Major in English
  - Major in Mathematics
  - Major in Science
  - Major in Social Studies""",
        "floors": 4,
        "department": "Senior Highschool",
        "facilities": ["Faculty Office", "Restroom", "Classrooms", "Library"],
        "description": """📍 BUILDING FACILITIES:
• Ground Floor:
  - Rooms 101, 102, 105, 106, 107 (Bookstores), Entrance & Exit
• 2nd Floor:
  - Rooms 201–208 (All classrooms)
• 3rd Floor:
  - Rooms 305–308 (Classrooms)
  - Supreme Student Government & Registered School Organizations Office
  - Basic Education Library
  - Basic Education Office
  - Restroom
• 4th Floor:
  - Rooms 401–408 (Classrooms)""",
        "image": "basic_ed.png",
        "color": "#8BC34A",
    },
    "CMA": {
        "aliases": ["CMA", "College of Management and Accountancy", "College of Tourism and Hospitality Management", "CTHM", "CHTM", "North Hall", "BSA", "BSMA", "BSAT", "BSHM", "BSTM", "BSBA"],
        "location_desc": "Located from the right side after the Registrar.",
        "programs_and_facilities": """📘 College of Management and Accountancy (CMA) / College of Hospitality and Tourism Management (CHTM)

🎓 PROGRAMS:
• Bachelor of Science in Accountancy (BSA)
• Bachelor of Science in Management Accounting (BSMA)
• Bachelor of Science in Accounting Technology (BSAT)
• Bachelor of Science in Hospitality Management (BSHM)
• Bachelor of Science in Tourism Management (BSTM)
• Bachelor of Science in Business Administration (BSBA)
  - Major in Marketing Management
  - Major in Financial Management
• Bachelor of Science in Hotel and Restaurant Management (BSHRM)""",
        "floors": 5,
        "department": "Accountancy/Tourism",
        "facilities": ["Teacher's Lounge", "Classrooms", "Restroom", "Cafeteria"],
        "description": """📍 BUILDING FACILITIES:
• Floor 1:
  - Restroom
  - Room 124 – Storage
  - Rooms 123–128 – Classrooms
  - HTM / CMA Dept (1st & 2nd Floor)
• 2nd Floor:
  - Continued CMA teaching spaces
• 3rd Floor (Tourism):
  - Rooms 323–330 (Classrooms)
  - Restroom
  - Cafeteria (Donut Stand)
• 4th Floor (Tourism):
  - Cold Kitchen Lab
  - Restaurant Simulation Lab
  - Storage Area (Tourism Equipment)
  - Rooms 425–428""",
        "image": "cma.png",
        "color": "#8BC34A",
    },
    "CHS": {
        "aliases": ["College of Criminal Justice Education", "CCJE", "Health Sciences", "CHS", "BSCrim", "Criminology"],
        "location_desc": "North of PHINMA AVE.",
        "programs_and_facilities": """🛡️ College of Criminal Justice Education (CCJE)

🎓 PROGRAMS:
• Bachelor of Science in Criminology (BSCrim)""",
        "floors": 3,
        "department": "Criminology/Health Sciences",
        "facilities": ["Offices", "Classrooms"],
        "description": """📍 BUILDING FACILITIES:
• Floor 1:
  - Restroom
  - Rooms 150–153 (Classrooms)
• Floor 2:
  - College of Criminal Justice Education Faculty Room
  - Restroom
  - Rooms 251–253 (Classrooms)
• Floor 3:
  - Rooms 350–353 (Classrooms)
• Floor 4:
  - Restroom
  - Rooms (Under Construction)""",
        "image": "ccje.png",
        "color": "#9C27B0",
    },
    "Gymnasium": {
        "aliases": ["GYM", "Sports Complex"],
        "floors": 1,
        "department": "Athletics",
        "facilities": ["Court", "Locker Rooms"],
        "location_desc": "West side near the parking lot.",
        "description": """• Sports facilities and athletic programs
• Court access/Event Hosting""",
        "image": "gym.jpg",
        "color": "#E53935",
    },
		"MBA ENG/Hall": {
				"aliases": ["MBA", "Master of Business Administration", "College of Engineering and Architecture", "CEA", "BSArch", "BSCpE", "BSCE", "BSEE", "BSME"],
				"location_desc": "Left after PHINMA AVE.",
				"programs_and_facilities": """🏗️ College of Engineering and Architecture (CEA)

🎓 PROGRAMS:
• Bachelor of Science in Architecture (BSArch)
• Bachelor of Science in Computer Engineering (BSCpE)
• Bachelor of Science in Civil Engineering (BSCE)
• Bachelor of Science in Electrical Engineering (BSEE)
• Bachelor of Science in Mechanical Engineering (BSME)""",
				"floors": 5,
				"department": "Engineering",
				"facilities": ["Lecture Halls", "Offices", "Classrooms", "Restroom", "Labs"],
				"description": """📍 BUILDING FACILITIES:
• Ground / 1st Floor – Point A:
		  - Restroom
		  - Room 101 – CEA Lab (Soil Mechanics, Surveying, Hydraulics, Materials & Testing)
		  - Rooms 102–104 – Classrooms
		  - Room 107, Room 108
		  - University Clinic
		  - Room 109 – Module Storage
		  - Rooms 110–111 – Classrooms (some flooded/abandoned)
	• 2nd Floor:
		- Rooms 201–203 – Classrooms
		- Crime Laboratory
		- HRD Office
		- Storage Room
		- Rooms 207–212 – Classrooms
	• 3rd Floor:
		- Restroom
		- College of Engineering & Architecture Teacher Office
		- Student Lounge / University Chapel
		- College of Education & Liberal Arts Teacher Office
		- Rooms 307–312 – Classrooms
	• 4th Floor (Point A & B):
		- Rooms 401–407 – Classrooms and specialized rooms
		- Mass Communication Simulation Room
		- Learning Resource Center
		- Rooms 407–412 – Classrooms
	• 5th Floor:
		- Room 501 – Audio Visual Room
		- Room 502 – Physics Lab
		- Room 503 – Biology / Pharma Lab
		- Rooms 504–507 – Chemistry Labs (abandoned-looking)""",
				"image": "mbaeng.png",
				"color": "#4CAF50",
		},
    "University Library": {
        "aliases": ["Library", "Bookstore", "Teller"],
        "floors": 3,
        "department": "Library Services",
        "facilities": ["Books", "Study Areas"],
        "location_desc": "Located at the Second floor of FVR.",
        "description": """• Extensive book collection
• Study and research areas
• Library services and support""",
        "image": "library.png",
        "color": "#3F51B5",
    },
    "Business Center": {
        "aliases": ["Biz Center"],
        "floors": 2,
        "department": "Business Services",
        "facilities": ["Offices", "Info Desk", "Bookstore"],
        "location_desc": "After the CMA Hallway then take a right.",
        "description": """• Business services offices
• Information desk
• Bookstore""",
        "image": "bc.png",
        "color": "#FFC107",
    },
    "RS": {
        "aliases": ["riverside", "RS", "CAS", "CAHS", "Nursing", "BSN", "BSP", "BSMLS", "MedTech", "BS Psychology", "College of Allied Health Sciences"],
        "location_desc": "Above the Parking Spot.",
        "programs_and_facilities": """🏥 College of Allied Health Sciences (CAHS)

🎓 PROGRAMS:
• Bachelor of Science in Nursing (BSN)
• Bachelor of Science in Pharmacy (BSP)
• Bachelor of Science in Medical Laboratory Science (BSMLS / MedTech)
• Bachelor of Science in Psychology (BS Psychology)""",
        "floors": 8,
        "department": "Nursing",
        "facilities": ["Classrooms", "Canteen", "Labs", "Restroom", "Offices", "Parking", "Elevator"],
        "description": """📍 BUILDING FACILITIES:
• Ground / 1st Floor:
  - Garage / Parking
  - Restroom
  - Elevator
• 2nd Floor:
  - 201 – Anatomy & Physiology Lab 1
  - 202 – Anatomy & Physiology Lab 2
  - 203 – Microbiology Lab 1
  - 204 – Microbiology Lab 2
  - 206 – Chemistry Lab 3
  - 207 – Chemistry Lab 4
  - 208 – Storage
  - 211 – Chemistry Lab 1
  - 212 – Dispensing Room / Lab
  - 213 – Chemistry Lab 2
  - 215 – Classroom
  - CAHS Faculty Offices
  - Restroom
• 3rd Floor:
  - 301 – Nursing Arts Laboratory Demo Room
  - 302–307 – Mock Hospital
  - 308 – Experimentation Room
  - 309–310 – Instrumentation Room
  - 311 – Molecular Lab (MedTech)
  - 312 – Clinical Chemistry / Microscopy Lab
  - 313 – Histology / Histopathology Lab
  - 314 – Hematology / Immunology / Serology / Immunohematology Lab
  - 315 – Microbiology / Parasitology Lab
  - Restrooms
  - CAS Faculty Office
• 4th Floor:
  - University Canteen
  - Nursing Skills Lab
  - Psychology Lab
  - Anatomy Lab
  - Employee Lounge
  - Restroom
• 5th Floor:
  - Rooms 535–549 – Classrooms
• 6th Floor:
  - Rooms 635–649 – Classrooms
• 7th Floor:
  - Rooms 735–749 – Classrooms
  - Restrooms near 735 and 749
• 8th Floor / Rooftop:
  - Rooms 842–849 – Classrooms
  - Open spaces used for PE classes""",
        "image": "rs.png",
        "color": "#FFC107",
    },
    "PTC": {
        "aliases": ["PTC", "CL", "College of Law", "Information Technology", "CITE", "BSIT", "College of Information Technology"],
        "location_desc": "Above the School Entrance.",
        "programs_and_facilities": """💻 College of Information Technology (CITE)

🎓 PROGRAMS:
• Bachelor of Science in Information Technology (BSIT)""",
        "floors": 4,
        "department": "Information Technology/Law",
        "facilities": ["Classrooms", "Offices", "Labs", "Restroom", "Library"],
        "description": """📍 BUILDING FACILITIES:
• 4th Floor:
  - College of Law Library
  - Room 406 – Classroom
  - Room 405 – Classroom
  - Room 404 – Classroom
  - Room 403 – Classroom
  - Room 402 – Classroom
  - CITE Office
• 3rd Floor:
  - MB-305, MB-306, MB-304, MB-303, MB-302 (Labs)
  - College of Law Moot Court
  - Restroom
• 2nd Floor:
  - Mac Lab
  - Union Office
• Ground Floor:
  - Entrance & Exit""",
        "image": "ptc.png",
        "color": "#FFC107",
    },
    "CSDL": {
        "aliases": ["CSDL", "Center for Student Development and Leadership"],
        "floors": 2,
        "department": "Student Development and Leadership Department",
        "facilities": ["Offices"],
        "location_desc": "Located at the Left side after the Entrance.",
        "description": """• 2nd Floor:
  - ITE 201 Lab
  - ITE 202 Lab
  - Information Technology Services Office
• Ground Floor:
  - CSDL / ITS building entrances
  - Support offices""",
        "image": "csdl.png",
        "color": "#FFC107",
    },
    "OP": {
        "aliases": ["OP", "Office of the President", "MP", "Marketing Department"],
        "floors": 2,
        "department": "Office of the President",
        "facilities": ["President's Office"],
        "location_desc": "2nd Floor of the Marketing Department.",
        "description": """• 2nd Floor:
  - Office of the President
• Ground Floor:
  - Marketing Department offices and reception""",
        "image": "op.png",
        "color": "#FFC107",
    },
    "Marketing Department": {
        "aliases": ["MP", "Office of the President", "Marketing Department", "OP"],
        "floors": 2,
        "department": "Marketing",
        "facilities": ["Office"],
        "location_desc": "1st Floor, after the Main school entrance.",
        "description": """• Ground Floor:
  - Marketing Department reception
  - Enrollment/Marketing service counters
• 2nd Floor:
  - Administrative offices
  - OP (Office of the President) access""",
        "image": "marketingdepartment.png",
        "color": "#FFC107",
    },
    "North Hall": {
        "aliases": ["NH", "North Hall", "Plaza"],
        "floors": 5,
        "department": "Engineering",
        "facilities": ["Classrooms"],
        "location_desc": "After CMA Hallway.",
        "description": """• 5th Floor:
  - 8 rooms with drawing desks (Engineering area, appears abandoned)
• 4th Floor:
  - Rooms 413–421 (no Room 422 — blocked)
• 3rd Floor:
  - Rooms 313–322
• 2nd Floor:
  - Rooms 213–222
• Ground / 1st Floor:
  - Rooms 113–121""",
        "image": "nh.png",
        "color": "#FFC107",
    },
    # small labels / misc
    "Module Distribution": {"aliases": ["Module"], "floors": 1, "department": "Logistics", "facilities": ["Distribution"], "location_desc": "First floor of Basic ED.", "image": "moduledistribution.png", "color": "#9E9E9E"},
    "Finance/Purchasing Department Office": {"aliases": ["Human Resources", "Teller", "Finance"], "floors": 1, "department": "Human Resources", "facilities": ["Teller"], "location_desc": "First floor of the FVR Building, after Atrium.", "image": "teller.png", "color": "#FF5722"},
    "SIS Office": {"aliases": ["SIS", "Concerns", "Office", "System"], "floors": 1, "department": "Information Technology", "facilities": ["IT Help Desk", "Office"], "location_desc": "Located within Atrium.", "image": "sisoffice.png", "color": "#FF5722"},
    "Entrance/Exit": {"aliases": ["Entrance", "Exit"], "floors": 1, "department": "Security", "facilities": ["Entrance", "Exit"], "location_desc": "Infront of the PHINMA Building.", "image": "entrance.png", "color": "#9E9E9E"},
    "Vehicle Entrance/Exit": {"aliases": ["Vehicle", "Entrance", "Exit"], "floors": 1, "department": "Security", "facilities": ["Vehicle Entrance", "Vehicle Exit"], "location_desc": "Beside the PHINMA Building.", "image": "ventrance2.png", "color": "#9E9E9E"},
    "PHINMA Garden": {"aliases": ["Park", "Garden", "PHINMA"], "floors": 1, "department": "None", "facilities": ["School Park"], "location_desc": "Right, after the Student Plaza.", "image": "park.png", "color": "#9E9E9E"},
    "Registrar": {"aliases": ["Registrar", "Office"], "floors": 1, "department": "Registrat's Office", "facilities": ["Registrar"], "location_desc": "At the end of the Atrium.", "image": "registrar.png", "color": "#9E9E9E"},
    "Information Technology Services": {"aliases": ["Information Technology Services", "IT", "CSDL"], "floors": 2, "department": "Information Technology", "facilities": ["Offices"], "location_desc": "Second floor of CSDL, after the vehicle entrance.", "image": "its.png", "color": "#9E9E9E"},
    "Student Support Group": {"aliases": ["SSG", "Student Support Group", "Help"], "floors": 1, "department": "Student Affairs", "facilities": ["Student Support Office"], "location_desc": "Located within Atrium.", "image": "ssg.png", "color": "#9E9E9E"},
    "Quality Assurance Office": {"aliases": ["QAO", "Quality Assurance Office", "Office"], "floors": 1, "department": "Quality Assurance", "facilities": ["Quality Assurance Office"], "location_desc": "Located within Atrium.", "image": "qao.png", "color": "#9E9E9E"},
    "TES/TDP Ched Scholarships": {"aliases": ["TES", "TDP", "Scholarship", "CHED"], "floors": 1, "department": "Scholarship Assistance", "facilities": ["Scholarship Office"], "location_desc": "Located within Atrium.", "image": "testdp.png", "color": "#9E9E9E"},
    "Supreme Student Council": {"aliases": ["SSC", "Supreme Student Council", "Office"], "floors": 1, "department": "Student Council", "facilities": ["Supreme Student Council Office"], "location_desc": "Located within Atrium.", "image": "ssc.png", "color": "#9E9E9E"},
    "University Research Center": {"aliases": ["URC", "University Research Center", "Office"], "floors": 1, "department": "Research", "facilities": ["Research Center"], "location_desc": "Located within Atrium.", "image": "qao.png", "color": "#9E9E9E"},
    "BSBA Simulation Room": {"aliases": ["BSBA", "Business Administration", "Simulation"], "floors": 2, "department": "Business Administration", "facilities": ["Simulation Room"], "location_desc": "Located on the second floor of the Atrium.", "image": "bsba.png", "color": "#9E9E9E"},
    "College of Law Office": {"aliases": ["COLO", "College of Law", "Office"], "floors": 2, "department": "Law", "facilities": ["Office"], "location_desc": "Located on the second floor of the Atrium.", "image": "colo.png", "color": "#9E9E9E"},
    "School of Graduate and Professional Studies": {"aliases": ["SOGAPS", "School of Graduate and Professional Studies", "Office"], "floors": 2, "department": "Graduate Studies", "facilities": ["Graduate Studies Office"], "location_desc": "Located on the second floor of the Atrium.", "image": "sogaps.png", "color": "#9E9E9E"},
    "University Extension Council": {"aliases": ["UEC", "University Extension Council"], "floors": 1, "department": "Extension Services", "facilities": ["Extension Services Office"], "location_desc": "Located on the left side after CSDL.", "image": "uec.png", "color": "#9E9E9E"},
    "SP":{"aliases": ["SP", "Student Plaza", "Food"], "floors": 1, "department": "Campus", "facilities": ["Cafeteria", "Student Canteen", "Student Plaza"], "location_desc": "Right side of PHINMA AVE.", "description": "Food court/Event Hosting Place.", "image": "sp.png", "color": "#FFC107"},
}

# ============================================================================
# SEARCH FUNCTIONALITY
# ============================================================================


def perform_search(query: str):
	"""
	Search buildings by name, aliases, location description, and facilities.
	Returns list of matching building names (case-insensitive).
	"""
	q = query.strip().lower()
	if not q:
		return []
	
	results = []
	for name, info in BUILDINGS.items():
		# Check building name
		if q in name.lower():
			results.append(name)
			continue
		
		# Check aliases
		aliases = info.get("aliases", [])
		if any(q in a.lower() for a in aliases):
			results.append(name)
			continue
		
		# Check location description
		if q in info.get("location_desc", "").lower():
			results.append(name)
			continue
		
		# Check facilities
		if any(q in f.lower() for f in info.get("facilities", [])):
			results.append(name)
			continue
	
	return results




# ============================================================================
# RIGHT PANEL: INFO AND MAP
# ============================================================================

# Top half: Building information panel
info_panel = tk.Frame(right_frame, bg="#FFF9E6", bd=2, relief=tk.RIDGE)
info_panel.place(relx=0, rely=0, relwidth=1, relheight=0.50)

info_title = tk.Label(
	info_panel, 
	text="Search a building", 
	font=("Arial", 18, "bold"), 
	bg="#2e7d32", 
	fg="#FFFFFF", 
	bd=2, 
	relief=tk.RIDGE, 
	padx=15, 
	pady=8
)
info_title.pack(pady=(10, 5))

# Horizontal layout: Image on left, description on right
content_frame = tk.Frame(info_panel, bg="#FFF9E6")
content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Building image (left side) - NO GREY BACKGROUND, image fills entire space
info_image_label = tk.Label(content_frame, bg="#FFF9E6")
info_image_label.pack(side=tk.LEFT, padx=(0, 15), fill=tk.BOTH, expand=True)

current_building = [None]

# --- Placeholder image and description on first load ---
def show_placeholder_info():
    # avoid re-rendering if already displayed
    if getattr(info_image_label, "image", None):
        return

    info_title.config(text="Campus Navigation System")
    info_text.config(state=tk.NORMAL)
    info_text.delete(1.0, tk.END)
    
    # Styled welcome message with floor-like headers and bullets
    info_text.insert(tk.END, " 🎓 Getting Started \n", 'floor')
    info_text.insert(tk.END, "• Use the search bar to find buildings, offices, or facilities.\n", 'bullet')
    info_text.insert(tk.END, "• Click on a result to view detailed building information.\n", 'bullet')
    info_text.insert(tk.END, "• Double-click results to highlight locations on the map.\n\n", 'bullet')
    
    info_text.insert(tk.END, " 🗺️ Exploring the Map \n", 'floor')
    info_text.insert(tk.END, "• Zoom in/out using the zoom buttons or mouse wheel.\n", 'bullet')
    info_text.insert(tk.END, "• Click and drag to pan across the campus map.\n", 'bullet')
    info_text.insert(tk.END, "• Double-click the map to reset zoom to default.\n\n", 'bullet')
    
    info_text.insert(tk.END, " 📍 Building Details \n", 'floor')
    info_text.insert(tk.END, "• View floor-by-floor information for each building.\n", 'bullet')
    info_text.insert(tk.END, "• Check facilities, departments, and location descriptions.\n", 'bullet')
    info_text.insert(tk.END, "• See building images and comprehensive room listings.\n\n", 'bullet')
    
    info_text.insert(tk.END, "Welcome to PHINMA Campus Navigation!\n", 'meta')
    
    info_text.config(state=tk.DISABLED, bg="#FFF9E6")

    logo_path = resource_path("phinma-logo2.png")

    def do_render():
        try:
            from PIL import Image, ImageTk
            if os.path.exists(logo_path):
                im = Image.open(logo_path)
                target = 260
                w0, h0 = im.size
                scale = min(target / w0, target / h0)
                nw = max(1, int(w0 * scale))
                nh = max(1, int(h0 * scale))
                im2 = im.resize((nw, nh), Image.Resampling.LANCZOS)
                info_image_label.image = ImageTk.PhotoImage(im2)
                info_image_label.config(image=info_image_label.image, text="", bg="#f0f0f0")
                return
        except Exception:
            pass

        try:
            info_image_label.update_idletasks()
            iw = max(1, info_image_label.winfo_width() or 200)
            ih = max(1, info_image_label.winfo_height() or 150)

            if os.path.exists(logo_path):
                img = tk.PhotoImage(file=logo_path)
                sx = max(1, int(img.width() / iw))
                sy = max(1, int(img.height() / ih))
                ss = max(sx, sy)
                if ss > 1:
                    img = img.subsample(ss, ss)
                info_image_label.image = img
                info_image_label.config(image=img, text="", bg="#f0f0f0")
                return
        except Exception:
            pass

        info_image_label.config(image="", text="PHINMA", font=("Arial", 18, "bold"), fg="#222", bg="#f0f0f0")

    if info_image_label.winfo_width() <= 1 or info_image_label.winfo_height() <= 1:
        info_image_label.after(100, do_render)
        def _on_cfg(e):
            try:
                info_image_label.unbind("<Configure>", _on_cfg_id)
            except Exception:
                pass
            do_render()
        _on_cfg_id = info_image_label.bind("<Configure>", _on_cfg)
    else:
        do_render()

# ============================================================================
# BUILDING INFO TEXT AREA WITH SCROLLBAR
# ============================================================================

text_frame = tk.Frame(content_frame, bg="#FFF9E6")
text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

info_text = tk.Text(
	text_frame, 
	wrap=tk.WORD, 
	font=("Arial", 11), 
	bg="#FFF9E6", 
	bd=1
)
info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
info_text.config(state=tk.DISABLED)

info_scroll = tk.Scrollbar(text_frame, command=info_text.yview)
info_scroll.pack(side=tk.RIGHT, fill=tk.Y)
info_text['yscrollcommand'] = info_scroll.set

# Configure text tags for styled formatting
info_text.tag_configure(
	'floor', 
	background='#2e7d32', 
	foreground='white',
	font=("Arial", 10, "bold"), 
	lmargin1=4, 
	lmargin2=4,
	spacing1=3, 
	spacing3=6
)
info_text.tag_configure(
	'bullet', 
	foreground='#222222',
	lmargin1=20, 
	lmargin2=30, 
	font=("Arial", 16), 
	spacing1=2, 
	spacing3=2
)
info_text.tag_configure(
	'meta', 
	font=("Arial", 16, "italic"), 
	foreground='#555555', 
	lmargin1=4, 
	spacing3=4
)
info_text.tag_configure(
	'normal', 
	font=("Arial", 16), 
	lmargin1=4, 
	spacing3=3
)

# ============================================================================
# BOTTOM HALF: MAP INTERFACE
# ============================================================================

map_frame = tk.Frame(right_frame, bg="#FFF9E6")
map_frame.place(relx=0, rely=0.50, relwidth=1, relheight=0.50)

# Map state variables
zoom_level = [1.0]
campus_map_image = [None]
original_image = [None]
map_mode = ["image"]


def redraw_map():
	"""Redraw the campus map at the current zoom level."""
	if original_image[0] is None:
		if map_mode[0] == "photoimage":
			map_canvas.delete("all")
			if campus_map_image[0]:
				map_canvas.create_image(0, 0, image=campus_map_image[0], anchor=tk.NW)
				map_canvas.config(
					scrollregion=(0, 0, campus_map_image[0].width(), campus_map_image[0].height())
				)
		return
	
	try:
		w, h = original_image[0].size
		new_w = max(1, int(w * zoom_level[0]))
		new_h = max(1, int(h * zoom_level[0]))
		
		resized = original_image[0].resize((new_w, new_h), Image.Resampling.LANCZOS)
		campus_map_image[0] = ImageTk.PhotoImage(resized)
		
		map_canvas.delete("all")
		map_canvas.create_image(0, 0, image=campus_map_image[0], anchor=tk.NW)
		map_canvas.config(scrollregion=(0, 0, new_w, new_h))
	except Exception as e:
		map_canvas.delete("all")
		map_canvas.create_text(
			400, 300, 
			text=f"Error: {str(e)}", 
			font=("Arial", 12), 
			fill="red", 
			justify=tk.CENTER
		)


def zoom_in():
	"""Zoom in on the map."""
	zoom_level[0] *= 1.5
	if zoom_level[0] > 5:
		zoom_level[0] = 5
	redraw_map()
	zoom_label.config(text=f"Zoom: {zoom_level[0]:.2f}x")


def zoom_out():
	"""Zoom out on the map."""
	zoom_level[0] /= 1.5
	if zoom_level[0] < 0.5:
		zoom_level[0] = 0.5
	redraw_map()
	zoom_label.config(text=f"Zoom: {zoom_level[0]:.2f}x")


def reset_zoom():
	"""Reset zoom to 1.0x."""
	zoom_level[0] = 1.0
	redraw_map()
	zoom_label.config(text="Zoom: 1.0x")

# Map controls and canvas
zoom_frame = tk.Frame(map_frame, bg="#FFF9E6")
zoom_frame.pack(fill=tk.X, padx=10, pady=(10, 5), side=tk.TOP)

left_spacer = tk.Frame(zoom_frame, bg="#FFF9E6")
left_spacer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Button(zoom_frame, text="🔍+ Zoom In", command=zoom_in, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
tk.Button(zoom_frame, text="🔍- Zoom Out", command=zoom_out, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
tk.Button(zoom_frame, text="↺ Reset", command=reset_zoom, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

center_container = tk.Frame(zoom_frame, bg="#FFF9E6")
center_container.pack(side=tk.LEFT, padx=20)

campus_map_title = tk.Label(
	center_container, 
	text="Campus Map", 
	font=("Arial", 14, "bold"),
	bg="#2e7d32", 
	fg="#FFFFFF", 
	bd=2, 
	relief=tk.RIDGE, 
	padx=12, 
	pady=6
)
campus_map_title.pack(side=tk.LEFT, padx=(0, 15))

zoom_label = tk.Label(
	center_container, 
	text="Zoom: 1.0x", 
	font=("Arial", 11, "bold"),
	bg="#FFF9E6", 
	fg="#000000", 
	bd=1, 
	relief=tk.SOLID, 
	padx=8, 
	pady=4
)
zoom_label.pack(side=tk.LEFT, padx=5)

legend_btn = tk.Button(
	center_container, 
	text="📋 Legend", 
	font=("Arial", 10),
	bg="#2e7d32", 
	fg="white", 
	bd=1, 
	relief=tk.SOLID,
	activebackground="#1b5e20", 
	activeforeground="white"
)
legend_btn.pack(side=tk.LEFT, padx=6)

right_spacer = tk.Frame(zoom_frame, bg="#FFF9E6")
right_spacer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Map canvas with scrollbars
map_canvas_frame = tk.Frame(map_frame, bg="#ffffff")
map_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

map_canvas = tk.Canvas(map_canvas_frame, bg="white", scrollregion=(0, 0, 1000, 1000))
map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

h_scroll = tk.Scrollbar(map_canvas_frame, orient=tk.HORIZONTAL, command=map_canvas.xview)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

v_scroll = tk.Scrollbar(map_canvas_frame, orient=tk.VERTICAL, command=map_canvas.yview)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

map_canvas.config(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

# ============================================================================
# LEGEND PANEL
# ============================================================================

legend_panel = tk.Frame(right_frame, bg="#FFF9E6", bd=2, relief=tk.RIDGE)
legend_is_open = [False]


def _populate_legend_placeholder():
	"""Populate legend with directory information."""
	for w in legend_panel.winfo_children():
		w.destroy()
	
	tk.Label(
		legend_panel, 
		text="Legend / Directory", 
		font=("Arial", 12, "bold"),
		bg="#2e7d32", 
		fg="white", 
		pady=6
	).pack(fill=tk.X)
	
	# Scrollable directory text
	txt_frame = tk.Frame(legend_panel, bg="#FFF9E6")
	txt_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
	
	txt = tk.Text(txt_frame, wrap=tk.WORD, font=("Arial", 14), bg="#FFF9E6", height=20)
	txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
	
	scrollbar = tk.Scrollbar(txt_frame, command=txt.yview)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
	txt['yscrollcommand'] = scrollbar.set
	
	# Configure styled tags
	txt.tag_configure(
		'number', 
		background='#2e7d32', 
		foreground='white',
		font=("Arial", 11, "bold"), 
		relief=tk.SOLID, 
		borderwidth=2, 
		lmargin1=2, 
		lmargin2=2
	)
	txt.tag_configure(
		'content', 
		background='#4a4a4a', 
		foreground='white',
		font=("Arial", 11, "bold"), 
		spacing1=2, 
		spacing3=2, 
		lmargin1=2, 
		lmargin2=2,
		relief=tk.SOLID, 
		borderwidth=2
	)
	txt.tag_configure('spacer', spacing1=4, spacing3=4)
	
	# Directory data
	directory_entries = [
		("1.", "Center for Student Development and Leadership (CSDL) Office", "CSDL ITS 1F"),
		("2.", "College of Allied Health Sciences (CAHS) Office", "Riverside 2F"),
		("3.", "College of Arts and Sciences (CAS) Office", "Riverside 3F"),
		("4.", "College of Criminal Justice Education (CCJE) Office", "CCJE 2F"),
		("5.", "College of Education and Liberal Arts (CELA) Office", "MBA Engg 3F"),
		("6.", "College of Engineering and Architecture (CEA) Office", "MBA Engg 3F"),
		("7.", "College of Information Technology Education (CITE) Office", "PTC 4F"),
		("8.", "College of Law Office", "Atrium 2F"),
		("9.", "College of Management and Accountancy (CMA) Office", "CMA 2F"),
		("10.", "Finance / Purchasing Department Office", "FVR 1F"),
		("11.", "General Services Department (GSD) Office", "GYM 1F"),
		("12.", "ITS Department Office", "CSDL ITS 2F"),
		("13.", "School of Graduate and Professional Studies (SGPS) Office", "Atrium 2F"),
		("14.", "PEDRO Hub Office", "Atrium 1F"),
		("15.", "Registrar's Office", "FVR 1F"),
		("16.", "Senior High School (SHS) Office", "Basic Ed 3F"),
		("17.", "University Canteen", "Riverside 4F"),
		("18.", "University Chapel", "MBA Hall 3F"),
		("19.", "University Clinic", "MBA Hall 1F"),
		("20.", "University Library", "FVR 2F - 3F"),
		("21.", "Business Center", "Business Center 1F"),
	]
	
	for num, name, location in directory_entries:
		txt.insert(tk.END, num + "\n", 'number')
		txt.insert(tk.END, f"{name}|{location}\n", 'content')
		txt.insert(tk.END, "\n", 'spacer')
	
	txt.config(state=tk.DISABLED)


def toggle_legend():
	"""Toggle legend panel visibility on the right side of the map."""
	if legend_is_open[0]:
		# Close legend - hide it and restore full width
		legend_panel.place_forget()
		map_frame.place(relx=0, rely=0.50, relwidth=1, relheight=0.50)
		legend_is_open[0] = False
		legend_btn.config(text="📋 Legend", bg="#2e7d32")
	else:
		# Open legend - position on right side of map area only
		map_frame.place(relx=0, rely=0.50, relwidth=0.85, relheight=0.50)
		legend_panel.place(relx=0.85, rely=0.50, relwidth=0.15, relheight=0.50)
		legend_is_open[0] = True
		legend_btn.config(text="📋 Close", bg="#c62828")
		_populate_legend_placeholder()


legend_btn.config(command=toggle_legend)

# ============================================================================
# MAP LOADING
# ============================================================================


def load_campus_map(filename="campus_map.png"):
	"""Load and display campus map image on the canvas."""
	full = filename if os.path.isabs(filename) else os.path.join(
		os.path.dirname(__file__), filename
	)
	
	if not os.path.exists(full):
		map_canvas.delete("all")
		map_canvas.create_text(
			400, 300, 
			text="Campus map file not found.\nPlace 'campus_map.png' in the script folder.", 
			font=("Arial", 12), 
			fill="#666", 
			justify=tk.CENTER
		)
		return False
	
	# Try Pillow first for smooth zoom/pan
	try:
		original_image[0] = Image.open(full)
		map_mode[0] = "image"
		campus_map_image[0] = None
		redraw_map()
		return True
	except ImportError:
		pass
	
	# Fallback: Tkinter PhotoImage (limited zoom)
	try:
		img = tk.PhotoImage(file=full)
		campus_map_image[0] = img
		original_image[0] = None
		map_mode[0] = "photoimage"
		map_canvas.delete("all")
		map_canvas.create_image(0, 0, image=campus_map_image[0], anchor=tk.NW, tags="map_image")
		map_canvas.config(scrollregion=(0, 0, img.width(), img.height()))
		zoom_label.config(text="Zoom: 1.0x (Install Pillow for smooth zoom)")
		return True
	except Exception:
		pass
	
	# Both methods failed
	map_canvas.delete("all")
	map_canvas.create_text(
		400, 300, 
		text="Could not load map image.\nTry installing Pillow: pip install pillow", 
		font=("Arial", 12), 
		fill="#666", 
		justify=tk.CENTER
	)
	return False


# Map interaction: mouse wheel and click-drag
def _on_mousewheel(event):
	"""Handle mouse wheel zoom."""
	if event.delta > 0:
		zoom_in()
	else:
		zoom_out()


map_canvas.bind("<MouseWheel>", _on_mousewheel)

# Hotspot interaction state and data
HOTSPOTS = {}
hotspot_file = os.path.join(os.path.dirname(__file__), "hotspots.json")
map_dragging = [False]

def load_hotspots():
	"""Load hotspots from `hotspots.json` if present.

	Supported formats in JSON:
	- Simple: {"Name": [[x,y], [x,y], ...], ...}
	- Extended: {"Name": {"poly": [[x,y],...], "images": ["sv/1.png", ...]}}

	Coordinates must be in the original image pixel space.
	"""
	global HOTSPOTS
	try:
		if os.path.exists(hotspot_file):
			with open(hotspot_file, "r", encoding="utf-8") as fh:
				raw = json.load(fh)
			HOTSPOTS = {}
			for k, v in raw.items():
				if isinstance(v, dict) and "poly" in v:
					HOTSPOTS[k] = {"poly": v.get("poly", []), "images": v.get("images", [])}
				elif isinstance(v, list):
					HOTSPOTS[k] = {"poly": v, "images": []}
				else:
					HOTSPOTS[k] = {"poly": [], "images": []}
		else:
			HOTSPOTS = {}
	except Exception:
		HOTSPOTS = {}

def point_in_poly(x, y, poly):
	"""Return True if point (x,y) is inside polygon `poly` (list of (x,y))."""
	inside = False
	j = len(poly) - 1
	for i in range(len(poly)):
		xi, yi = poly[i]
		xj, yj = poly[j]
		intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi)
		if intersect:
			inside = not inside
		j = i
	return inside

def image_coords_from_event(event):
	"""Convert canvas event coords to original image coords (ints)."""
	cx = map_canvas.canvasx(event.x)
	cy = map_canvas.canvasy(event.y)
	if zoom_level[0] <= 0:
		return int(cx), int(cy)
	return int(cx / zoom_level[0]), int(cy / zoom_level[0])

def clear_hotspot_highlight():
	try:
		map_canvas.delete("hotspot_highlight")
	except Exception:
		pass


def open_street_view(image_paths, title="Street View"):
	"""Open a simple street-view modal for the given list of image paths.

	Image paths may be absolute or relative to the script folder.
	"""
	if not image_paths:
		return

	sv_win = tk.Toplevel()
	sv_win.title(title)
	sv_win.geometry("800x600")
	sv_win.transient(map_canvas)
	sv_win.grab_set()

	idx = [0]
	pil_imgs = [None]
	tk_img = [None]
	zoom = [1.0]
	offset = [0, 0]

	viewer = tk.Canvas(sv_win, bg="#000000")
	viewer.pack(fill=tk.BOTH, expand=True)

	def load_image(i):
		p = image_paths[i]
		full = p if os.path.isabs(p) else os.path.join(os.path.dirname(__file__), p)
		try:
			from PIL import Image, ImageTk
			im = Image.open(full)
			pil_imgs[0] = im
			render()
		except Exception:
			pil_imgs[0] = None
			viewer.delete("all")
			viewer.create_text(400, 300, text="Street image not found", fill="white")

	def render():
		viewer.delete("all")
		if not pil_imgs[0]:
			return
		from PIL import ImageTk
		im = pil_imgs[0]
		w, h = im.size
		nw = max(1, int(w * zoom[0]))
		nh = max(1, int(h * zoom[0]))
		resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
		tk_img[0] = ImageTk.PhotoImage(resized)
		viewer.create_image(offset[0], offset[1], image=tk_img[0], anchor=tk.NW, tags="svimg")

	def prev_img():
		if idx[0] > 0:
			idx[0] -= 1
			zoom[0] = 1.0
			offset[0], offset[1] = 0, 0
			load_image(idx[0])

	def next_img():
		if idx[0] < len(image_paths) - 1:
			idx[0] += 1
			zoom[0] = 1.0
			offset[0], offset[1] = 0, 0
			load_image(idx[0])

	def zoom_in():
		zoom[0] = min(5.0, zoom[0] * 1.25)
		render()

	def zoom_out():
		zoom[0] = max(0.5, zoom[0] / 1.25)
		render()

	def on_drag_start(e):
		viewer.scan_mark(e.x, e.y)

	def on_drag(e):
		viewer.scan_dragto(e.x, e.y, gain=1)
		# update offset for rendering coordinates
		# Tk canvas manages visual pan; keep offset as negative of canvas x/y origin
		try:
			offset[0] = -int(viewer.canvasx(0))
			offset[1] = -int(viewer.canvasy(0))
		except Exception:
			pass

	btn_frame = tk.Frame(sv_win, bg="#222")
	btn_frame.place(relx=0.5, rely=0.96, anchor=tk.S)

	tk.Button(btn_frame, text="◀ Prev", command=prev_img).pack(side=tk.LEFT, padx=6)
	tk.Button(btn_frame, text="Zoom +", command=zoom_in).pack(side=tk.LEFT, padx=6)
	tk.Button(btn_frame, text="Zoom -", command=zoom_out).pack(side=tk.LEFT, padx=6)
	tk.Button(btn_frame, text="Next ▶", command=next_img).pack(side=tk.LEFT, padx=6)
	tk.Button(btn_frame, text="Close", command=sv_win.destroy).pack(side=tk.LEFT, padx=6)

	viewer.bind("<ButtonPress-1>", on_drag_start)
	viewer.bind("<B1-Motion>", on_drag)

	load_image(idx[0])

def draw_hotspot_highlight(name):
	"""Draw polygon highlight for hotspot `name` scaled by current zoom."""
	clear_hotspot_highlight()
	poly = HOTSPOTS.get(name)
	if not poly:
		return
	scaled = []
	for x, y in poly:
		scaled.append(int(x * zoom_level[0]))
		scaled.append(int(y * zoom_level[0]))
	# outline with building color if available
	color = BUILDINGS.get(name, {}).get("color", "#FFD54F")
	map_canvas.create_polygon(*scaled, outline=color, fill="", width=3, tags=("hotspot_highlight",))
	# center view on hotspot
	try:
		bx = sum(p[0] for p in poly) / len(poly)
		by = sum(p[1] for p in poly) / len(poly)
		cx = int(bx * zoom_level[0])
		cy = int(by * zoom_level[0])
		vw = map_canvas.winfo_width() or 400
		vh = map_canvas.winfo_height() or 300
		full_w = (original_image[0].size[0] * zoom_level[0]) if original_image[0] else campus_map_image[0].width()
		full_h = (original_image[0].size[1] * zoom_level[0]) if original_image[0] else campus_map_image[0].height()
		left = max(0, cx - vw // 2)
		top = max(0, cy - vh // 2)
		if full_w > 0:
			map_canvas.xview_moveto(min(1.0, left / max(1, full_w - vw)))
		if full_h > 0:
			map_canvas.yview_moveto(min(1.0, top / max(1, full_h - vh)))
	except Exception:
		pass

def on_map_button_press(event):
	map_dragging[0] = False
	try:
		map_canvas.scan_mark(event.x, event.y)
	except Exception:
		pass

def on_map_motion(event):
	map_dragging[0] = True
	try:
		map_canvas.scan_dragto(event.x, event.y, gain=1)
	except Exception:
		pass

def on_map_button_release(event):
	# if it was a click (no dragging), handle hotspot lookup
	if not map_dragging[0]:
		ix, iy = image_coords_from_event(event)
		# find first matching hotspot
		for name, data in HOTSPOTS.items():
			poly = data.get("poly") if isinstance(data, dict) else data
			if poly and point_in_poly(ix, iy, poly):
				draw_hotspot_highlight(name)
				# If hotspot has street-view images, open modal viewer
				imgs = data.get("images", []) if isinstance(data, dict) else []
				if imgs:
					open_street_view(imgs, title=name)
				else:
					try:
						show_building_info(name)
					except Exception:
						pass
				return
		# no hotspot matched - clear highlight
		clear_hotspot_highlight()

load_hotspots()

map_canvas.bind("<ButtonPress-1>", on_map_button_press)
map_canvas.bind("<B1-Motion>", on_map_motion)
map_canvas.bind("<ButtonRelease-1>", on_map_button_release)
map_canvas.bind("<Double-Button-1>", lambda e: reset_zoom())

# ============================================================================
# BUILDING INFO PARSING AND DISPLAY
# ============================================================================


def _normalize_floor_label(header: str) -> str:
	"""Normalize various floor header formats to standardized labels."""
	h = header.strip().lower()
	h = h.replace('/', ' ').replace('–', '-')
	h = re.sub(r'[\:\s]+$', '', h)
	
	# Normalize common floor names
	h = re.sub(r'\bground\b', '1st', h)
	h = re.sub(r'\bfirst\b', '1st', h)
	h = re.sub(r'\bsecond\b', '2nd', h)
	h = re.sub(r'\bthird\b', '3rd', h)
	h = re.sub(r'\bfourth\b', '4th', h)
	h = re.sub(r'\bfifth\b', '5th', h)
	h = re.sub(r'\bsixth\b', '6th', h)
	h = re.sub(r'\bseventh\b', '7th', h)
	h = re.sub(r'\beighth\b', '8th', h)
	h = re.sub(r'\bninth\b', '9th', h)
	
	# Check for rooftop
	if 'rooftop' in h or 'roof' in h:
		return 'Rooftop'
	
	# Extract numeric ordinal
	m = re.search(r'(\d+(st|nd|rd|th)?)', h)
	if m:
		return f"{m.group(1)} Floor".replace('  ', ' ').strip()
	
	return header.strip().title()


def _parse_description_sections(desc: str):
	"""
	Parse building description into floor sections and other lines.
	Returns: (ordered_sections, other_lines)
	  ordered_sections = [(floor_label, [lines]), ...] sorted numerically
	  other_lines = [lines not under a floor header]
	"""
	if not desc:
		return [], []
	
	# Normalize restroom terms
	text = re.sub(r'\bComfort Room(s)?\b', 'Restroom', desc, flags=re.I)
	text = re.sub(r'\bRestrooms\b', 'Restroom', text, flags=re.I)
	text = text.replace('•', '').strip()
	lines = [ln.rstrip() for ln in text.splitlines()]
	
	sections = []
	other = []
	current_header = None
	current_lines = []
	
	# Header detection pattern
	header_re = re.compile(r'\b(floor|ground|rooftop|level)\b', re.I)
	
	for ln in lines:
		s = ln.strip()
		if not s:
			if current_header:
				current_lines.append('')
			else:
				other.append('')
			continue
		
		if header_re.search(s):
			if current_header:
				sections.append((current_header, current_lines))
			current_header = _normalize_floor_label(s)
			current_lines = []
		else:
			if current_header:
				current_lines.append(s)
			else:
				other.append(s)
	
	if current_header:
		sections.append((current_header, current_lines))
	
	# Sort sections by floor number
	def sort_key(item):
		hdr = item[0]
		if hdr == 'Rooftop':
			return 999
		m = re.match(r'(\d+)', hdr)
		return int(m.group(1)) if m else 1000
	
	sections_sorted = sorted(sections, key=sort_key)
	return sections_sorted, other

def show_building_info(name: str):
    # remember current building for resize redraws
    try:
        current_building[0] = name
    except Exception:
        pass
    info = BUILDINGS.get(name)
    if not info:
        info_title.config(text="Unknown")
        info_text.config(state=tk.NORMAL)
        info_text.delete(1.0, tk.END)
        info_text.insert(tk.END, "No information available.", 'normal')
        info_text.config(state=tk.DISABLED)
        info_image_label.config(image="", text="No Building Info", bg="#FFF9E6", fg="#333")
        return
    info_title.config(text=name)

    # Meta lines (floors, department, facilities, location)
    floors = info.get('floors', '?')
    dept = info.get('department', 'N/A')
    facilities = ", ".join(info.get("facilities", []))
    location = info.get('location_desc', '')
    # Clear and build nicely formatted content with tags
    info_text.config(state=tk.NORMAL)
    info_text.delete(1.0, tk.END)

    info_text.insert(tk.END, f"🏢 Floors: {floors}\n", 'meta')
    info_text.insert(tk.END, f"🏛 Department: {dept}\n", 'meta')
    info_text.insert(tk.END, f"🏫 Facilities: {facilities}\n", 'meta')
    info_text.insert(tk.END, f"📍 Location: {location}\n\n", 'meta')

    # Display programs and facilities info if available (remove decorative emoji/headers)
    programs_info = info.get("programs_and_facilities", "")
    if programs_info:
        clean_prog = programs_info
        for ch in ["📚","📘","🛡️","🏗️","🏥","💻","🎓","📎","📍"]:
            clean_prog = clean_prog.replace(ch, "")
        # Trim leading spaces on each line and collapse excessive blank lines
        clean_prog = re.sub(r'^[ \t]+', '', clean_prog, flags=re.M)
        clean_prog = re.sub(r'\n{3,}', '\n\n', clean_prog)
        info_text.insert(tk.END, f"{clean_prog}\n\n", 'normal')

    # Parse description into ordered floor sections and other lines (clean decorative headings)
    desc = info.get("description", "")
    # remove '📍 BUILDING FACILITIES:' heading and common decorative emojis
    desc = re.sub(r'📍\s*BUILDING FACILITIES:\s*', '', desc, flags=re.I)
    for ch in ["📚","📘","🛡️","🏗️","🏥","💻","🎓","📎","📍"]:
        desc = desc.replace(ch, "")
    desc = re.sub(r'^[ \t]+', '', desc, flags=re.M)
    sections, other_lines = _parse_description_sections(desc)

    # Render floor sections in numeric order (1st, 2nd, ...)
    for (hdr, lines) in sections:
        # show only standardized header (e.g., "1st Floor")
        info_text.insert(tk.END, f" {hdr} \n", 'floor')
        for ln in lines:
            t = ln.strip()
            if not t:
                info_text.insert(tk.END, "\n", 'normal')
                continue
            # treat offices and rooms and numeric-start lines as bullets
            if re.search(r'\bOffice\b', t, re.I) or re.search(r'\bRoom\b', t, re.I) or re.match(r'^\d', t) or t.startswith('-') or ',' in t:
                item = re.sub(r'^[\-\s•]+', '', t)
                info_text.insert(tk.END, f"• {item}\n", 'bullet')
            else:
                # fallback normal text
                info_text.insert(tk.END, f"{t}\n", 'normal')
        info_text.insert(tk.END, "\n", 'normal')

    # Render any non-floor lines after floors (keeps them readable)
    if other_lines:
        for ln in other_lines:
            t = ln.strip()
            if not t:
                info_text.insert(tk.END, "\n", 'normal')
                continue
            # prefer bullets for office-like or room-like lines
            if re.search(r'\bOffice\b', t, re.I) or re.search(r'\bRoom\b', t, re.I) or re.match(r'^\d', t) or t.startswith('-'):
                item = re.sub(r'^[\-\s•]+', '', t)
                info_text.insert(tk.END, f"• {item}\n", 'bullet')
            else:
                info_text.insert(tk.END, f"{t}\n", 'normal')

    info_text.config(state=tk.DISABLED)

    # Load and render the building image using FIT mode (no cropping, fills space)
    img_path = info.get("image", "")
    if img_path:
        full = os.path.join(os.path.dirname(__file__), img_path)
        if os.path.exists(full):
            def do_render():
                info_image_label.update_idletasks()
                iw = info_image_label.winfo_width() or 300
                ih = info_image_label.winfo_height() or 200
                if iw <= 1:
                    iw = 300
                if ih <= 1:
                    ih = 200
                
                try:
                    from PIL import Image, ImageTk
                    im = Image.open(full)
                    w, h = im.size
                    # FIT mode: scale to fit inside without cropping
                    scale = min(iw / w, ih / h)
                    new_w = max(1, int(w * scale))
                    new_h = max(1, int(h * scale))
                    im2 = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(im2)
                    info_image_label.image = photo
                    info_image_label.config(image=photo, text="", bg="#FFF9E6")
                    return
                except Exception:
                    pass
                
                # Fallback: tkinter PhotoImage with subsample
                try:
                    img = tk.PhotoImage(file=full)
                    sx = max(1, int(img.width() / iw))
                    sy = max(1, int(img.height() / ih))
                    ss = max(sx, sy)
                    if ss > 1:
                        img = img.subsample(ss, ss)
                    info_image_label.image = img
                    info_image_label.config(image=img, text="", bg="#FFF9E6")
                    return
                except Exception:
                    pass
                
                # Final fallback
                color = info.get("color", "#cccccc")
                info_image_label.config(image="", text=name, font=("Arial", 14, "bold"), fg="#ffffff", bg=color)

            if info_image_label.winfo_width() <= 1 or info_image_label.winfo_height() <= 1:
                info_image_label.after(50, do_render)
                def _on_cfg(e):
                    try:
                        info_image_label.unbind("<Configure>", _on_cfg_id)
                    except Exception:
                        pass
                    do_render()
                _on_cfg_id = info_image_label.bind("<Configure>", _on_cfg)
            else:
                do_render()
        else:
            color = info.get("color", "#cccccc")
            info_image_label.config(image="", text=name, font=("Arial", 14, "bold"), fg="#ffffff", bg=color)
    else:
        color = info.get("color", "#cccccc")
        info_image_label.config(image="", text=name, font=("Arial", 14, "bold"), fg="#ffffff", bg=color)

# ============================================================================
# SEARCH AND BUILDING INTERACTION
# ============================================================================


def on_search_click():
	"""Execute search query and display results."""
	query = search_bar.get()
	if query == "Search":
		query = ""
	results = perform_search(query)
	results_listbox.delete(0, tk.END)
	if not results:
		results_listbox.insert(tk.END, "No results found")
	else:
		for item in results:
			results_listbox.insert(tk.END, item)
		# Auto-show first result
		show_building_info(results[0])


def on_enter_pressed(event):
	"""Handle Enter key in search box."""
	on_search_click()


def on_result_double_click(event):
	"""Handle double-click on search result."""
	sel = results_listbox.curselection()
	if not sel:
		return
	item = results_listbox.get(sel[0])
	if item == "No results found":
		return
	show_building_info(item)


# Bind Return key after function is defined
search_bar.bind("<Return>", on_enter_pressed)

# Results listbox below the search box — adjusted for new layout
results_listbox = tk.Listbox(sidebar, font=("Arial", 12), bg="white", fg="black", highlightthickness=0, bd=1, relief=tk.SOLID)
results_listbox.place(relx=0.5, rely=0.58, anchor="n", relwidth=0.9, relheight=0.28)
results_listbox.insert(tk.END, "Type a query and press Enter")

results_listbox.bind("<Double-Button-1>", on_result_double_click)

# Add logout function and button under the search bar
def logout():
    """Ask user to confirm logout, restart the script and exit current process."""
    if not messagebox.askyesno("Exit", "Are you sure you want to return to the start screen?"):
        return
    try:
        # spawn a new process running this script, then exit current one
        script = os.path.abspath(__file__)
        subprocess.Popen([sys.executable, script], cwd=os.path.dirname(script))
    except Exception as e:
        messagebox.showerror("Restart Failed", f"Unable to restart application:\n{e}")
    finally:
        try:
            window.destroy()
        except Exception:
            pass
        sys.exit(0)

# red logout button placed under the results listbox
logout_btn = tk.Button(sidebar, text="Exit", command=logout, bg="#E53935", fg="white", font=("Arial", 12, "bold"))
logout_btn.place(relx=0.5, rely=0.90, anchor="center", relwidth=0.6)

# dynamic update routine to resize sidebar logo and adjust fonts if desired
def _on_main_window_resize(event=None):
    try:
        # always measure canvas size and draw; original_logo_img used if available
        cw = logo_canvas.winfo_width()
        ch = logo_canvas.winfo_height()
        if cw <= 1 or ch <= 1:
            logo_canvas.after(50, _on_main_window_resize)
            return

        # Use supersampling factor for anti-aliased circle edges
        SS = 4
        CIRCLE_FACTOR = 0.95  # larger circle to fill more space
        LOGO_FACTOR = 0.85    # logo takes up 85% of circle diameter for better readability

        diameter = int(min(cw, ch) * CIRCLE_FACTOR)
        logo_diameter = int(diameter * LOGO_FACTOR)

        # Coordinates for center on canvas (float -> int)
        cx = cw // 2
        cy = ch // 2

        try:
            # Use Pillow to render a smooth circular background and composite the logo
            from PIL import Image, ImageTk, ImageDraw

            # Create a transparent high-res canvas and draw a filled cream circle



            hr_w = max(1, cw * SS)
            hr_h = max(1, ch * SS)
            hr_img = Image.new("RGBA", (hr_w, hr_h), (0, 0, 0,  0))
            draw = ImageDraw.Draw(hr_img)

            # circle coords at high-res
            hr_dia = max(1, diameter * SS)
            hr_cx = hr_w // 2
            hr_cy = hr_h // 2
            left = hr_cx - hr_dia // 2
            top = hr_cy - hr_dia // 2
            right = left + hr_dia
            bottom = top + hr_dia

            draw.ellipse((left, top, right, bottom), fill=(255, 249, 230, 255))

            # Prepare logo: resize at high-res for better quality then paste centered (if available)
            try:
                if original_logo_img is not None:
                    logo_hr_dia = max(1, logo_diameter * SS)

                    logo_im = original_logo_img.copy().convert("RGBA")
                    w0, h0 = logo_im.size
                    # Scale to fit within the logo diameter while preserving aspect ratio
                    scale = min(logo_hr_dia / w0, logo_hr_dia / h0)
                    new_w = max(1, int(w0 * scale))
                    new_h = max(1, int(h0 * scale))
                    logo_resized = logo_im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    # Paste logo centered on the high-res circle
                    lx = hr_cx - new_w // 2
                    ly = hr_cy - new_h // 2
                    hr_img.paste(logo_resized, (lx, ly), logo_resized)
            except Exception:
                # if logo fails, leave circle only
                pass

            # Downsample to display size with LANCZOS for smooth edges
            final = hr_img.resize((cw, ch), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(final)
            logo_canvas.delete("all")
            logo_canvas.create_image(cx, cy, image=photo, anchor=tk.CENTER, tags=("logo_image",))
            logo_canvas.config(scrollregion=(0, 0, cw, ch))
            # keep reference to avoid GC
            logo_canvas.image = photo
            return
        except Exception:
            # Pillow not available or failed — fallback to canvas oval (original approach)
            pass

        # Fallback: draw simple oval (keeps previous visual if PIL isn't usable)
        logo_canvas.delete("all")
        half = diameter / 2
        left = cx - half
        top = cy - half
        right = cx + half
        bottom = cy + half
        logo_canvas.create_oval(left, top, right, bottom,
                                fill="#FFF9E6", outline="#cccccc", width=2, tags=("oval",))

        # draw the logo inside the circle using existing original_logo_img (resized via Pillow if available)
        try:
            from PIL import Image, ImageTk
            logo_diameter2 = int(diameter * 0.90)
            if original_logo_img is not None:
                w0, h0 = original_logo_img.size
                scale = min(logo_diameter2 / w0, logo_diameter2 / h0)
                new_w = max(1, int(w0 * scale))
                new_h = max(1, int(h0 * scale))
                im = original_logo_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(im)
                logo_canvas.create_image(cx, cy, image=photo, tags=("logo_image",), anchor=tk.CENTER)
                logo_canvas.image = photo
        except Exception:
            # final fallback: nothing else to draw
            pass
    except Exception:
        pass

# call once to set initial sizes, and bind to resize events
window.after(50, _on_main_window_resize)
window.bind("<Configure>", _on_main_window_resize)

# Load the map on startup (now load_campus_map is defined)
load_campus_map()
# schedule placeholder once the UI has settled so the image gets rendered
window.after(500, show_placeholder_info)

window.mainloop()
