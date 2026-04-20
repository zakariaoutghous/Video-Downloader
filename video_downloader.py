#!/usr/bin/env python3
"""
Video Downloader - YouTube & Video Downloader
A premium desktop application with modern UI and professional features
Version: 3.0 - Complete UI Redesign
"""

import sys
import os
import threading
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar,
    QTextEdit, QFileDialog, QGroupBox, QFrame, QCheckBox,
    QMessageBox, QListWidget, QListWidgetItem, QSplitter,
    QGraphicsOpacityEffect, QSpacerItem, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import (
    Qt, pyqtSignal, QObject, QSize, QThread, QPropertyAnimation,
    QEasingCurve, QRect, QPoint, QTimer, QParallelAnimationGroup
)
from PyQt5.QtGui import (
    QFont, QIcon, QPixmap, QPalette, QColor, QLinearGradient,
    QBrush, QPainter, QMovie, QFontDatabase, QCursor, QPainterPath,
    QPen
)

import yt_dlp
import requests
from io import BytesIO

# ==================== MODERN STYLESHEET ====================
MODERN_STYLE = """
/* Global Styles */
* {
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

QMainWindow {
    background-color: #0A0E27;
}

QWidget {
    background-color: transparent;
    color: #E2E8F0;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #1A1F3A;
    width: 8px;
    border-radius: 4px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #4A5568;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #7C8BFF;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Cards */
QFrame#card {
    background-color: #11162E;
    border-radius: 16px;
    border: 1px solid rgba(124, 139, 255, 0.1);
}

/* Labels */
QLabel {
    color: #E2E8F0;
}

QLabel#cardTitle {
    font-size: 18px;
    font-weight: 700;
    color: #7C8BFF;
    letter-spacing: 0.5px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(124, 139, 255, 0.2);
}

QLabel#infoLabel {
    font-size: 13px;
    color: #A0AEC0;
}

QLabel#infoValue {
    font-size: 14px;
    font-weight: 600;
    color: #E2E8F0;
}

/* Line Edits */
QLineEdit {
    background-color: #0F1428;
    border: 2px solid #1F253E;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 14px;
    color: #E2E8F0;
    selection-background-color: #7C8BFF;
}

QLineEdit:focus {
    border-color: #7C8BFF;
    background-color: #0D1225;
}

QLineEdit:hover {
    border-color: #4A5568;
}

/* Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7C8BFF, stop:1 #5A67D8);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 28px;
    font-size: 14px;
    font-weight: 600;
    min-height: 48px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8B9AFF, stop:1 #6B77E8);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6B77E8, stop:1 #4A57C8);
}

QPushButton:disabled {
    background: #2D3748;
    color: #718096;
}

QPushButton#downloadButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #48BB78, stop:1 #38A169);
    font-size: 16px;
    padding: 16px 32px;
    min-height: 52px;
}

QPushButton#downloadButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5FD489, stop:1 #48BB78);
}

QPushButton#secondaryButton {
    background: rgba(124, 139, 255, 0.15);
    border: 1px solid rgba(124, 139, 255, 0.3);
}

QPushButton#secondaryButton:hover {
    background: rgba(124, 139, 255, 0.25);
    border-color: rgba(124, 139, 255, 0.5);
}

/* Combo Box */
QComboBox {
    background-color: #0F1428;
    border: 2px solid #1F253E;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 13px;
    color: #E2E8F0;
    min-width: 140px;
}

QComboBox:hover {
    border-color: #4A5568;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #7C8BFF;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #0F1428;
    border: 1px solid #1F253E;
    border-radius: 12px;
    padding: 5px;
    selection-background-color: #7C8BFF;
}

/* Checkbox */
QCheckBox {
    spacing: 12px;
    font-size: 14px;
    font-weight: 500;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid #4A5568;
    background-color: #0F1428;
}

QCheckBox::indicator:checked {
    background-color: #7C8BFF;
    border-color: #7C8BFF;
}

QCheckBox::indicator:hover {
    border-color: #7C8BFF;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 12px;
    text-align: center;
    background-color: #1A1F3A;
    height: 44px;
    font-size: 14px;
    font-weight: 700;
    color: #E2E8F0;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7C8BFF, stop:0.5 #48BB78, stop:1 #7C8BFF);
    border-radius: 12px;
}

/* Text Edit */
QTextEdit {
    background-color: #0F1428;
    border: 1px solid #1F253E;
    border-radius: 12px;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    padding: 12px;
    color: #E2E8F0;
}

QTextEdit:focus {
    border-color: #7C8BFF;
}

/* List Widget */
QListWidget {
    background-color: #0F1428;
    border: 1px solid #1F253E;
    border-radius: 12px;
    outline: none;
    padding: 8px;
}

QListWidget::item {
    padding: 12px;
    border-radius: 10px;
    margin: 4px 0px;
}

QListWidget::item:selected {
    background-color: #7C8BFF;
    color: white;
}

QListWidget::item:hover:!selected {
    background-color: #1A1F3A;
}

/* Thumbnail */
QLabel#thumbnail {
    border-radius: 12px;
    background-color: #0F1428;
    border: 2px solid #1F253E;
}

/* Folder Label */
QLabel#folderPath {
    background-color: #0F1428;
    border: 1px solid #1F253E;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 12px;
    font-family: monospace;
}
"""

