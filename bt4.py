from abc import ABC, abstractmethod

# ==========================================
# 1. ĐỊNH NGHĨA CÁC LỚP ĐỐI TƯỢNG
# ==========================================

class Equipment(ABC):
    """Lớp trừu tượng định hình tiêu chuẩn cho mọi loại trang bị."""
    
    @abstractmethod
    def calculate_total_damage(self) -> int:
        """Phương thức trừu tượng tính toán tổng sát thương gây ra."""
        pass


class Weapon(Equipment):
    """Lớp biểu diễn Vũ khí Vật lý thông thường."""
    
    def __init__(self, name: str, base_damage: int, upgrade_level: int = 0):
        self.name = name
        self.base_damage = base_damage
        self.upgrade_level = upgrade_level

    def calculate_total_damage(self) -> int:
        """Công thức: Sát thương gốc + (Cấp cường hóa * 10)"""
        return self.base_damage + (self.upgrade_level * 10)

    def __gt__(self, other):
        """Bẫy dữ liệu 2: Nạp chồng toán tử > bảo vệ kiểu dữ liệu"""
        if not isinstance(other, Equipment):
            print("Loi: Chi co the so sanh giua cac trang bi!")
            return False
        return self.calculate_total_damage() > other.calculate_total_damage()

    def __add__(self, other):
        """Bẫy dữ liệu 2: Nạp chồng toán tử + (Dung hợp vũ khí)"""
        if not isinstance(other, Equipment):
            print("Loi: Chi co the dung hop giua cac trang bi!")
            return None
        
        new_name = f"Fusion({self.name} + {other.name})"
        new_base_damage = self.base_damage + other.base_damage
        new_upgrade_level = self.upgrade_level + other.upgrade_level
        
        return Weapon(new_name, new_base_damage, new_upgrade_level)


class MagicMixin:
    """Mixin Class cung cấp các thuộc tính phép thuật phụ trợ."""
    
    def __init__(self, magic_power: int):
        self.magic_power = magic_power

    def cast_glow(self) -> str:
        return f"Vu khi toa ra luong ma luc huyen bi (Magic Power: {self.magic_power})!"


class MagicSword(Weapon, MagicMixin):
    """Kiếm Ma Thuật - Kết hợp đa kế thừa từ Weapon và MagicMixin."""
    
    def __init__(self, name: str, base_damage: int, upgrade_level: int, magic_power: int):
        # Bẫy dữ liệu 3: Khởi tạo tường minh theo đúng MRO để tránh mất thuộc tính
        Weapon.__init__(self, name, base_damage, upgrade_level)
        MagicMixin.__init__(self, magic_power)

    def calculate_total_damage(self) -> int:
        """Công thức: Sát thương vật lý + Sức mạnh phép thuật"""
        return Weapon.calculate_total_damage(self) + self.magic_power


# ==========================================
# 2. HỆ THỐNG QUẢN LÝ LÒ RÈN
# ==========================================

