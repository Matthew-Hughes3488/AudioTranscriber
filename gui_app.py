"""
GUI interface for audio/video transcription using OpenAI Whisper.
A warm, friendly interface designed for non-technical users.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
from transcription_core import (
    TranscriptionSession, find_media_files, get_search_directory,
    WHISPER_MODELS, get_model_info, is_media_file,
    get_transcription_output_dir
)


class AudioTranscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Transcriber - Made with ❤️ by Matt")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.center_window()
        
        # Prevent window from being too small
        self.root.minsize(600, 500)
        
        # Variables
        self.selected_files = []
        self.transcription_session = None
        self.is_transcribing = False
        
        # Create GUI
        self.create_widgets()
        
        # Start with welcome screen
        self.show_welcome_screen()
    
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Welcome frame (initially hidden)
        self.create_welcome_frame()
        
        # Main application frame
        self.create_main_frame()
        
        # Progress frame (initially hidden)
        self.create_progress_frame()
    
    def create_welcome_frame(self):
        """Create the welcome screen."""
        self.welcome_frame = ttk.Frame(self.main_frame)
        
        # Welcome message
        welcome_label = ttk.Label(
            self.welcome_frame,
            text="🎵 Audio Transcriber 🎵",
            font=("Arial", 24, "bold"),
            foreground="#4a4a4a"
        )
        welcome_label.pack(pady=(50, 20))
        
        # Personal message
        message_label = ttk.Label(
            self.welcome_frame,
            text="Made with love for you... From Matthew ❤️",
            font=("Arial", 16, "italic"),
            foreground="#666666"
        )
        message_label.pack(pady=(0, 20))
        
        # Description
        desc_text = """
        This tool will help you easily transcribe your interviews and recordings
        for your academic work. Simply choose your files, select a model,
        and let the magic happen!
        
        All transcripts include timestamps to help you find specific parts
        of your recordings quickly.
        """
        
        desc_label = ttk.Label(
            self.welcome_frame,
            text=desc_text.strip(),
            font=("Arial", 12),
            foreground="#555555",
            justify=tk.CENTER,
            wraplength=600
        )
        desc_label.pack(pady=(0, 40))
        
        # Get started button
        start_button = ttk.Button(
            self.welcome_frame,
            text="Get Started",
            command=self.show_main_screen,
            style="Accent.TButton"
        )
        start_button.pack(pady=10)
        
        # Configure button style
        self.root.style = ttk.Style()
        self.root.style.configure("Accent.TButton", font=("Arial", 12, "bold"))
    
    def create_main_frame(self):
        """Create the main application interface."""
        self.app_frame = ttk.Frame(self.main_frame)
        
        # Title
        title_label = ttk.Label(
            self.app_frame,
            text="🎵 Audio Transcriber 🎵",
            font=("Arial", 18, "bold"),
            foreground="#4a4a4a"
        )
        title_label.pack(pady=(0, 20))
        
        # Model selection frame
        model_frame = ttk.LabelFrame(self.app_frame, text="Step 1: Choose Transcription Model", padding="15")
        model_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.model_var = tk.StringVar(value='base')
        model_info = get_model_info()
        
        for model in WHISPER_MODELS:
            description = model_info.get(model, '')
            ttk.Radiobutton(
                model_frame,
                text=f"{model.title()}: {description}",
                variable=self.model_var,
                value=model
            ).pack(anchor=tk.W, pady=2)
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.app_frame, text="Step 2: Select Audio/Video Files", padding="15")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # File selection buttons
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            button_frame,
            text="📁 Choose Files",
            command=self.select_files
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="📂 Find Files in Folder",
            command=self.find_files_in_folder
        ).pack(side=tk.LEFT)
        
        # Selected files display
        self.files_text = scrolledtext.ScrolledText(
            file_frame,
            height=8,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        self.files_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.files_text.insert(tk.END, "No files selected yet.\n\nYou can:\n• Click 'Choose Files' to select individual files\n• Click 'Find Files in Folder' to auto-detect audio/video files")
        self.files_text.config(state=tk.DISABLED)
        
        # Action buttons frame
        action_frame = ttk.Frame(self.app_frame)
        action_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Clear files button
        ttk.Button(
            action_frame,
            text="Clear Files",
            command=self.clear_files
        ).pack(side=tk.LEFT)
        
        # Start transcription button
        self.start_button = ttk.Button(
            action_frame,
            text="🎯 Start Transcription",
            command=self.start_transcription,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.RIGHT)
    
    def create_progress_frame(self):
        """Create the progress/status frame."""
        self.progress_frame = ttk.Frame(self.main_frame)
        
        # Title
        title_label = ttk.Label(
            self.progress_frame,
            text="🎵 Transcription in Progress 🎵",
            font=("Arial", 18, "bold"),
            foreground="#4a4a4a"
        )
        title_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.pack(pady=(0, 20))
        
        # Status text
        self.status_text = scrolledtext.ScrolledText(
            self.progress_frame,
            height=15,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Action buttons
        progress_button_frame = ttk.Frame(self.progress_frame)
        progress_button_frame.pack(fill=tk.X)
        
        self.cancel_button = ttk.Button(
            progress_button_frame,
            text="Cancel",
            command=self.cancel_transcription
        )
        self.cancel_button.pack(side=tk.LEFT)
        
        self.back_button = ttk.Button(
            progress_button_frame,
            text="Back to Main",
            command=self.show_main_screen,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.RIGHT)
    
    def show_welcome_screen(self):
        """Show the welcome screen."""
        self.app_frame.pack_forget()
        self.progress_frame.pack_forget()
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_main_screen(self):
        """Show the main application screen."""
        self.welcome_frame.pack_forget()
        self.progress_frame.pack_forget()
        self.app_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_progress_screen(self):
        """Show the progress screen."""
        self.welcome_frame.pack_forget()
        self.app_frame.pack_forget()
        self.progress_frame.pack(fill=tk.BOTH, expand=True)
    
    def select_files(self):
        """Open file dialog to select audio/video files."""
        filetypes = [
            ("Audio/Video Files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma *.mp4 *.mkv *.mov *.avi *.webm *.wmv *.mpeg *.mpg"),
            ("Audio Files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma"),
            ("Video Files", "*.mp4 *.mkv *.mov *.avi *.webm *.wmv *.mpeg *.mpg"),
            ("All Files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select audio/video files to transcribe",
            filetypes=filetypes
        )
        
        if files:
            # Filter for media files only
            media_files = [f for f in files if is_media_file(os.path.basename(f))]
            if media_files != list(files):
                messagebox.showwarning(
                    "File Filter",
                    f"Selected {len(files)} files, but only {len(media_files)} are supported media files."
                )
            
            self.selected_files = media_files
            self.update_files_display()
    
    def find_files_in_folder(self):
        """Find media files in a selected folder."""
        folder = filedialog.askdirectory(title="Select folder containing audio/video files")
        
        if folder:
            media_files = find_media_files(folder)
            if media_files:
                # Convert to full paths
                self.selected_files = [os.path.join(folder, f) for f in media_files]
                self.update_files_display()
                messagebox.showinfo(
                    "Files Found",
                    f"Found {len(media_files)} media files in the selected folder."
                )
            else:
                messagebox.showwarning(
                    "No Files Found",
                    "No audio/video files were found in the selected folder."
                )
    
    def clear_files(self):
        """Clear the selected files."""
        self.selected_files = []
        self.update_files_display()
    
    def update_files_display(self):
        """Update the files display text widget."""
        self.files_text.config(state=tk.NORMAL)
        self.files_text.delete(1.0, tk.END)
        
        if self.selected_files:
            self.files_text.insert(tk.END, f"Selected {len(self.selected_files)} files:\n\n")
            for i, file_path in enumerate(self.selected_files, 1):
                filename = os.path.basename(file_path)
                self.files_text.insert(tk.END, f"{i:2d}. {filename}\n")
        else:
            self.files_text.insert(tk.END, "No files selected yet.\n\nYou can:\n• Click 'Choose Files' to select individual files\n• Click 'Find Files in Folder' to auto-detect audio/video files")
        
        self.files_text.config(state=tk.DISABLED)
    
    def start_transcription(self):
        """Start the transcription process."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select some audio/video files first.")
            return
        
        # Confirm start
        model_name = self.model_var.get()
        result = messagebox.askyesno(
            "Start Transcription",
            f"Ready to transcribe {len(self.selected_files)} files using the '{model_name}' model.\n\nThis may take several minutes depending on file length.\n\nProceed?"
        )
        
        if not result:
            return
        
        # Show progress screen
        self.show_progress_screen()
        
        # Clear status text
        self.status_text.delete(1.0, tk.END)
        
        # Start progress bar
        self.progress_bar.start(10)
        
        # Disable buttons
        self.is_transcribing = True
        self.cancel_button.config(state=tk.NORMAL)
        self.back_button.config(state=tk.DISABLED)
        
        # Start transcription in background thread
        self.transcription_thread = threading.Thread(target=self.run_transcription)
        self.transcription_thread.daemon = True
        self.transcription_thread.start()
    
    def run_transcription(self):
        """Run transcription in background thread."""
        try:
            model_name = self.model_var.get()
            self.transcription_session = TranscriptionSession(model_name, self.update_progress)
            
            # Load model
            if not self.transcription_session.load_model():
                self.transcription_finished(success=False, error="Failed to load transcription model")
                return
            
            # Prepare file list and directories
            files_by_dir = {}
            for file_path in self.selected_files:
                dir_path = os.path.dirname(file_path)
                filename = os.path.basename(file_path)
                if dir_path not in files_by_dir:
                    files_by_dir[dir_path] = []
                files_by_dir[dir_path].append(filename)
            
            # Transcribe files by directory
            total_results = {
                'total_files': len(self.selected_files),
                'completed_files': 0,
                'failed_files': 0,
                'errors': []
            }
            
            for search_dir, files in files_by_dir.items():
                if self.transcription_session.is_cancelled:
                    break
                
                results = self.transcription_session.transcribe_files(files, search_dir)
                total_results['completed_files'] += results['completed_files']
                total_results['failed_files'] += results['failed_files']
                total_results['errors'].extend(results['errors'])
            
            self.transcription_finished(success=True, results=total_results)
            
        except Exception as e:
            self.transcription_finished(success=False, error=str(e))
    
    def update_progress(self, message):
        """Update progress display (called from background thread)."""
        # Use after_idle to safely update GUI from thread
        self.root.after_idle(lambda: self._update_progress_safe(message))
    
    def _update_progress_safe(self, message):
        """Thread-safe progress update."""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def cancel_transcription(self):
        """Cancel the ongoing transcription."""
        if self.transcription_session:
            self.transcription_session.cancel()
        
        self.update_progress("Cancelling transcription...")
        self.cancel_button.config(state=tk.DISABLED)
    
    def transcription_finished(self, success=True, results=None, error=None):
        """Handle transcription completion (called from background thread)."""
        self.root.after_idle(lambda: self._transcription_finished_safe(success, results, error))
    
    def _transcription_finished_safe(self, success, results, error):
        """Thread-safe transcription completion handler."""
        # Stop progress bar
        self.progress_bar.stop()
        
        # Update UI state
        self.is_transcribing = False
        self.cancel_button.config(state=tk.DISABLED)
        self.back_button.config(state=tk.NORMAL)
        
        if success and results:
            # Show success message
            self.update_progress("\n" + "="*50)
            self.update_progress("🎉 TRANSCRIPTION COMPLETE! 🎉")
            self.update_progress(f"Total files: {results['total_files']}")
            self.update_progress(f"Completed successfully: {results['completed_files']}")
            self.update_progress(f"Failed: {results['failed_files']}")
            
            if results['errors']:
                self.update_progress("\nErrors:")
                for error in results['errors']:
                    self.update_progress(f"  {error}")
            
            if results['completed_files'] > 0:
                # Find output directory (use the directory of the first file)
                if self.selected_files:
                    first_file_dir = os.path.dirname(self.selected_files[0])
                    output_dir = get_transcription_output_dir(first_file_dir)
                    self.update_progress(f"\nTranscript files saved to:")
                    self.update_progress(f"{output_dir}")
                    
                    # Show completion dialog
                    messagebox.showinfo(
                        "Transcription Complete!",
                        f"Successfully transcribed {results['completed_files']} files!\n\nTranscripts saved to:\n{output_dir}"
                    )
            else:
                messagebox.showerror("Transcription Failed", "No files were successfully transcribed.")
                
        elif error:
            # Show error
            self.update_progress(f"\n❌ ERROR: {error}")
            messagebox.showerror("Transcription Error", f"An error occurred during transcription:\n\n{error}")
        else:
            # Cancelled
            self.update_progress("\n🚫 Transcription cancelled by user")
            messagebox.showinfo("Cancelled", "Transcription was cancelled.")


def main():
    """Main GUI application entry point."""
    root = tk.Tk()
    app = AudioTranscriberGUI(root)
    
    # Handle window close
    def on_closing():
        if app.is_transcribing:
            if messagebox.askokcancel("Quit", "Transcription is in progress. Do you want to cancel and quit?"):
                if app.transcription_session:
                    app.transcription_session.cancel()
                root.quit()
        else:
            root.quit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    # Fix for PyInstaller multiprocessing issues
    import multiprocessing
    multiprocessing.freeze_support()
    
    main()