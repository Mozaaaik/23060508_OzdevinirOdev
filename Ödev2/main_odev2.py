"""
Final Ödev 2
Turing Makinesi ile Araç Plaka Formatı Tanıyıcı

Tanınan dil / format:
    NNLLNNN

Burada:
    N -> Rakam (0-9)
    L -> Büyük harf (A-Z)

Örnek geçerli girdi:
    55AB123

Bu programda plaka doğrulaması doğrudan if-else zinciriyle yapılmaz.
Format kontrolü Turing Makinesi durumları ve geçiş tablosu üzerinden yapılır.
"""

# ------------------------------------------------------------
# 1. Turing Makinesi temel tanımları
# ------------------------------------------------------------

BLANK = "□"          # Boşluk sembolü
MOVE_RIGHT = "R"     # Kafa sağa hareket eder
MOVE_STAY = "S"      # Kafa olduğu yerde kalır

START_STATE = "q0"
ACCEPT_STATE = "q_accept"
REJECT_STATE = "q_reject"

DIGITS = set("0123456789")
UPPERCASE_LETTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

STATES = {
    "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7",
    ACCEPT_STATE,
    REJECT_STATE
}

INPUT_ALPHABET = DIGITS.union(UPPERCASE_LETTERS)
TAPE_ALPHABET = INPUT_ALPHABET.union({BLANK})

# ------------------------------------------------------------
# 2. Geçiş fonksiyonu
#
# Anahtar: (mevcut_durum, sembol_tipi)
# Değer:   (yeni_durum, yazılacak_sembol, kafa_hareketi)
#
# Sembol tipleri:
#   N     -> rakam
#   L     -> büyük harf
#   B     -> boşluk
#   OTHER -> geçersiz karakter
# ------------------------------------------------------------

TRANSITIONS = {
    # q0 -> ilk karakter rakam olmalı
    ("q0", "N"): ("q1", "SAME", MOVE_RIGHT),

    # q1 -> ikinci karakter rakam olmalı
    ("q1", "N"): ("q2", "SAME", MOVE_RIGHT),

    # q2 -> üçüncü karakter büyük harf olmalı
    ("q2", "L"): ("q3", "SAME", MOVE_RIGHT),

    # q3 -> dördüncü karakter büyük harf olmalı
    ("q3", "L"): ("q4", "SAME", MOVE_RIGHT),

    # q4 -> beşinci karakter rakam olmalı
    ("q4", "N"): ("q5", "SAME", MOVE_RIGHT),

    # q5 -> altıncı karakter rakam olmalı
    ("q5", "N"): ("q6", "SAME", MOVE_RIGHT),

    # q6 -> yedinci karakter rakam olmalı
    ("q6", "N"): ("q7", "SAME", MOVE_RIGHT),

    # q7 -> tam 7 karakter okunduktan sonra boşluk gelirse kabul
    ("q7", "B"): (ACCEPT_STATE, "SAME", MOVE_STAY),
}


def get_symbol_type(symbol):
    """
    Okunan sembolün türünü belirler.
    Bu fonksiyon sadece karakter sınıflandırması yapar.
    Plaka formatı kontrolü geçiş tablosu ile yapılır.
    """
    if symbol == BLANK:
        return "B"
    if symbol in DIGITS:
        return "N"
    if symbol in UPPERCASE_LETTERS:
        return "L"
    return "OTHER"


def create_tape(user_input):
    """
    Kullanıcı girdisini Turing Makinesi bandına yerleştirir.
    Bandın sonuna boşluk sembolü eklenir.
    """
    return list(user_input) + [BLANK]


def tape_to_string(tape, head_position):
    """
    Bandı ekrana daha anlaşılır basmak için hazırlar.
    Kafanın bulunduğu sembol köşeli parantez içinde gösterilir.
    """
    result = []

    for index, symbol in enumerate(tape):
        if index == head_position:
            result.append(f"[{symbol}]")
        else:
            result.append(f" {symbol} ")

    return "".join(result)


def print_machine_info():
    """
    Turing Makinesi'nin temel bileşenlerini ekrana yazar.
    Bu bölüm rapora ve ekran görüntüsüne destek olması için eklenmiştir.
    """
    print("\n" + "=" * 70)
    print("TURING MAKINESI TANIMI")
    print("=" * 70)
    print("Proje Adı       : Turing Makinesi ile Araç Plaka Formatı Tanıyıcı")
    print("Tanınan Format  : NNLLNNN")
    print("N               : Rakam (0-9)")
    print("L               : Büyük harf (A-Z)")
    print("Başlangıç Durumu:", START_STATE)
    print("Kabul Durumu    :", ACCEPT_STATE)
    print("Red Durumu      :", REJECT_STATE)
    print("Boşluk Sembolü  :", BLANK)

    print("\nDurum Kümesi:")
    print(", ".join(sorted(STATES)))

    print("\nGeçiş Tablosu:")
    print("-" * 70)
    print(f"{'Mevcut Durum':<15}{'Okunan Tip':<15}{'Yeni Durum':<15}{'Yaz':<10}{'Hareket'}")
    print("-" * 70)

    for (state, symbol_type), (next_state, write_symbol, move) in TRANSITIONS.items():
        print(f"{state:<15}{symbol_type:<15}{next_state:<15}{write_symbol:<10}{move}")

    print("-" * 70)