class BlacksmithManager:
    def __init__(self):
        self.inventory = []

    def get_validated_int(self, prompt: str) -> int:
        """Hàm helper ép kiểu số nguyên và bắt lỗi nhập liệu"""
        while True:
            try:
                val = int(input(prompt))
                if val <= 0:
                    print("Loi: Gia tri phai lon hon 0!")
                    continue
                return val
            except ValueError:
                print("Loi: Vui long nhap vao mot so nguyen hop le!")

    def show_inventory(self):
        """Chức năng 1: Xem kho vũ khí ứng dụng Tính Đa hình"""
        print("\n--- KHO VU KHI CUA NGUOI CHOI ---")
        if not self.inventory:
            print("Kho vu khi hien dang trong.")
            print("Vui long ren vu khi bang Chuc nang 2 hoac Chuc nang 3.")
            return

        print(f"{'STT':<4} | {'Ten vu khi':<25} | {'Loai':<12} | {'Cap':<5} | {'Sat thuong tong'}")
        print("-" * 65)
        for idx, item in enumerate(self.inventory, 1):
            loai_vk = item.__class__.__name__
            print(f"{idx:<4} | {item.name:<25} | {loai_vk:<12} | {item.upgrade_level:<5} | {item.calculate_total_damage()}")
        print("-" * 65)

    def craft_weapon(self):
        """Chức năng 2: Rèn Vũ khí Vật lý"""
        print("\n--- REN VU KHI VAT LY ---")
        name = input("Nhập tên vũ khí: ").strip().title()
        base_damage = self.get_validated_int("Nhập sát thương gốc: ")
        upgrade_level = self.get_validated_int("Nhập cấp cường hóa: ")

        new_wp = Weapon(name, base_damage, upgrade_level)
        self.inventory.append(new_wp)

        print("\n>> Ren vu khi vat ly thanh cong!")
        print(f"Ten vu khi: {new_wp.name} | Loai: Weapon | Cap cuong hoa: {new_wp.upgrade_level} | Sat thuong tong: {new_wp.calculate_total_damage()}")

    def craft_magic_sword(self):
        """Chức năng 3: Rèn Kiếm Ma Thuật"""
        print("\n--- REN KIEM MA THUAT ---")
        name = input("Nhập tên kiếm ma thuật: ").strip().title()
        base_damage = self.get_validated_int("Nhập sát thương gốc: ")
        upgrade_level = self.get_validated_int("Nhập cấp cường hóa: ")
        magic_power = self.get_validated_int("Nhập sức mạnh phép thuật: ")

        new_ms = MagicSword(name, base_damage, upgrade_level, magic_power)
        self.inventory.append(new_ms)

        print("\n>> Ren kiem ma thuat thanh cong!")
        print(new_ms.cast_glow())
        print(f"Ten vu khi: {new_ms.name} | Loai: MagicSword | Cap cuong hoa: {new_ms.upgrade_level} | Sat thuong tong: {new_ms.calculate_total_damage()}")

    def evaluate_weapons(self):
        """Chức năng 4: Thẩm định vũ khí bằng toán tử >"""
        print("\n--- THAM DINH VU KHI ---")
        if len(self.inventory) < 2:
            print("Loi: Can it nhat 2 vu khi trong kho de tham dinh!")
            return

        vk1 = self.inventory[0]
        vk2 = self.inventory[1]

        print(f"Vu khi thu nhat:\n{vk1.name} | Loai: {vk1.__class__.__name__} | Sat thuong: {vk1.calculate_total_damage()}\n")
        print(f"Vu khi thu hai:\n{vk2.name} | Loai: {vk2.__class__.__name__} | Sat thuong: {vk2.calculate_total_damage()}\n")

        if vk1 > vk2:
            print(f"Ket qua: {vk1.name} manh hon {vk2.name}.")
        elif vk2 > vk1:
            print(f"Ket qua: {vk2.name} manh hon {vk1.name}.")
        else:
            print("Ket qua: Hai vu khi co suc manh ngang nhau.")

    def fuse_weapons(self):
        """Chức năng 5: Dung hợp 2 vũ khí bằng toán tử +"""
        print("\n--- DUNG HOP VU KHI ---")
        if len(self.inventory) < 2:
            print("Loi: Can it nhat 2 vu khi trong kho de dung hop!")
            return

        print("Dang dung hop 2 vu khi dau tien trong kho...\n")
        vk1 = self.inventory[0]
        vk2 = self.inventory[1]

        print(f"Vu khi 1: {vk1.name} | Cap: {vk1.upgrade_level} | Sat thuong goc: {vk1.base_damage}")
        print(f"Vu khi 2: {vk2.name} | Cap: {vk2.upgrade_level} | Sat thuong goc: {vk2.base_damage}")

        new_weapon = vk1 + vk2

        if new_weapon:
            self.inventory.pop(0)
            self.inventory.pop(0)
            self.inventory.append(new_weapon)

            print("\n>> Dung hop vu khi thanh cong!")
            print(f"Da xoa khoi kho: {vk1.name}")
            print(f"Da xoa khoi kho: {vk2.name}\n")
            print(f"Vu khi moi: {new_weapon.name}")
            print(f"Loai: {new_weapon.__class__.__name__}")
            print(f"Cap cuong hoa: {new_weapon.upgrade_level}")
            print(f"Sat thuong tong: {new_weapon.calculate_total_damage()}")


# ==========================================
# 3. KỊCH BẢN ĐIỀU HƯỚNG MAIN MENU
# ==========================================

if __name__ == "__main__":
    try:
        loi_interface = Equipment()
    except TypeError as e:
        print(f"[KIEN TRUC SU HE THONG]: Da kich hoat bao mat ABC thanh cong! {e}\n")

    blacksmith = BlacksmithManager()

    while True:
        print("\n===== LO REN VU KHI RIKKEI STUDIOS =====")
        print("1. Xem kho vu khi & Sat thuong tong")
        print("2. Ren Vu khi Vat ly (Tao Weapon)")
        print("3. Ren Kiem Ma Thuat (Tao MagicSword)")
        print("4. Tham dinh vu khi (So sanh lon hon)")
        print("5. Dung hop vu khi (Cong don cap do)")
        print("6. Thoat game")
        print("========================================")
        
        choice = input("Chon chuc nang (1-6): ").strip()
        
        if choice == "1":
            blacksmith.show_inventory()
        elif choice == "2":
            blacksmith.craft_weapon()
        elif choice == "3":
            blacksmith.craft_magic_sword()
        elif choice == "4":
            blacksmith.evaluate_weapons()
        elif choice == "5":
            blacksmith.fuse_weapons()
        elif choice == "6":
            print("\nThoat Lo Ren. Hen gap lai Anh hung!")
            break
        else:
            print("Loi: Lua chon khong hop le, hay chon tu 1 den 6.")