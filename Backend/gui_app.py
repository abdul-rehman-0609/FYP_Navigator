"""
FYP Recommender System - Enhanced Professional GUI Application
Beautiful, modern interface with improved colors, fonts, and spacing.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional
from student_profile import StudentProfile, Proficiency, InterestLevel
from data_extractor import DataExtractor
from storage_manager import StorageManager
from fyp_recommender import FYPRecommender


class FYPRecommenderGUI:
    """Enhanced GUI application for FYP Recommender System."""
    
    # Modern Color Scheme
    COLORS = {
        'primary': '#2563EB',      # Blue
        'primary_dark': '#1E40AF',
        'secondary': '#8B5CF6',    # Purple
        'success': '#10B981',      # Green
        'danger': '#EF4444',       # Red
        'warning': '#F59E0B',      # Orange
        'bg': '#F8FAFC',          # Light gray
        'bg_dark': '#E2E8F0',
        'text': '#1E293B',
        'text_light': '#64748B',
        'white': '#FFFFFF',
        'border': '#CBD5E1'
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("FYP Recommender System - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.COLORS['bg'])
        
        # Initialize backend components
        self.data_extractor = DataExtractor()
        self.storage_manager = StorageManager()
        self.recommender = FYPRecommender()
        
        # Current student being edited
        self.current_student: Optional[StudentProfile] = None
        
        # Setup UI
        self._setup_modern_styles()
        self._create_header()
        self._create_menu()
        self._create_main_layout()
        self._create_status_bar()
        
        # Load initial data
        self._refresh_student_list()
    
    def _setup_modern_styles(self):
        """Configure modern, professional styling with larger fonts and better colors."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Frame
        style.configure("TFrame", background=self.COLORS['bg'])
        style.configure("Card.TFrame", background=self.COLORS['white'], 
                       relief=tk.RAISED, borderwidth=1)
        
        # Configure Labels
        style.configure("TLabel", 
                       background=self.COLORS['bg'],
                       foreground=self.COLORS['text'],
                       font=("Segoe UI", 11))
        
        style.configure("Title.TLabel",
                       font=("Segoe UI", 24, "bold"),
                       foreground=self.COLORS['primary'],
                       background=self.COLORS['bg'])
        
        style.configure("Subtitle.TLabel",
                       font=("Segoe UI", 12),
                       foreground=self.COLORS['text_light'],
                       background=self.COLORS['bg'])
        
        style.configure("Header.TLabel",
                       font=("Segoe UI", 14, "bold"),
                       foreground=self.COLORS['primary'],
                       background=self.COLORS['white'])
        
        style.configure("SectionLabel.TLabel",
                       font=("Segoe UI", 12, "bold"),
                       foreground=self.COLORS['text'],
                       background=self.COLORS['white'])
        
        # Configure Buttons
        style.configure("TButton",
                       font=("Segoe UI", 11),
                       padding=(15, 8))
        
        style.configure("Primary.TButton",
                       font=("Segoe UI", 12, "bold"),
                       padding=(20, 10))
        
        style.map("Primary.TButton",
                 background=[('active', self.COLORS['primary_dark'])])
        
        style.configure("Success.TButton",
                       font=("Segoe UI", 11, "bold"),
                       padding=(15, 8))
        
        style.configure("Danger.TButton",
                       font=("Segoe UI", 11),
                       padding=(15, 8))
        
        # Configure Entry and Combobox
        style.configure("TEntry", font=("Segoe UI", 11), padding=8)
        style.configure("TCombobox", font=("Segoe UI", 11), padding=8)
        style.configure("TSpinbox", font=("Segoe UI", 11), padding=8)
        
        # Configure LabelFrame
        style.configure("TLabelframe",
                       background=self.COLORS['white'],
                       borderwidth=2,
                       relief=tk.GROOVE)
        style.configure("TLabelframe.Label",
                       font=("Segoe UI", 13, "bold"),
                       foreground=self.COLORS['primary'],
                       background=self.COLORS['white'])
        
        # Configure Notebook (Tabs)
        style.configure("TNotebook",
                       background=self.COLORS['bg'],
                       borderwidth=0)
        style.configure("TNotebook.Tab",
                       font=("Segoe UI", 12, "bold"),
                       padding=(20, 12))
        style.map("TNotebook.Tab",
                 background=[('selected', self.COLORS['primary'])],
                 foreground=[('selected', self.COLORS['white'])])
        
        # Configure Treeview
        style.configure("Treeview",
                       font=("Segoe UI", 11),
                       rowheight=35,
                       background=self.COLORS['white'],
                       fieldbackground=self.COLORS['white'])
        style.configure("Treeview.Heading",
                       font=("Segoe UI", 12, "bold"),
                       background=self.COLORS['primary'],
                       foreground=self.COLORS['white'],
                       padding=10)
        style.map("Treeview.Heading",
                 background=[('active', self.COLORS['primary_dark'])])
    
    def _create_header(self):
        """Create beautiful header section."""
        header_frame = tk.Frame(self.root, bg=self.COLORS['primary'], height=100)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame,
                              text="🎓 FYP Recommender System",
                              font=("Segoe UI", 28, "bold"),
                              bg=self.COLORS['primary'],
                              fg=self.COLORS['white'])
        title_label.pack(pady=(20, 5))
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Intelligent Project Matching Powered by AI",
                                 font=("Segoe UI", 13),
                                 bg=self.COLORS['primary'],
                                 fg=self.COLORS['white'])
        subtitle_label.pack()
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root, font=("Segoe UI", 10))
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export All Data", command=self._export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_main_layout(self):
        """Create main tabbed interface with enhanced styling."""
        # Container for notebook
        notebook_container = tk.Frame(self.root, bg=self.COLORS['bg'])
        notebook_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self._create_add_student_tab()
        self._create_view_students_tab()
        self._create_recommendations_tab()
        self._create_history_tab()
    
    def _create_status_bar(self):
        """Create enhanced status bar at bottom."""
        status_frame = tk.Frame(self.root, bg=self.COLORS['primary_dark'], height=40)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("✓ Ready")
        
        status_label = tk.Label(status_frame,
                               textvariable=self.status_var,
                               bg=self.COLORS['primary_dark'],
                               fg=self.COLORS['white'],
                               font=("Segoe UI", 11),
                               anchor=tk.W,
                               padx=15)
        status_label.pack(fill=tk.BOTH, expand=True)
    
    # ==================== TAB 1: Add/Edit Student ====================
    
    def _create_add_student_tab(self):
        """Create the Add/Edit Student tab with enhanced design."""
        tab = tk.Frame(self.notebook, bg=self.COLORS['bg'])
        self.notebook.add(tab, text="➕ Add/Edit Student")
        
        # Create scrollable frame
        canvas = tk.Canvas(tab, bg=self.COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COLORS['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Basic Information Section
        basic_frame = ttk.LabelFrame(scrollable_frame, text="📋 Basic Information", padding=20)
        basic_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        
        # Student ID
        ttk.Label(basic_frame, text="Student ID:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w", pady=8, padx=5)
        self.student_id_var = tk.StringVar()
        id_entry = ttk.Entry(basic_frame, textvariable=self.student_id_var, width=35, font=("Segoe UI", 11))
        id_entry.grid(row=0, column=1, sticky="w", pady=8, padx=5)
        
        # Name
        ttk.Label(basic_frame, text="Full Name:", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", pady=8, padx=5)
        self.name_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.name_var, width=35, font=("Segoe UI", 11)).grid(
            row=1, column=1, sticky="w", pady=8, padx=5)
        
        # CGPA
        ttk.Label(basic_frame, text="CGPA:", font=("Segoe UI", 11, "bold")).grid(
            row=2, column=0, sticky="w", pady=8, padx=5)
        self.cgpa_var = tk.DoubleVar(value=3.0)
        cgpa_spinbox = ttk.Spinbox(basic_frame, from_=0.0, to=4.0, increment=0.1,
                                   textvariable=self.cgpa_var, width=33, font=("Segoe UI", 11))
        cgpa_spinbox.grid(row=2, column=1, sticky="w", pady=8, padx=5)
        
        # Major
        ttk.Label(basic_frame, text="Major:", font=("Segoe UI", 11, "bold")).grid(
            row=3, column=0, sticky="w", pady=8, padx=5)
        self.major_var = tk.StringVar()
        major_combo = ttk.Combobox(basic_frame, textvariable=self.major_var,
                                   values=self.data_extractor.get_majors(), width=33, font=("Segoe UI", 11))
        major_combo.grid(row=3, column=1, sticky="w", pady=8, padx=5)
        
        # Year
        ttk.Label(basic_frame, text="Year:", font=("Segoe UI", 11, "bold")).grid(
            row=4, column=0, sticky="w", pady=8, padx=5)
        self.year_var = tk.IntVar(value=4)
        year_combo = ttk.Combobox(basic_frame, textvariable=self.year_var,
                                 values=self.data_extractor.get_years(), width=33, font=("Segoe UI", 11))
        year_combo.grid(row=4, column=1, sticky="w", pady=8, padx=5)
        
        # Skills Section
        skills_frame = ttk.LabelFrame(scrollable_frame, text="💻 Technical Skills", padding=20)
        skills_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        
        ttk.Label(skills_frame, text="Select Skill:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w", pady=5)
        self.skill_var = tk.StringVar()
        skill_combo = ttk.Combobox(skills_frame, textvariable=self.skill_var,
                                   values=self.data_extractor.get_all_skills(), width=30, font=("Segoe UI", 11))
        skill_combo.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(skills_frame, text="Proficiency:", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", pady=5)
        self.skill_level_var = tk.StringVar(value="INTERMEDIATE")
        skill_level_combo = ttk.Combobox(skills_frame, textvariable=self.skill_level_var,
                                        values=self.data_extractor.get_proficiency_levels(), width=30, font=("Segoe UI", 11))
        skill_level_combo.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        add_skill_btn = ttk.Button(skills_frame, text="➕ Add Skill", command=self._add_skill, style="Success.TButton")
        add_skill_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Skills listbox with larger font
        self.skills_listbox = tk.Listbox(skills_frame, height=8, width=45, font=("Segoe UI", 11),
                                         bg=self.COLORS['white'], selectbackground=self.COLORS['primary'])
        self.skills_listbox.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Button(skills_frame, text="❌ Remove Selected", command=self._remove_skill, style="Danger.TButton").grid(
            row=4, column=0, columnspan=2, pady=5)
        
        # Interests Section
        interests_frame = ttk.LabelFrame(scrollable_frame, text="❤️ Interests & Domains", padding=20)
        interests_frame.grid(row=1, column=1, sticky="nsew", padx=15, pady=10)
        
        ttk.Label(interests_frame, text="Select Interest:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w", pady=5)
        self.interest_var = tk.StringVar()
        interest_combo = ttk.Combobox(interests_frame, textvariable=self.interest_var,
                                     values=self.data_extractor.get_all_domains(), width=30, font=("Segoe UI", 11))
        interest_combo.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(interests_frame, text="Interest Level:", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", pady=5)
        self.interest_level_var = tk.StringVar(value="HIGH")
        interest_level_combo = ttk.Combobox(interests_frame, textvariable=self.interest_level_var,
                                           values=self.data_extractor.get_interest_levels(), width=30, font=("Segoe UI", 11))
        interest_level_combo.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Button(interests_frame, text="➕ Add Interest", command=self._add_interest, style="Success.TButton").grid(
            row=2, column=0, columnspan=2, pady=10)
        
        # Interests listbox
        self.interests_listbox = tk.Listbox(interests_frame, height=8, width=45, font=("Segoe UI", 11),
                                           bg=self.COLORS['white'], selectbackground=self.COLORS['primary'])
        self.interests_listbox.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Button(interests_frame, text="❌ Remove Selected", command=self._remove_interest, style="Danger.TButton").grid(
            row=4, column=0, columnspan=2, pady=5)
        
        # Courses Section
        courses_frame = ttk.LabelFrame(scrollable_frame, text="📚 Completed Courses", padding=20)
        courses_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
        
        self.course_var = tk.StringVar()
        course_combo = ttk.Combobox(courses_frame, textvariable=self.course_var,
                                   values=self.data_extractor.get_all_courses(), width=35, font=("Segoe UI", 11))
        course_combo.grid(row=0, column=0, pady=5, padx=5)
        
        ttk.Button(courses_frame, text="➕ Add Course", command=self._add_course, style="Success.TButton").grid(
            row=1, column=0, pady=10)
        
        self.courses_listbox = tk.Listbox(courses_frame, height=8, width=45, font=("Segoe UI", 11),
                                         bg=self.COLORS['white'], selectbackground=self.COLORS['primary'])
        self.courses_listbox.grid(row=2, column=0, pady=5)
        
        ttk.Button(courses_frame, text="❌ Remove Selected", command=self._remove_course, style="Danger.TButton").grid(
            row=3, column=0, pady=5)
        
        # Preferences Section
        prefs_frame = ttk.LabelFrame(scrollable_frame, text="⚙️ Preferences", padding=20)
        prefs_frame.grid(row=2, column=1, sticky="nsew", padx=15, pady=10)
        
        ttk.Label(prefs_frame, text="Max Weekly Hours:", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w", pady=8, padx=5)
        self.max_hours_var = tk.IntVar(value=20)
        ttk.Spinbox(prefs_frame, from_=5, to=40, textvariable=self.max_hours_var, width=33, font=("Segoe UI", 11)).grid(
            row=0, column=1, pady=8, padx=5)
        
        ttk.Label(prefs_frame, text="Team Size:", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", pady=8, padx=5)
        self.team_size_var = tk.IntVar(value=1)
        ttk.Spinbox(prefs_frame, from_=1, to=5, textvariable=self.team_size_var, width=33, font=("Segoe UI", 11)).grid(
            row=1, column=1, pady=8, padx=5)
        
        ttk.Label(prefs_frame, text="Preferred Domains:", font=("Segoe UI", 11, "bold")).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=8, padx=5)
        
        self.domain_var = tk.StringVar()
        domain_combo = ttk.Combobox(prefs_frame, textvariable=self.domain_var,
                                   values=self.data_extractor.get_all_domains(), width=35, font=("Segoe UI", 11))
        domain_combo.grid(row=3, column=0, columnspan=2, pady=5, padx=5)
        
        ttk.Button(prefs_frame, text="➕ Add Domain", command=self._add_domain, style="Success.TButton").grid(
            row=4, column=0, columnspan=2, pady=10)
        
        self.domains_listbox = tk.Listbox(prefs_frame, height=5, width=45, font=("Segoe UI", 11),
                                         bg=self.COLORS['white'], selectbackground=self.COLORS['primary'])
        self.domains_listbox.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(prefs_frame, text="❌ Remove Selected", command=self._remove_domain, style="Danger.TButton").grid(
            row=6, column=0, columnspan=2, pady=5)
        
        # Action Buttons
        button_frame = tk.Frame(scrollable_frame, bg=self.COLORS['bg'])
        button_frame.grid(row=3, column=0, columnspan=2, pady=25)
        
        save_btn = ttk.Button(button_frame, text="💾 Save Student", style="Primary.TButton",
                             command=self._save_student)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear Form", command=self._clear_form)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        load_btn = ttk.Button(button_frame, text="📂 Load Student", command=self._load_student_dialog)
        load_btn.pack(side=tk.LEFT, padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # ==================== TAB 2: View Students ====================
    
    def _create_view_students_tab(self):
        """Create the View Students tab with enhanced design."""
        tab = tk.Frame(self.notebook, bg=self.COLORS['bg'])
        self.notebook.add(tab, text="👥 View Students")
        
        # Search frame
        search_frame = tk.Frame(tab, bg=self.COLORS['white'], relief=tk.RAISED, borderwidth=2)
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 12, "bold"),
                 background=self.COLORS['white']).pack(side=tk.LEFT, padx=15, pady=15)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._filter_students())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40, font=("Segoe UI", 12))
        search_entry.pack(side=tk.LEFT, padx=10, pady=15)
        
        # Students table
        table_frame = tk.Frame(tab, bg=self.COLORS['bg'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Create treeview
        columns = ("ID", "Name", "Major", "CGPA", "Year")
        self.students_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=200)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.students_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(tab, bg=self.COLORS['bg'])
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Button(button_frame, text="👁️ View Details", command=self._view_student_details).pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="✏️ Edit Student", command=self._edit_student, style="Success.TButton").pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="🗑️ Delete Student", command=self._delete_student, style="Danger.TButton").pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="🔄 Refresh", command=self._refresh_student_list).pack(side=tk.LEFT, padx=8)
    
    # ==================== TAB 3: Get Recommendations ====================
    
    def _create_recommendations_tab(self):
        """Create the Get Recommendations tab with enhanced design."""
        tab = tk.Frame(self.notebook, bg=self.COLORS['bg'])
        self.notebook.add(tab, text="🎯 Recommendations")
        
        # Selection frame
        select_frame = ttk.LabelFrame(tab, text="🎓 Select Student & Generate", padding=20)
        select_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(select_frame, text="Student:", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=10)
        self.rec_student_var = tk.StringVar()
        self.rec_student_combo = ttk.Combobox(select_frame, textvariable=self.rec_student_var, width=45, font=("Segoe UI", 11))
        self.rec_student_combo.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(select_frame, text="Count:", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=20)
        self.rec_count_var = tk.IntVar(value=5)
        ttk.Spinbox(select_frame, from_=1, to=10, textvariable=self.rec_count_var, width=10, font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(select_frame, text="✨ Generate Recommendations", style="Primary.TButton",
                  command=self._generate_recommendations).pack(side=tk.LEFT, padx=25)
        
        # Results frame
        results_frame = ttk.LabelFrame(tab, text="📊 Recommendation Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.rec_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=("Consolas", 11),
                                                  bg=self.COLORS['white'], fg=self.COLORS['text'])
        self.rec_text.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = tk.Frame(tab, bg=self.COLORS['bg'])
        action_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Button(action_frame, text="💾 Save to History", command=self._save_to_history, style="Success.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(action_frame, text="🗑️ Clear Results", command=lambda: self.rec_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=10)
    
    # ==================== TAB 4: History ====================
    
    def _create_history_tab(self):
        """Create the Recommendations History tab with enhanced design."""
        tab = tk.Frame(self.notebook, bg=self.COLORS['bg'])
        self.notebook.add(tab, text="📜 History")
        
        # Filter frame
        filter_frame = tk.Frame(tab, bg=self.COLORS['white'], relief=tk.RAISED, borderwidth=2)
        filter_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(filter_frame, text="Filter by Student:", font=("Segoe UI", 11, "bold"),
                 background=self.COLORS['white']).pack(side=tk.LEFT, padx=15, pady=15)
        self.history_filter_var = tk.StringVar()
        self.history_filter_combo = ttk.Combobox(filter_frame, textvariable=self.history_filter_var, width=35, font=("Segoe UI", 11))
        self.history_filter_combo.pack(side=tk.LEFT, padx=10, pady=15)
        
        ttk.Button(filter_frame, text="📋 Show All", command=lambda: self._load_history(None)).pack(side=tk.LEFT, padx=10)
        ttk.Button(filter_frame, text="🔍 Filter", command=lambda: self._load_history(self.history_filter_var.get()), style="Success.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(filter_frame, text="🗑️ Clear History", command=self._clear_history, style="Danger.TButton").pack(side=tk.LEFT, padx=20)
        
        # History display
        history_frame = tk.Frame(tab, bg=self.COLORS['bg'])
        history_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, font=("Consolas", 11),
                                                      bg=self.COLORS['white'], fg=self.COLORS['text'])
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Load initial history
        self._load_history()
    
    # ==================== Helper Methods (keeping existing logic) ====================
    
    def _add_skill(self):
        """Add skill to the listbox."""
        skill = self.skill_var.get().strip()
        level = self.skill_level_var.get()
        
        if not skill:
            messagebox.showwarning("Warning", "Please select a skill")
            return
        
        self.skills_listbox.insert(tk.END, f"{skill} ({level})")
        self.skill_var.set("")
        self.status_var.set(f"✓ Added skill: {skill}")
    
    def _remove_skill(self):
        """Remove selected skill from listbox."""
        selection = self.skills_listbox.curselection()
        if selection:
            self.skills_listbox.delete(selection)
            self.status_var.set("✓ Skill removed")
    
    def _add_interest(self):
        """Add interest to the listbox."""
        interest = self.interest_var.get().strip()
        level = self.interest_level_var.get()
        
        if not interest:
            messagebox.showwarning("Warning", "Please select an interest")
            return
        
        self.interests_listbox.insert(tk.END, f"{interest} ({level})")
        self.interest_var.set("")
        self.status_var.set(f"✓ Added interest: {interest}")
    
    def _remove_interest(self):
        """Remove selected interest from listbox."""
        selection = self.interests_listbox.curselection()
        if selection:
            self.interests_listbox.delete(selection)
            self.status_var.set("✓ Interest removed")
    
    def _add_course(self):
        """Add course to the listbox."""
        course = self.course_var.get().strip()
        
        if not course:
            messagebox.showwarning("Warning", "Please select a course")
            return
        
        self.courses_listbox.insert(tk.END, course)
        self.course_var.set("")
        self.status_var.set(f"✓ Added course: {course}")
    
    def _remove_course(self):
        """Remove selected course from listbox."""
        selection = self.courses_listbox.curselection()
        if selection:
            self.courses_listbox.delete(selection)
            self.status_var.set("✓ Course removed")
    
    def _add_domain(self):
        """Add preferred domain to the listbox."""
        domain = self.domain_var.get().strip()
        
        if not domain:
            messagebox.showwarning("Warning", "Please select a domain")
            return
        
        self.domains_listbox.insert(tk.END, domain)
        self.domain_var.set("")
        self.status_var.set(f"✓ Added domain: {domain}")
    
    def _remove_domain(self):
        """Remove selected domain from listbox."""
        selection = self.domains_listbox.curselection()
        if selection:
            self.domains_listbox.delete(selection)
            self.status_var.set("✓ Domain removed")
    
    def _save_student(self):
        """Save the current student profile."""
        # Validate basic info
        if not self.student_id_var.get().strip():
            messagebox.showerror("Error", "Student ID is required")
            return
        
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Name is required")
            return
        
        try:
            # Create student profile
            student = StudentProfile(
                student_id=self.student_id_var.get().strip(),
                name=self.name_var.get().strip(),
                cgpa=self.cgpa_var.get(),
                major=self.major_var.get(),
                year=self.year_var.get(),
                max_weekly_hours=self.max_hours_var.get(),
                team_size_preference=self.team_size_var.get()
            )
            
            # Add skills
            for i in range(self.skills_listbox.size()):
                item = self.skills_listbox.get(i)
                skill_name, level_str = item.rsplit(" (", 1)
                level_str = level_str.rstrip(")")
                student.add_skill(skill_name, Proficiency[level_str])
            
            # Add interests
            for i in range(self.interests_listbox.size()):
                item = self.interests_listbox.get(i)
                interest_name, level_str = item.rsplit(" (", 1)
                level_str = level_str.rstrip(")")
                student.add_interest(interest_name, InterestLevel[level_str])
            
            # Add courses
            for i in range(self.courses_listbox.size()):
                student.completed_courses.add(self.courses_listbox.get(i))
            
            # Add preferred domains
            for i in range(self.domains_listbox.size()):
                domain = self.domains_listbox.get(i)
                if domain not in student.preferred_domains:
                    student.preferred_domains.append(domain)
            
            # Save to storage
            if self.storage_manager.save_student(student):
                messagebox.showinfo("Success", f"✓ Student {student.name} saved successfully!")
                self.status_var.set(f"✓ Saved student: {student.student_id}")
                self._refresh_student_list()
                self._clear_form()
            else:
                messagebox.showerror("Error", "Failed to save student")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error saving student: {str(e)}")
    
    def _clear_form(self):
        """Clear all form fields."""
        self.student_id_var.set("")
        self.name_var.set("")
        self.cgpa_var.set(3.0)
        self.major_var.set("")
        self.year_var.set(4)
        self.max_hours_var.set(20)
        self.team_size_var.set(1)
        
        self.skills_listbox.delete(0, tk.END)
        self.interests_listbox.delete(0, tk.END)
        self.courses_listbox.delete(0, tk.END)
        self.domains_listbox.delete(0, tk.END)
        
        self.current_student = None
        self.status_var.set("✓ Form cleared")
    
    def _load_student_dialog(self):
        """Show dialog to load a student."""
        student_ids = self.storage_manager.get_all_student_ids()
        
        if not student_ids:
            messagebox.showinfo("Info", "No students saved yet")
            return
        
        # Create simple dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Student")
        dialog.geometry("400x200")
        dialog.configure(bg=self.COLORS['bg'])
        
        ttk.Label(dialog, text="Select Student ID:", font=("Segoe UI", 12, "bold")).pack(pady=20)
        
        student_var = tk.StringVar()
        combo = ttk.Combobox(dialog, textvariable=student_var, values=student_ids, width=35, font=("Segoe UI", 11))
        combo.pack(pady=15)
        
        def load():
            sid = student_var.get()
            if sid:
                self._load_student_to_form(sid)
                dialog.destroy()
        
        ttk.Button(dialog, text="Load", command=load, style="Primary.TButton").pack(pady=15)
    
    def _load_student_to_form(self, student_id: str):
        """Load a student profile into the form."""
        student = self.storage_manager.load_student(student_id)
        
        if not student:
            messagebox.showerror("Error", f"Student {student_id} not found")
            return
        
        # Clear form first
        self._clear_form()
        
        # Load basic info
        self.student_id_var.set(student.student_id)
        self.name_var.set(student.name)
        self.cgpa_var.set(student.cgpa)
        self.major_var.set(student.major)
        self.year_var.set(student.year)
        self.max_hours_var.set(student.max_weekly_hours)
        self.team_size_var.set(student.team_size_preference)
        
        # Load skills
        for skill_name, level in student.skills.items():
            self.skills_listbox.insert(tk.END, f"{skill_name} ({level.name})")
        
        # Load interests
        for interest_name, level in student.interests.items():
            self.interests_listbox.insert(tk.END, f"{interest_name} ({level.name})")
        
        # Load courses
        for course in student.completed_courses:
            self.courses_listbox.insert(tk.END, course)
        
        # Load domains
        for domain in student.preferred_domains:
            self.domains_listbox.insert(tk.END, domain)
        
        self.current_student = student
        self.status_var.set(f"✓ Loaded student: {student.name}")
    
    def _refresh_student_list(self):
        """Refresh the student list in View Students tab."""
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Load all students
        students = self.storage_manager.load_all_students()
        
        for student in students.values():
            self.students_tree.insert("", tk.END, values=(
                student.student_id,
                student.name,
                student.major,
                f"{student.cgpa:.2f}",
                student.year
            ))
        
        # Update recommendation combo
        student_list = [f"{s.student_id} - {s.name}" for s in students.values()]
        self.rec_student_combo['values'] = student_list
        self.history_filter_combo['values'] = student_list
        
        self.status_var.set(f"✓ Loaded {len(students)} students")
    
    def _filter_students(self):
        """Filter students based on search text."""
        search_text = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Load and filter students
        students = self.storage_manager.load_all_students()
        
        for student in students.values():
            if (search_text in student.student_id.lower() or 
                search_text in student.name.lower() or
                search_text in student.major.lower()):
                self.students_tree.insert("", tk.END, values=(
                    student.student_id,
                    student.name,
                    student.major,
                    f"{student.cgpa:.2f}",
                    student.year
                ))
    
    def _view_student_details(self):
        """View detailed information about selected student."""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student")
            return
        
        item = self.students_tree.item(selection[0])
        student_id = item['values'][0]
        
        student = self.storage_manager.load_student(student_id)
        if not student:
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Student Details - {student.name}")
        details_window.geometry("700x600")
        details_window.configure(bg=self.COLORS['bg'])
        
        text = scrolledtext.ScrolledText(details_window, wrap=tk.WORD, font=("Consolas", 11),
                                        bg=self.COLORS['white'], fg=self.COLORS['text'])
        text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Format details
        details = f"""
STUDENT PROFILE
{'=' * 70}

Basic Information:
  Student ID: {student.student_id}
  Name: {student.name}
  Major: {student.major}
  CGPA: {student.cgpa:.2f}
  Year: {student.year}

Skills:
"""
        for skill, level in student.skills.items():
            details += f"  • {skill}: {level.name}\n"
        
        details += "\nInterests:\n"
        for interest, level in student.interests.items():
            details += f"  • {interest}: {level.name}\n"
        
        details += "\nCompleted Courses:\n"
        for course in sorted(student.completed_courses):
            details += f"  • {course}\n"
        
        details += f"\nPreferred Domains:\n"
        for domain in student.preferred_domains:
            details += f"  • {domain}\n"
        
        details += f"""
Preferences:
  Max Weekly Hours: {student.max_weekly_hours}
  Team Size Preference: {student.team_size_preference}
"""
        
        text.insert(1.0, details)
        text.config(state=tk.DISABLED)
    
    def _edit_student(self):
        """Edit selected student."""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student")
            return
        
        item = self.students_tree.item(selection[0])
        student_id = item['values'][0]
        
        # Switch to Add/Edit tab and load student
        self.notebook.select(0)
        self._load_student_to_form(student_id)
    
    def _delete_student(self):
        """Delete selected student."""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student")
            return
        
        item = self.students_tree.item(selection[0])
        student_id = item['values'][0]
        student_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?"):
            if self.storage_manager.delete_student(student_id):
                messagebox.showinfo("Success", f"✓ Student {student_name} deleted")
                self._refresh_student_list()
            else:
                messagebox.showerror("Error", "Failed to delete student")
    
    def _generate_recommendations(self):
        """Generate recommendations for selected student."""
        student_info = self.rec_student_var.get()
        
        if not student_info:
            messagebox.showwarning("Warning", "Please select a student")
            return
        
        # Extract student ID
        student_id = student_info.split(" - ")[0]
        student = self.storage_manager.load_student(student_id)
        
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
        
        # Generate recommendations
        self.rec_text.delete(1.0, tk.END)
        self.rec_text.insert(1.0, "⏳ Generating recommendations...\n\n")
        self.root.update()
        
        try:
            report = self.recommender.get_recommendations_for_student(
                student, 
                top_n=self.rec_count_var.get()
            )
            
            self.rec_text.delete(1.0, tk.END)
            self.rec_text.insert(1.0, report)
            
            self.status_var.set(f"✓ Generated recommendations for {student.name}")
            
            # Store current recommendations for saving
            self.current_recommendations = report
            self.current_rec_student = student
        
        except Exception as e:
            self.rec_text.delete(1.0, tk.END)
            self.rec_text.insert(1.0, f"❌ Error generating recommendations:\n{str(e)}")
    
    def _save_to_history(self):
        """Save current recommendations to history."""
        if not hasattr(self, 'current_recommendations') or not self.current_recommendations:
            messagebox.showwarning("Warning", "No recommendations to save")
            return
        
        messagebox.showinfo("Info", "✓ Recommendations saved to history")
        self._load_history()
        self.status_var.set("✓ Saved to history")
    
    def _load_history(self, student_id: Optional[str] = None):
        """Load recommendation history."""
        self.history_text.delete(1.0, tk.END)
        
        history = self.storage_manager.load_recommendation_history(student_id)
        
        if not history:
            self.history_text.insert(1.0, "No recommendation history found.")
            return
        
        output = "RECOMMENDATION HISTORY\n"
        output += "=" * 90 + "\n\n"
        
        for i, entry in enumerate(reversed(history), 1):
            output += f"Entry #{i}\n"
            output += f"Date: {entry['timestamp']}\n"
            output += f"Student: {entry['student_name']} ({entry['student_id']})\n"
            output += f"ML Used: {'Yes' if entry.get('ml_used', False) else 'No'}\n"
            output += f"Recommendations: {len(entry['recommendations'])}\n"
            
            for rec in entry['recommendations']:
                output += f"  • {rec.get('title', 'N/A')} (Score: {rec.get('score', 0):.2f})\n"
            
            output += "\n" + "-" * 90 + "\n\n"
        
        self.history_text.insert(1.0, output)
        self.status_var.set(f"✓ Loaded {len(history)} history entries")
    
    def _clear_history(self):
        """Clear all recommendation history."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            self.storage_manager.clear_history()
            self._load_history()
            messagebox.showinfo("Success", "✓ History cleared")
            self.status_var.set("✓ History cleared")
    
    def _export_data(self):
        """Export all data to file."""
        filename = self.storage_manager.export_all_data()
        messagebox.showinfo("Success", f"✓ Data exported to:\n{filename}")
        self.status_var.set(f"✓ Data exported")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """
FYP Recommender System
Version 2.0 - Enhanced Edition

A professional application for managing student profiles
and generating intelligent FYP topic recommendations.

Features:
• Beautiful, modern interface
• Persistent data storage
• AI-powered recommendations
• ML fallback system
• Comprehensive history tracking

© 2025 FYP Recommender Team
"""
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = FYPRecommenderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