# ==================== CUSTOM WIDGETS ====================
class ModernCard(QFrame):
    """Modern card widget with shadow and rounded corners"""
    
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameStyle(QFrame.NoFrame)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            layout.addWidget(title_label)
            
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(12)
        layout.addLayout(self.content_layout)
        
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)
        
    def add_layout(self, layout):
        self.content_layout.addLayout(layout)


class IconLabel(QWidget):
    """Widget with icon and text"""
    
    def __init__(self, icon_text, label_text, value_text=""):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        icon = QLabel(icon_text)
        icon.setStyleSheet("font-size: 18px;")
        layout.addWidget(icon)
        
        label = QLabel(label_text)
        label.setObjectName("infoLabel")
        label.setMinimumWidth(80)
        layout.addWidget(label)
        
        self.value = QLabel(value_text if value_text else "-")
        self.value.setObjectName("infoValue")
        layout.addWidget(self.value)
        layout.addStretch()
        
    def set_value(self, text):
        self.value.setText(text)


class ModernLogo(QWidget):
    """Modern logo widget with gradient circle and video camera + download arrow"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 52)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw gradient circle background
        rect = self.rect()
        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0, QColor(124, 139, 255))  # #7C8BFF - Blue
        gradient.setColorAt(1, QColor(72, 187, 120))   # #48BB78 - Green
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)
        
        # Draw video camera body
        painter.setPen(QPen(QColor(255, 255, 255), 2.5))
        painter.setBrush(Qt.NoBrush)
        
        # Camera body (rounded rectangle)
        camera_rect = QRect(rect.center().x() - 14, rect.center().y() - 8, 28, 18)
        painter.drawRoundedRect(camera_rect, 4, 4)
        
        # Camera lens (circle)
        lens_center = QPoint(rect.center().x() - 4, rect.center().y())
        painter.drawEllipse(lens_center, 4, 4)
        
        # Camera flash (small circle)
        flash_center = QPoint(rect.center().x() + 8, rect.center().y() - 4)
        painter.drawEllipse(flash_center, 2, 2)
        
        # Download arrow below camera
        arrow_start = rect.center().x()
        arrow_mid = rect.center().y() + 12
        arrow_bottom = rect.center().y() + 18
        
        # Arrow line
        painter.drawLine(arrow_start, arrow_mid, arrow_start, arrow_bottom - 3)
        
        # Arrow head
        arrow_size = 5
        points = [
            QPoint(arrow_start - arrow_size, arrow_bottom - arrow_size),
            QPoint(arrow_start + arrow_size, arrow_bottom - arrow_size),
            QPoint(arrow_start, arrow_bottom)
        ]
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawPolygon(points)


# ==================== WORKER THREADS ====================
class DownloadWorker(QThread):
    """Advanced download worker with progress tracking"""
    progress_update = pyqtSignal(float)
    status_update = pyqtSignal(str)
    speed_update = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, url, download_path, quality, is_audio_only=False):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self.quality = quality
        self.is_audio_only = is_audio_only
        
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if d.get('total_bytes'):
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.progress_update.emit(percent)
            elif d.get('total_bytes_estimate'):
                percent = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
                self.progress_update.emit(percent)
            
            if d.get('speed'):
                speed = d['speed'] / 1024 / 1024
                self.speed_update.emit(f"⚡ {speed:.2f} MB/s")
                
        elif d['status'] == 'finished':
            self.status_update.emit("🎬 Processing and converting...")
            
    def run(self):
        try:
            if self.is_audio_only:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                }
            else:
                quality_map = {
                    '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]',
                    '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]',
                    '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]',
                    '4K': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160]',
                    'Best': 'bestvideo+bestaudio/best',
                }
                
                ydl_opts = {
                    'format': quality_map.get(self.quality, 'best'),
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                    'merge_output_format': 'mp4',
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_update.emit("🚀 Starting download...")
                ydl.download([self.url])
                
            self.finished.emit(True, "✨ Download completed successfully!")
            
        except Exception as e:
            self.finished.emit(False, f"❌ Error: {str(e)}")


class VideoInfoFetcher(QThread):
    """Enhanced video info fetcher"""
    info_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        
    def run(self):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
                video_info = {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'views': info.get('view_count', 0),
                    'likes': info.get('like_count', 0),
                    'description': info.get('description', '')[:200],
                }
                
                formats = []
                for f in info.get('formats', []):
                    if f.get('height'):
                        height = f.get('height')
                        if height and height <= 2160:
                            formats.append(f)
                
                video_info['available_qualities'] = sorted(
                    set([f.get('height') for f in formats if f.get('height')]),
                    reverse=True
                )
                
                self.info_ready.emit(video_info)
                
        except Exception as e:
            self.error_occurred.emit(f"Failed to fetch video info: {str(e)}")


# ==================== MAIN APPLICATION ====================
class VideoDownloader(QMainWindow):
    """Professional Video Downloader Main Window - Redesigned"""
    
    def __init__(self):
        super().__init__()
        self.download_path = str(Path.home() / "Downloads" / "VideoDownloader")
        os.makedirs(self.download_path, exist_ok=True)
        self.current_video_info = None
        self.download_worker = None
        self.info_fetcher = None
        self.init_ui()
        self.setup_shortcuts()
        self.apply_window_animation()
        
    def init_ui(self):
        """Initialize the redesigned user interface"""
        self.setWindowTitle("Video Downloader")
        self.setGeometry(100, 100, 1300, 850)
        self.setMinimumSize(900, 600)
        
        # Apply modern style
        self.setStyleSheet(MODERN_STYLE)
        
        # Central widget with scroll area
        central_scroll = QScrollArea()
        central_scroll.setWidgetResizable(True)
        central_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        central_widget = QWidget()
        central_scroll.setWidget(central_widget)
        self.setCentralWidget(central_scroll)
        
        # Main layout with responsive spacing
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(28)
        
        # Header
        self.create_header(main_layout)
        
        # Responsive content container
        self.content_container = QWidget()
        self.content_layout = QHBoxLayout(self.content_container)
        self.content_layout.setSpacing(28)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.content_container)
        
        # Left column (Main content)
        self.left_column = QWidget()
        self.left_layout = QVBoxLayout(self.left_column)
        self.left_layout.setSpacing(28)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create all cards
        self.create_url_card(self.left_layout)
        self.create_video_info_card(self.left_layout)
        self.create_settings_card(self.left_layout)
        self.create_action_buttons(self.left_layout)
        self.create_progress_card(self.left_layout)
        
        self.content_layout.addWidget(self.left_column, stretch=2)
        
        # Right column (History sidebar)
        self.right_column = QWidget()
        self.right_layout = QVBoxLayout(self.right_column)
        self.right_layout.setSpacing(28)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.create_history_card(self.right_layout)
        
        self.content_layout.addWidget(self.right_column, stretch=1)
        
        # Setup responsive layout
        self.setup_responsive_layout()
        
        # Status bar
        self.setup_status_bar()
        
    def setup_responsive_layout(self):
        """Make layout responsive - switches to vertical on narrow windows"""
        def adjust_layout():
            if self.width() < 950:
                # Switch to vertical layout
                if not hasattr(self, '_is_vertical') or not self._is_vertical:
                    # Remove widgets from layout
                    self.content_layout.removeWidget(self.left_column)
                    self.content_layout.removeWidget(self.right_column)
                    
                    # Change to vertical
                    self.content_layout.setDirection(QHBoxLayout.LeftToRight)
                    
                    # Create new vertical layout
                    self.vertical_container = QWidget()
                    self.vertical_layout = QVBoxLayout(self.vertical_container)
                    self.vertical_layout.setSpacing(28)
                    self.vertical_layout.setContentsMargins(0, 0, 0, 0)
                    
                    # Add widgets vertically
                    self.vertical_layout.addWidget(self.left_column)
                    self.vertical_layout.addWidget(self.right_column)
                    
                    # Add to main layout
                    self.content_layout.addWidget(self.vertical_container)
                    self._is_vertical = True
            else:
                # Switch to horizontal layout
                if hasattr(self, '_is_vertical') and self._is_vertical:
                    # Remove vertical container
                    self.content_layout.removeWidget(self.vertical_container)
                    self.vertical_container.deleteLater()
                    
                    # Add widgets horizontally
                    self.content_layout.addWidget(self.left_column, 2)
                    self.content_layout.addWidget(self.right_column, 1)
                    self._is_vertical = False
        
        def resize_event(event):
            adjust_layout()
            QMainWindow.resizeEvent(self, event)
        
        self.resizeEvent = resize_event
        adjust_layout()
        
    def create_header(self, parent_layout):
        """Create modern header with logo and title"""
        header_container = QWidget()
        header_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(124, 139, 255, 0.08), stop:1 rgba(72, 187, 120, 0.04));
            border-radius: 20px;
            margin-bottom: 8px;
        """)
        
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(28, 24, 28, 24)
        header_layout.setSpacing(20)
        
        # Modern Logo
        self.logo = ModernLogo()
        self.logo.setFixedSize(60, 60)   # تكبير اللوغو شوية
        header_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Title container
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(4)
        title_layout.setAlignment(Qt.AlignCenter)

        # Application Title
        title_label = QLabel("Video Downloader")
        title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 0.5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        header_layout.addWidget(title_container, alignment=Qt.AlignCenter)

        # Spacer باش الاسم يبقى فالنص
        header_layout.addStretch()
        header_layout.addStretch()
        
        parent_layout.addWidget(header_container)
        
    def create_url_card(self, parent_layout):
        """Create URL input card"""
        card = ModernCard("📎 Video URL")
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.url_input.setMinimumHeight(52)
        self.url_input.returnPressed.connect(self.fetch_video_info)
        
        card.add_widget(self.url_input)
        parent_layout.addWidget(card)
        
    def create_video_info_card(self, parent_layout):
        """Create video information card"""
        card = ModernCard("🎬 Video Information")
        
        # Thumbnail and basic info
        info_container = QWidget()
        info_layout = QHBoxLayout(info_container)
        info_layout.setSpacing(24)
        
        # Thumbnail
        thumb_container = QWidget()
        thumb_container.setFixedSize(240, 135)
        thumb_layout = QVBoxLayout(thumb_container)
        thumb_layout.setContentsMargins(0, 0, 0, 0)
        
        self.thumbnail_label = QLabel("🎬")
        self.thumbnail_label.setObjectName("thumbnail")
        self.thumbnail_label.setFixedSize(240, 135)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setStyleSheet("font-size: 48px;")
        thumb_layout.addWidget(self.thumbnail_label)
        
        info_layout.addWidget(thumb_container)
        
        # Details grid
        details_container = QWidget()
        details_layout = QVBoxLayout(details_container)
        details_layout.setSpacing(10)
        
        self.title_label = IconLabel("📝", "Title:")
        details_layout.addWidget(self.title_label)
        
        self.duration_label = IconLabel("⏱️", "Duration:")
        details_layout.addWidget(self.duration_label)
        
        self.uploader_label = IconLabel("👤", "Uploader:")
        details_layout.addWidget(self.uploader_label)
        
        self.views_label = IconLabel("👁️", "Views:")
        details_layout.addWidget(self.views_label)
        
        self.likes_label = IconLabel("❤️", "Likes:")
        details_layout.addWidget(self.likes_label)
        
        info_layout.addWidget(details_container, stretch=1)
        
        card.add_widget(info_container)
        parent_layout.addWidget(card)
        
    def create_settings_card(self, parent_layout):
        """Create download settings card"""
        card = ModernCard("⚙️ Download Settings")
        
        # Quality selector
        quality_container = QWidget()
        quality_layout = QHBoxLayout(quality_container)
        quality_layout.setSpacing(15)
        
        quality_icon = QLabel("🎞️")
        quality_icon.setStyleSheet("font-size: 18px;")
        quality_layout.addWidget(quality_icon)
        
        quality_label = QLabel("Video Quality:")
        quality_label.setObjectName("infoLabel")
        quality_label.setMinimumWidth(100)
        quality_layout.addWidget(quality_label)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(['1080p', '720p', '360p', '4K', 'Best'])
        self.quality_combo.setCurrentIndex(0)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        
        card.add_widget(quality_container)
        
        # Audio only
        self.audio_checkbox = QCheckBox("🎵 Download as MP3 (Audio Only)")
        self.audio_checkbox.toggled.connect(self.on_audio_toggle)
        card.add_widget(self.audio_checkbox)
        
        # Folder selection
        folder_container = QWidget()
        folder_layout = QHBoxLayout(folder_container)
        folder_layout.setSpacing(15)
        
        folder_icon = QLabel("📁")
        folder_icon.setStyleSheet("font-size: 18px;")
        folder_layout.addWidget(folder_icon)
        
        folder_label = QLabel("Save to:")
        folder_label.setObjectName("infoLabel")
        folder_label.setMinimumWidth(100)
        folder_layout.addWidget(folder_label)
        
        self.folder_label = QLabel(self.download_path)
        self.folder_label.setObjectName("folderPath")
        self.folder_label.setWordWrap(True)
        folder_layout.addWidget(self.folder_label, stretch=1)
        
        self.browse_btn = QPushButton("📂 Browse")
        self.browse_btn.setObjectName("secondaryButton")
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_btn)
        
        card.add_widget(folder_container)
        parent_layout.addWidget(card)
        
    def create_action_buttons(self, parent_layout):
        """Create action buttons"""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)
        
        self.fetch_btn = QPushButton("🔍 Fetch Info")
        self.fetch_btn.setMinimumHeight(52)
        self.fetch_btn.clicked.connect(self.fetch_video_info)
        button_layout.addWidget(self.fetch_btn, 1)
        
        self.download_btn = QPushButton("⬇ Download")
        self.download_btn.setObjectName("downloadButton")
        self.download_btn.setEnabled(False)
        self.download_btn.setMinimumHeight(52)
        self.download_btn.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_btn, 1)
        
        parent_layout.addWidget(button_container)
        
    def create_progress_card(self, parent_layout):
        """Create download progress card"""
        card = ModernCard("📊 Download Progress")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setMinimumHeight(44)
        card.add_widget(self.progress_bar)
        
        self.speed_label = QLabel("")
        self.speed_label.setStyleSheet("color: #48BB78; font-size: 13px; font-weight: 600;")
        self.speed_label.setAlignment(Qt.AlignCenter)
        card.add_widget(self.speed_label)
        
        parent_layout.addWidget(card)
        
    def create_history_card(self, parent_layout):
        """Create download history card"""
        card = ModernCard("📜 Download History")
        
        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(300)
        self.history_list.itemDoubleClicked.connect(self.reuse_from_history)
        card.add_widget(self.history_list)
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.setMinimumHeight(44)
        clear_btn.clicked.connect(self.clear_history)
        card.add_widget(clear_btn)
        
        parent_layout.addWidget(card)
        
    def setup_status_bar(self):
        """Setup modern status bar"""
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C8BFF, stop:1 #5A67D8);
                color: white;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        self.statusBar().showMessage("🚀 Ready to download videos")
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        
        QShortcut(QKeySequence("Ctrl+D"), self, self.start_download)
        QShortcut(QKeySequence("Ctrl+B"), self, self.browse_folder)
        
    def apply_window_animation(self):
        """Apply fade-in animation to window"""
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_animation.start()
        
    def on_audio_toggle(self, checked):
        """Handle audio only toggle"""
        self.quality_combo.setEnabled(not checked)
        if checked:
            self.log_message("🎵 Audio mode activated - Downloading as MP3 (320kbps)")
        else:
            self.log_message("🎬 Video mode activated")
            
    def browse_folder(self):
        """Open folder browser"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder",
            self.download_path
        )
        if folder:
            self.download_path = folder
            self.folder_label.setText(folder)
            self.log_message(f"📁 Download folder changed to: {folder}")
            
    def fetch_video_info(self):
        """Fetch video information"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a video URL")
            return
            
        self.fetch_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.log_message("🔍 Fetching video information...")
        
        self.info_fetcher = VideoInfoFetcher(url)
        self.info_fetcher.info_ready.connect(self.on_info_ready)
        self.info_fetcher.error_occurred.connect(self.on_info_error)
        self.info_fetcher.start()
        
    def on_info_ready(self, info):
        """Handle video info loaded"""
        self.current_video_info = info
        
        # Update labels
        self.title_label.set_value(info['title'][:100])
        
        duration = info['duration']
        minutes = duration // 60
        seconds = duration % 60
        self.duration_label.set_value(f"{minutes}:{seconds:02d}")
        
        self.uploader_label.set_value(info['uploader'])
        self.views_label.set_value(f"{info['views']:,}")
        
        if info.get('likes'):
            self.likes_label.set_value(f"{info['likes']:,}")
        
        # Update quality options
        if info.get('available_qualities'):
            current_quality = self.quality_combo.currentText()
            self.quality_combo.clear()
            qualities = []
            for q in info['available_qualities']:
                if q <= 360:
                    qualities.append('360p')
                elif q <= 720:
                    qualities.append('720p')
                elif q <= 1080:
                    qualities.append('1080p')
                elif q <= 2160:
                    qualities.append('4K')
            qualities.append('Best')
            
            qualities = list(dict.fromkeys(qualities))
            self.quality_combo.addItems(qualities)
            
            if current_quality in qualities:
                self.quality_combo.setCurrentText(current_quality)
        
        # Load thumbnail
        if info['thumbnail']:
            self.load_thumbnail(info['thumbnail'])
        
        self.download_btn.setEnabled(True)
        self.log_message(f"✅ Video info loaded: {info['title']}")
        self.fetch_btn.setEnabled(True)
        self.statusBar().showMessage(f"Ready to download: {info['title'][:50]}...", 3000)
        
    def load_thumbnail(self, url):
        """Load thumbnail from URL"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                scaled = pixmap.scaled(240, 135, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.thumbnail_label.setPixmap(scaled)
                self.thumbnail_label.setText("")
        except Exception as e:
            self.log_message(f"⚠️ Could not load thumbnail: {str(e)}")
            
    def on_info_error(self, error):
        """Handle info fetch error"""
        self.log_message(f"❌ {error}")
        QMessageBox.critical(self, "Error", error)
        self.fetch_btn.setEnabled(True)
        
    def start_download(self):
        """Start the download process"""
        if not self.current_video_info:
            QMessageBox.warning(self, "Warning", "Please fetch video information first")
            return
            
        url = self.url_input.text().strip()
        quality = self.quality_combo.currentText()
        is_audio = self.audio_checkbox.isChecked()
        
        # Disable UI
        self.fetch_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.speed_label.setText("🚀 Starting download...")
        
        # Start download thread
        self.download_worker = DownloadWorker(
            url, self.download_path, quality, is_audio
        )
        self.download_worker.progress_update.connect(self.update_progress)
        self.download_worker.status_update.connect(self.log_message)
        self.download_worker.speed_update.connect(self.update_speed)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.start()
        
        # Add to history
        self.add_to_history(url, self.current_video_info['title'], 
                           self.current_video_info.get('thumbnail'))
        
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(int(value))
        
    def update_speed(self, speed_text):
        """Update download speed display"""
        self.speed_label.setText(speed_text)
        
    def on_download_finished(self, success, message):
        """Handle download completion"""
        self.progress_bar.setVisible(False)
        self.fetch_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.download_btn.setEnabled(True)
        self.speed_label.setText("")
        
        if success:
            self.log_message(f"✅ {message}")
            QMessageBox.information(self, "Success", 
                f"{message}\n\nSaved to: {self.download_path}")
            self.statusBar().showMessage(message, 5000)
        else:
            self.log_message(f"❌ {message}")
            QMessageBox.critical(self, "Error", message)
            
    def add_to_history(self, url, title, thumbnail_url=None):
        """Add download to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_text = f"[{timestamp}] {title[:80]}"
        
        item = QListWidgetItem(history_text)
        item.setData(Qt.UserRole, url)
        self.history_list.insertItem(0, item)
        
        # Limit history
        while self.history_list.count() > 30:
            self.history_list.takeItem(self.history_list.count() - 1)
            
    def reuse_from_history(self, item):
        """Reuse URL from history"""
        url = item.data(Qt.UserRole)
        if url:
            self.url_input.setText(url)
            self.fetch_video_info()
            self.log_message(f"📜 Loading from history: {url[:50]}...")
            
    def clear_history(self):
        """Clear download history"""
        self.history_list.clear()
        self.log_message("🗑️ History cleared")
        
    def log_message(self, message):
        """Add timestamped message to status bar"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.statusBar().showMessage(f"[{timestamp}] {message}", 5000)
        
    def closeEvent(self, event):
        """Handle application close"""
        if self.download_worker and self.download_worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Download in progress. Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Video Downloader")
    app.setApplicationVersion("3.0")
    
    # Create and show window
    window = VideoDownloader()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()