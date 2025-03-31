import time
import datetime
import os
import sys
import threading
from threading import Timer, Event

# Global event to signal all threads to exit
exit_event = Event()
# Global variable to store the current timer
current_timer = None

def play_bell_sound():
    """Play the bell.wav sound file from the script's directory."""
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bell_path = os.path.join(script_dir, "bell.wav")
        
        # Check if the bell.wav file exists
        if not os.path.exists(bell_path):
            print(f"Error: bell.wav not found at {bell_path}")
            print("Please place a bell.wav file in the same directory as this script.")
            return
        
        # Play the sound based on the platform
        if sys.platform.startswith('win'):
            import winsound
            winsound.PlaySound(bell_path, winsound.SND_FILENAME)
        elif sys.platform.startswith('darwin'):  # macOS
            os.system(f"afplay '{bell_path}'")
        else:  # Linux and other platforms
            os.system(f"aplay '{bell_path}' 2>/dev/null || paplay '{bell_path}' 2>/dev/null")
        
        print("Bell sound played")
    except Exception as e:
        print(f"Error playing sound: {e}")

def schedule_next_hour():
    """Schedule the next alarm for the top of the next hour."""
    global current_timer
    
    # If exit was requested, don't schedule more timers
    if exit_event.is_set():
        return
    
    now = datetime.datetime.now()
    # Calculate seconds until the next hour
    next_hour = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    seconds_until_next_hour = (next_hour - now).total_seconds()
    
    print(f"Next alarm scheduled for: {next_hour.strftime('%H:%M:%S')}")
    print(f"(in {int(seconds_until_next_hour)} seconds)")
    
    # Schedule the next alarm
    current_timer = Timer(seconds_until_next_hour, hourly_alarm)
    current_timer.daemon = True  # Set as daemon so it won't prevent program exit
    current_timer.start()

def hourly_alarm():
    """Function that runs every hour to play the sound and reschedule."""
    # Check if exit was requested
    if exit_event.is_set():
        return
        
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\nHourly alarm triggered at {current_time}")
    play_bell_sound()
    schedule_next_hour()

def cleanup_and_exit():
    """Clean up resources and exit properly."""
    print("\nCleaning up and exiting...")
    
    # Signal all threads to exit
    exit_event.set()
    
    # Cancel the current timer if it exists
    global current_timer
    if current_timer is not None:
        current_timer.cancel()
    
    # Give a moment for threads to clean up
    time.sleep(0.5)
    
    print("All threads terminated. Goodbye!")
    sys.exit(0)

if __name__ == "__main__":
    print("Hourly Bell Notification Script")
    print("-------------------------------")
    
    # Check for bell.wav file at startup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bell_path = os.path.join(script_dir, "bell.wav")
    if not os.path.exists(bell_path):
        print(f"Warning: bell.wav not found at {bell_path}")
        print("Please place a bell.wav file in the same directory as this script.")
    
    print("Playing test sound on startup...")
    play_bell_sound()  # Play sound once on startup
    
    print("\nThe script is now running. Press Ctrl+C to exit.")
    schedule_next_hour()  # Schedule the first alarm
    
    try:
        # Keep the script running
        while not exit_event.is_set():
            time.sleep(60)  # Check for exit event
    except KeyboardInterrupt:
        cleanup_and_exit()
