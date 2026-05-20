"""
Tek Bantlı Turing Makinesi ile Binary Çarpma Hesaplayıcı

Bu program yalnızca ödevde istenen program kısmını yapar:
1. Kullanıcıdan iki binary sayı alır.
2. Girdilerin yalnızca 0 ve 1 içerdiğini doğrular.
3. Girdiyi Turing bant formatına dönüştürür: sayi1*sayi2=
4. * karakterini kullanarak operandları ayırır.
5. Turing Makinesi simülasyonunu çalıştırır.
6. Her adımda mevcut durum, okunan sembol, yazılan sembol,
   kafa hareketi ve bant içeriğini gösterir.
7. Sonucu binary ve decimal olarak gösterir.
"""

BLANK = "_"
LEFT = "L"
RIGHT = "R"
STAY = "S"


def is_binary(number):
    """Girilen sayının yalnızca 0 ve 1 içerip içermediğini kontrol eder."""
    if number == "":
        return False

    for char in number:
        if char not in ("0", "1"):
            return False

    return True


def binary_add(first, second):
    """
    İki binary sayıyı binary olarak toplar.
    Çarpma için hazır fonksiyon kullanılmaz.
    Shift & Add mantığındaki add kısmı burada yapılır.
    """
    first = first[::-1]
    second = second[::-1]

    max_len = max(len(first), len(second))
    carry = 0
    result = []

    for i in range(max_len):
        bit1 = int(first[i]) if i < len(first) else 0
        bit2 = int(second[i]) if i < len(second) else 0

        total = bit1 + bit2 + carry
        result.append(str(total % 2))
        carry = total // 2

    if carry:
        result.append(str(carry))

    answer = "".join(result[::-1]).lstrip("0")

    if answer == "":
        return "0"

    return answer


