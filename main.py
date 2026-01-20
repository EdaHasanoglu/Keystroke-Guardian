#!/usr/bin/env python3
"""
Keystroke Bio-Profiler
A biometric authentication system based on typing rhythm analysis.

This program uses the pynput library to monitor keystrokes and creates
a biometric profile based on the time intervals between key presses
(flight time) when typing a specific sentence.

Author: [Your Name]
Date: 2026
"""

import time
import json
import os
from pynput import keyboard
import sys
import cv2  # OpenCV for Camera Capture

# Configuration
PROFILE_FILE = "user_profile.json"
TARGET_SENTENCE = "The quick brown fox jumps over the lazy dog"

def take_intruder_photo():
    """
    Captures a photo of the unauthorized user using the webcam.
    """
    print("\n[SYSTEM ALERT] Unauthorized access detected! Capturing evidence...")
    
    # Initialize webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[ERROR] Could not access the camera.")
        return

    # Warm-up time for camera light adjustment
    time.sleep(0.5)
    
    # Capture a single frame
    ret, frame = cap.read()
    
    if ret:
        timestamp = int(time.time())
        filename = f"INTRUDER_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 [EVIDENCE SAVED] Intruder photo saved as: {filename}")
    else:
        print("[ERROR] Failed to capture image.")
        
    # Release the camera resource
    cap.release()

def get_keystrokes(prompt_text):
    """
    Captures keystrokes and measures flight time (latency between keys).
    """
    print(f"\n{prompt_text}")
    print(f"Please type: '{TARGET_SENTENCE}'")
    
    # Anti-Ghosting Delay: Wait for user to release the 'Enter' key from menu selection
    time.sleep(0.5) 
    
    print("Start typing (Press ENTER when done): ", end='', flush=True)

    flight_times = []
    last_time = None
    typed_chars = []

    def on_press(key):
        nonlocal last_time
        current_time = time.time()
        
        try:
            # Echo typed characters to console
            if hasattr(key, 'char'):
                sys.stdout.write(key.char)
                sys.stdout.flush()
                typed_chars.append(key.char)
            elif key == keyboard.Key.space:
                sys.stdout.write(' ')
                sys.stdout.flush()
                typed_chars.append(' ')
            
            # Measure flight time
            if last_time is not None:
                diff = current_time - last_time
                flight_times.append(diff)
            
            last_time = current_time

        except Exception:
            pass

    def on_release(key):
        if key == keyboard.Key.enter:
            return False # Stop listener

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    print() # New line
    return flight_times, "".join(typed_chars)

def main():
    # Initialize profile file if not exists
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'w') as f:
            json.dump({}, f)

    while True:
        print("\n--- 🛡️ KEYSTROKE GUARDIAN V2.0 (BIOMETRIC SECURITY) 🛡️ ---")
        print("1. Train Mode (Build Profile)")
        print("2. Authenticate (Security Test)")
        print("3. Exit")
        
        choice = input("Select Option (1-3): ").strip()

        if choice == '1':
            print("\n--- TRAINING MODE ---")
            print("You need to type the phrase 5 times to build a baseline.")
            all_flights = []
            
            for i in range(5):
                flights, text = get_keystrokes(f"--- Sample {i+1}/5 ---")
                
                # Basic validation
                if len(text) < 10:
                    print("❌ Input too short. Please try again.")
                    continue
                    
                all_flights.extend(flights)
                print("✅ Sample Recorded.")
            
            if all_flights:
                # Calculate average flight time
                avg_flight = sum(all_flights) / len(all_flights)
                with open(PROFILE_FILE, 'w') as f:
                    json.dump({"avg_flight": avg_flight}, f)
                print(f"\n✨ Biometric Profile Saved! (Speed Score: {avg_flight:.4f})")
            
        elif choice == '2':
            print("\n--- AUTHENTICATION MODE ---")
            try:
                with open(PROFILE_FILE, 'r') as f:
                    data = json.load(f)
            except Exception:
                data = {}
            
            if "avg_flight" not in data:
                print("⚠️ No profile found. Please use Training Mode (Option 1) first.")
                continue
                
            saved_avg = data["avg_flight"]
            flights, text = get_keystrokes("Verify your identity:")
            
            if not flights:
                print("No input detected.")
                continue

            current_avg = sum(flights) / len(flights)
            print(f"\nYour Speed: {current_avg:.4f}")
            print(f"Profile Speed: {saved_avg:.4f}")
            
            # Security Threshold (25% Tolerance)
            diff = abs(current_avg - saved_avg)
            threshold = saved_avg * 0.25
            
            if diff < threshold:
                print("\n🔓 ACCESS GRANTED. Welcome back, User! ✅")
            else:
                print("\n🚨 SECURITY ALERT: BIOMETRIC MISMATCH! 🚨")
                print("System assumes you are an intruder.")
                take_intruder_photo() # TRIGGER CAMERA
                
        elif choice == '3':
            print("System shutting down. Stay safe! 👋")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()