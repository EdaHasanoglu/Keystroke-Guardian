import time
import json
import sys
import numpy as np
from pynput import keyboard
from sklearn.ensemble import IsolationForest

PROFILE_FILE = "user_profile.json"
TARGET_SENTENCE = "cyber security" # Demo için kısa ve vurucu bir cümle

def extract_features(flight_times):
    """
    13 farklı süreyi vermek yerine, yazma ritminin 'Özetini' (Özniteliklerini) çıkarır.
    Bu sayede yapay zeka ufak insani duraksamaları tolere edebilir.
    """
    flight_array = np.array(flight_times)
    mean_speed = np.mean(flight_array)      # Ortalama hız
    variance = np.var(flight_array)         # Ritim dalgalanması (Tutarlılık)
    total_time = np.sum(flight_array)       # Toplam geçen süre
    return [mean_speed, variance, total_time]

def get_keystrokes(prompt_text):
    """
    Kullanıcının tuşlara basma süreleri arasındaki farkı ölçer.
    Aynı zamanda ekranda yazdıklarını gösterir.
    """
    print(f"\n{prompt_text}")
    print(f"Lütfen şunu hatasız yazın: '{TARGET_SENTENCE}'")
    
    time.sleep(0.5) # Terminalin nefes alması için kısa bir bekleme
    
    flight_times = []
    last_time = [None]
    
    # Arka planda çalışan zaman ölçer fonksiyonumuz
    def on_press(key):
        current_time = time.time()
        if last_time[0] is not None:
            flight_times.append(current_time - last_time[0])
        last_time[0] = current_time

    # 1. Pynput ajanını arka planda başlatıyoruz
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # 2. Ekranda kullanıcının yazdıklarını görmesi için input
    typed_text = input("👉 ")
    
    # 3. Kullanıcı Enter'a basınca arka plandaki ajanı durdur
    listener.stop()

    # Güvenlik Kontrolü: Cümleyi yanlış yazdıysa kabul etme
    if typed_text.strip() != TARGET_SENTENCE:
        print("⚠️ Hata: Cümleyi yanlış veya eksik yazdınız! Harfi harfine aynı olmalı.")
        return None
        
    expected_length = len(TARGET_SENTENCE) - 1
    if len(flight_times) >= expected_length:
        return flight_times[:expected_length]
    return None

def train_model():
    print("\n--- 🧠 TRAINING MODE (BEHAVIORAL PROFILING) ---")
    print("Sistemin yazma ritmini (DNA'nı) öğrenmesi için cümleyi 3 kez yazmalısın.")
    
    samples = []
    for i in range(3):
        flights = get_keystrokes(f"Deneme {i+1}/3:")
        if flights:
            # Ham veriyi değil, ritim özetini (features) alıyoruz
            features = extract_features(flights)
            samples.append(features)
        else:
            print("İşlem iptal edildi. Lütfen baştan başlayın.")
            return

    # Profili JSON olarak kaydet
    with open(PROFILE_FILE, 'w') as f:
        json.dump({"flight_matrices": samples}, f)
    print("\n✅ Biyometrik Profil Başarıyla Oluşturuldu! (Feature Extraction Applied)")

def authenticate_user():
    print("\n--- 🔒 AUTHENTICATION MODE (ZERO-TRUST) ---")
    
    try:
        with open(PROFILE_FILE, 'r') as f:
            data = json.load(f)
            training_data = np.array(data["flight_matrices"])
    except:
        print("⚠️ Profil bulunamadı. Lütfen önce Training (Eğitim) yapın.")
        return

    test_flight = get_keystrokes("Kimliğini Doğrula:")
    
    if not test_flight:
        print("Giriş başarısız.")
        return

    # Test edilen yazının da özetini (features) çıkarıyoruz
    test_features = extract_features(test_flight)
    test_data = np.array(test_features).reshape(1, -1)

    # Contamination oranını düşük tutarak modeli daha dengeli yapıyoruz
    clf = IsolationForest(contamination=0.05, random_state=42)
    clf.fit(training_data)
    
    prediction = clf.predict(test_data)

    if prediction[0] == 1:
        print("\n🔓 ACCESS GRANTED! Biyometrik imza eşleşti. Hoş geldin.")
    else:
        print("\n🚨 SECURITY ALERT: BEHAVIORAL ANOMALY DETECTED! 🚨")
        print("Yazma ritminiz profille uyuşmuyor (Intruder Behavior).")
        print("Oturum Güvenlik Sebebiyle Kilitlendi (Session Lockout).")

def main():
    while True:
        print("\n" + "="*50)
        print("🛡️ KEYSTROKE GUARDIAN V2.0 (ML-POWERED)")
        print("="*50)
        print("1. Training Mode (Profil Oluştur)")
        print("2. Authentication Mode (Giriş Yap)")
        print("3. Çıkış")
        
        try:
            time.sleep(0.1) 
            choice = input("\nSeçiminiz (1-3): ").strip()
            
            if choice == '1':
                train_model()
            elif choice == '2':
                authenticate_user()
            elif choice == '3':
                print("Sistem kapatılıyor. Güvende kalın!")
                break
            elif choice == '':
                continue 
            else:
                print("Geçersiz seçim.")
                time.sleep(0.5)
                
        except (EOFError, KeyboardInterrupt):
            print("\n[!] Sistem zorla durduruldu. Çıkış yapılıyor...")
            break

if __name__ == "__main__":
    main()