class TuringMachine:
    def __init__(self, first_number, second_number):
        # 1) Turing Makinesi bant yapısı
        self.tape = list(first_number + "*" + second_number + "=")

        # 2) Okuma / yazma kafası
        self.head = 0

        # 3) Durum kümesi
        self.states = {
            "q_start",
            "q_find_star",
            "q_find_equal",
            "q_split_operands",
            "q_read_multiplier_bit",
            "q_skip_add",
            "q_shift_multiplicand",
            "q_add",
            "q_write_result",
            "q_accept",
            "q_reject"
        }

        # 4) Giriş alfabesi
        self.input_alphabet = {"0", "1", "*", "="}

        # 5) Bant alfabesi
        self.tape_alphabet = {"0", "1", "*", "=", BLANK}

        # 6) Geçiş fonksiyonu
        # Burada temel sembol okuma/yazma geçişleri tanımlanmıştır.
        # Çarpma kısmında bit değerine göre bu geçiş mantığı uygulanır.
        self.transition_function = {
            ("q_start", "0"): ("q_find_star", "0", RIGHT),
            ("q_start", "1"): ("q_find_star", "1", RIGHT),

            ("q_find_star", "0"): ("q_find_star", "0", RIGHT),
            ("q_find_star", "1"): ("q_find_star", "1", RIGHT),
            ("q_find_star", "*"): ("q_find_equal", "*", RIGHT),

            ("q_find_equal", "0"): ("q_find_equal", "0", RIGHT),
            ("q_find_equal", "1"): ("q_find_equal", "1", RIGHT),
            ("q_find_equal", "="): ("q_split_operands", "=", STAY),

            ("q_read_multiplier_bit", "0"): ("q_skip_add", "0", LEFT),
            ("q_read_multiplier_bit", "1"): ("q_shift_multiplicand", "1", STAY),
        }

        # 7) Başlangıç durumu
        self.start_state = "q_start"
        self.state = self.start_state

        # 8) Kabul durumu
        self.accept_state = "q_accept"

        # 9) Red durumu
        self.reject_state = "q_reject"

        # 10) Operand ayrıştırma için alanlar
        self.first_number = first_number
        self.second_number = second_number
        self.multiplicand = ""
        self.multiplier = ""

        self.result_binary = "0"
        self.step_number = 0

    def tape_content(self):
        return "".join(self.tape)

    def read_symbol(self):
        if self.head < 0:
            self.head = 0

        if self.head >= len(self.tape):
            self.tape.append(BLANK)

        return self.tape[self.head]

    def write_symbol(self, symbol):
        if self.head >= len(self.tape):
            self.tape.append(BLANK)

        self.tape[self.head] = symbol

    def move_head(self, movement):
        if movement == RIGHT:
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append(BLANK)

        elif movement == LEFT:
            if self.head > 0:
                self.head -= 1

        elif movement == STAY:
            pass

    def print_step(self, current_state, read_symbol, write_symbol, movement):
        """
        11) Adım adım simülasyon çıktısı
        Her adımda istenen 5 bilgi gösterilir:
        - mevcut durum
        - okunan sembol
        - yazılan sembol
        - kafa hareketi
        - bant içeriği
        """
        self.step_number += 1

        print("\n" + "-" * 50)
        print("Adım:", self.step_number)
        print("Mevcut durum:", current_state)
        print("Okunan sembol:", read_symbol)
        print("Yazılan sembol:", write_symbol)
        print("Kafa hareketi:", movement)
        print("Bant içeriği:", self.tape_content())

        pointer = " " * self.head + "^"
        print("              " + pointer)

    def apply_transition(self, next_state, write_symbol, movement):
        """
        Bir Turing Makinesi geçişini uygular.
        Önce okur, sonra yazar, adımı gösterir, sonra kafayı hareket ettirir.
        """
        current_state = self.state
        read = self.read_symbol()

        self.write_symbol(write_symbol)

        self.print_step(
            current_state=current_state,
            read_symbol=read,
            write_symbol=write_symbol,
            movement=movement
        )

        self.move_head(movement)
        self.state = next_state

    def find_star(self):
        """
        Bant üzerinde * karakterini bulur.
        * sol tarafı birinci sayı, sağ tarafı ikinci sayı olarak ayrılır.
        """
        self.state = "q_find_star"
        self.head = 0

        while True:
            read = self.read_symbol()

            if read not in self.tape_alphabet:
                self.state = self.reject_state
                raise ValueError("Bant üzerinde geçersiz sembol bulundu.")

            if read == "*":
                self.apply_transition(
                    next_state="q_find_equal",
                    write_symbol="*",
                    movement=RIGHT
                )
                return self.head - 1

            if read in ("0", "1"):
                self.apply_transition(
                    next_state="q_find_star",
                    write_symbol=read,
                    movement=RIGHT
                )
            else:
                self.state = self.reject_state
                raise ValueError("* sembolü bulunmadan beklenmeyen sembol okundu.")

    def find_equal(self):
        """
        Bant üzerinde = karakterini bulur.
        = karakterinden sonrası sonuç alanıdır.
        """
        self.state = "q_find_equal"

        while True:
            read = self.read_symbol()

            if read == "=":
                self.apply_transition(
                    next_state="q_split_operands",
                    write_symbol="=",
                    movement=STAY
                )
                return self.head

            if read in ("0", "1"):
                self.apply_transition(
                    next_state="q_find_equal",
                    write_symbol=read,
                    movement=RIGHT
                )
            else:
                self.state = self.reject_state
                raise ValueError("= sembolü bulunmadan beklenmeyen sembol okundu.")

    def split_operands(self, star_index, equal_index):
        """
        Operand ayrıştırma mekanizması.

        Bant örneği:
        11*10=

        * sol tarafı  -> multiplicand = 11
        * sağ tarafı  -> multiplier   = 10
        """
        self.state = "q_split_operands"
        self.head = star_index

        self.multiplicand = "".join(self.tape[:star_index])
        self.multiplier = "".join(self.tape[star_index + 1:equal_index])

        if self.multiplicand == "" or self.multiplier == "":
            self.state = self.reject_state
            raise ValueError("Birinci veya ikinci operand boş olamaz.")

        read = self.read_symbol()

        self.print_step(
            current_state=self.state,
            read_symbol=read,
            write_symbol=read,
            movement=STAY
        )

        print("\nOperand ayrıştırma:")
        print("* sol tarafı, birinci sayı:", self.multiplicand)
        print("* sağ tarafı, ikinci sayı:", self.multiplier)

    def multiply_with_shift_add(self):
        """
        Turing Makinesi seviyesinde shift & add mantığı.

        Multiplier sağdan sola okunur.
        Okunan bit 0 ise toplama yapılmaz.
        Okunan bit 1 ise multiplicand sola kaydırılıp sonuca eklenir.
        """
        result = "0"
        star_index = self.tape.index("*")

        reversed_multiplier = self.multiplier[::-1]

        for shift_amount, bit in enumerate(reversed_multiplier):
            original_index = len(self.multiplier) - 1 - shift_amount
            self.head = star_index + 1 + original_index

            self.state = "q_read_multiplier_bit"
            read = self.read_symbol()

            self.print_step(
                current_state=self.state,
                read_symbol=read,
                write_symbol=read,
                movement=STAY
            )

            if bit == "0":
                self.state = "q_skip_add"

                self.print_step(
                    current_state=self.state,
                    read_symbol=read,
                    write_symbol=read,
                    movement=LEFT
                )

                self.move_head(LEFT)
                continue

            shifted_value = self.multiplicand + ("0" * shift_amount)

            self.state = "q_shift_multiplicand"

            self.print_step(
                current_state=self.state,
                read_symbol=read,
                write_symbol=read,
                movement=STAY
            )

            old_result = result
            result = binary_add(result, shifted_value)

            self.state = "q_add"

            self.print_step(
                current_state=self.state,
                read_symbol=read,
                write_symbol=read,
                movement=STAY
            )

            print("Ara toplam:", old_result, "+", shifted_value, "=", result)

        self.result_binary = result

    def write_result_to_tape(self):
        """
        Sonucu = karakterinden sonra banda yazar.
        """
        self.state = "q_write_result"

        equal_index = self.tape.index("=")
        self.tape = self.tape[:equal_index + 1]
        self.head = equal_index + 1

        for bit in self.result_binary:
            if self.head >= len(self.tape):
                self.tape.append(BLANK)

            read = self.read_symbol()
            self.write_symbol(bit)

            self.print_step(
                current_state=self.state,
                read_symbol=read,
                write_symbol=bit,
                movement=RIGHT
            )

            self.move_head(RIGHT)

        while len(self.tape) > 0 and self.tape[-1] == BLANK:
            self.tape.pop()

    def accept(self):
        """
        Makine kabul durumuna geçer.
        """
        self.state = self.accept_state
        self.head = len(self.tape) - 1

        read = self.read_symbol()

        self.print_step(
            current_state=self.state,
            read_symbol=read,
            write_symbol=read,
            movement=STAY
        )

    def reject(self, message):
        """
        Makine red durumuna geçer.
        """
        self.state = self.reject_state

        print("\n" + "-" * 50)
        print("Mevcut durum:", self.state)
        print("Red nedeni:", message)

    def run(self):
        """
        Turing Makinesi simülasyonunu çalıştırır.
        """
        print("\nBaşlangıç bant içeriği:", self.tape_content())
        print("Bant formatı: birinci_sayı*ikinci_sayı=")

        star_index = self.find_star()
        equal_index = self.find_equal()

        self.split_operands(star_index, equal_index)
        self.multiply_with_shift_add()
        self.write_result_to_tape()
        self.accept()

        decimal_result = int(self.result_binary, 2)

        print("\n" + "=" * 50)
        print("SONUÇ")
        print("=" * 50)
        print("Final bant içeriği:", self.tape_content())
        print("Binary sonuç:", self.result_binary)
        print("Decimal karşılığı:", decimal_result)
        print("=" * 50)


def main():
    print("Turing Makinesi ile Binary Çarpma Hesaplayıcı")
    print("-" * 50)

    first_number = input("Birinci binary sayıyı giriniz: ").strip()
    second_number = input("İkinci binary sayıyı giriniz: ").strip()

    if not is_binary(first_number):
        print("Hata: Birinci sayı yalnızca 0 ve 1 içermelidir.")
        return

    if not is_binary(second_number):
        print("Hata: İkinci sayı yalnızca 0 ve 1 içermelidir.")
        return

    machine = TuringMachine(first_number, second_number)

    try:
        machine.run()
    except ValueError as error:
        machine.reject(str(error))


if __name__ == "__main__":
    main()