def simulate_turing_machine(user_input, show_steps=True):
    """
    Girilen plakayı Turing Makinesi ile adım adım kontrol eder.

    Kabul şartı:
        q7 durumuna geldikten sonra okunan sembol boşluk ise KABUL.

    Red şartı:
        Beklenen sembol türü gelmezse,
        küçük harf veya özel karakter varsa,
        eksik karakter varsa,
        fazladan karakter varsa RED.
    """
    tape = create_tape(user_input)
    head = 0
    current_state = START_STATE
    step = 1

    if show_steps:
        print("\n" + "=" * 70)
        print(f"Girdi: {user_input}")
        print("=" * 70)
        print("Başlangıç bandı:")
        print(tape_to_string(tape, head))
        print("-" * 70)

    while current_state not in {ACCEPT_STATE, REJECT_STATE}:
        # Kafa bandın dışına çıkarsa yeni boşluk eklenir.
        if head >= len(tape):
            tape.append(BLANK)

        read_symbol = tape[head]
        symbol_type = get_symbol_type(read_symbol)

        transition = TRANSITIONS.get((current_state, symbol_type))

        # Geçiş yoksa makine RED durumuna gider.
        if transition is None:
            if show_steps:
                print(f"Adım {step}")
                print(f"Mevcut durum : {current_state}")
                print(f"Okunan sembol: {read_symbol}")
                print(f"Sembol tipi  : {symbol_type}")
                print("Geçiş        : Uygun geçiş bulunamadı")
                print("Yeni durum   :", REJECT_STATE)
                print("Kafa hareketi:", MOVE_STAY)
                print("Bant         :", tape_to_string(tape, head))
                print("-" * 70)

            current_state = REJECT_STATE
            break

        next_state, write_rule, move = transition

        if write_rule == "SAME":
            write_symbol = read_symbol
        else:
            write_symbol = write_rule

        tape[head] = write_symbol

        if show_steps:
            print(f"Adım {step}")
            print(f"Mevcut durum : {current_state}")
            print(f"Okunan sembol: {read_symbol}")
            print(f"Sembol tipi  : {symbol_type}")
            print(f"Yazılan      : {write_symbol}")
            print(f"Kafa hareketi: {move}")
            print(f"Yeni durum   : {next_state}")
            print("Bant         :", tape_to_string(tape, head))
            print("-" * 70)

        if move == MOVE_RIGHT:
            head += 1
        elif move == MOVE_STAY:
            head = head

        current_state = next_state
        step += 1

    if show_steps:
        if current_state == ACCEPT_STATE:
            print("Sonuç: KABUL")
        else:
            print("Sonuç: RED")
        print("=" * 70)

    return current_state == ACCEPT_STATE


def run_single_input():
    """
    Kullanıcıdan tek bir plaka alır ve adım adım simülasyon yapar.
    """
    plate = input("Plaka giriniz: ")
    simulate_turing_machine(plate, show_steps=True)


def run_test_suite():
    """
    Teslimde kullanılabilecek örnek testleri çalıştırır.
    En az 5 geçerli ve 5 geçersiz test girdisi içerir.
    """
    valid_inputs = [
        "55AB123",
        "34TR456",
        "06AA789",
        "01BC234",
        "81ZZ999"
    ]

    invalid_inputs = [
        "5AB123",     # Eksik karakter / ilk iki rakam şartı bozuk
        "555AB12",    # Üçüncü karakter harf olmalıydı
        "34A1234",    # Dördüncü karakter harf olmalıydı
        "AB34123",    # İlk karakterler rakam olmalıydı
        "34AB12X",    # Son karakter rakam olmalıydı
        "55ab123",    # Küçük harf kabul edilmez
        "55AB1234",   # Fazladan karakter var
        "55A*123"     # Özel karakter var
    ]

    print("\n" + "=" * 70)
    print("HAZIR TESTLER")
    print("=" * 70)

    print("\nGEÇERLİ GİRDİ TESTLERİ")
    print("-" * 70)
    for plate in valid_inputs:
        result = simulate_turing_machine(plate, show_steps=False)
        print(f"{plate:<12} -> {'KABUL' if result else 'RED'}")

    print("\nGEÇERSİZ GİRDİ TESTLERİ")
    print("-" * 70)
    for plate in invalid_inputs:
        result = simulate_turing_machine(plate, show_steps=False)
        print(f"{plate:<12} -> {'KABUL' if result else 'RED'}")

    print("=" * 70)


def main():
    print_machine_info()

    while True:
        print("\nMENÜ")
        print("1 - Tek plaka gir ve adım adım çalıştır")
        print("2 - Hazır testleri çalıştır")
        print("0 - Çıkış")

        choice = input("Seçiminiz: ")

        if choice == "1":
            run_single_input()
        elif choice == "2":
            run_test_suite()
        elif choice == "0":
            print("Program sonlandırıldı.")
            break
        else:
            print("Geçersiz seçim. Lütfen 1, 2 veya 0 giriniz.")


if __name__ == "__main__":
    main()