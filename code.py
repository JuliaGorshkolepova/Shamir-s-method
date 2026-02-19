import random
from typing import List, Tuple
class ShamirSecretSharing:
    def __init__(self, prime: int = 2**127 - 1):
        self.prime = prime

    def _eval_poly(self, coeffs: List[int], x: int) -> int:
        y = 0
        for coeff in reversed(coeffs):
            y = (y * x + coeff) % self.prime
        return y

    def _lagrange_interpolation(self, x: int, shares: List[Tuple[int, int]]) -> int:
        result = 0
        k = len(shares)
        for i in range(k):
            xi, yi = shares[i]
            li = 1
            for j in range(k):
                if i != j:
                    xj, _ = shares[j]
                    li = (li * (x - xj) * pow(xi - xj, -1, self.prime)) % self.prime
            result = (result + yi * li) % self.prime
        return result

    def generate_and_split(self, n: int, secret_length: int, k: int) -> Tuple[str, List[Tuple[int, int]]]:
        if k > n:
            raise ValueError("k не может быть больше n")
        
        min_val = 10**(secret_length - 1)
        max_val = 10**secret_length - 1
        secret = random.randint(min_val, max_val)
        
        coeffs = [secret] + [random.randrange(1, self.prime) for _ in range(k - 1)]
        
        shares = []
        for i in range(1, n + 1):
            x = i
            y = self._eval_poly(coeffs, x)
            shares.append((x, y))
        
        return str(secret), shares

    def split_existing_secret(self, secret: int, n: int, k: int) -> List[Tuple[int, int]]:
        if k > n:
            raise ValueError("k не может быть больше n")
        if secret >= self.prime:
            raise ValueError("Секрет должен быть меньше простого числа")

        coeffs = [secret] + [random.randrange(1, self.prime) for _ in range(k - 1)]

        shares = []
        for i in range(1, n + 1):
            x = i
            y = self._eval_poly(coeffs, x)
            shares.append((x, y))
        return shares

    def recover_secret_from_shares(self, shares: List[Tuple[int, int]]) -> int:
        if len(shares) < 2:
            raise ValueError("Нужно хотя бы 2 доли для восстановления")
        return self._lagrange_interpolation(0, shares)

def main():
    sss = ShamirSecretSharing()
    
    while True:
        print("\nВыберите режим:")
        print("1. Генерация и разделение секрета")
        print("2. Разделение уже готового секрета")
        print("3. Восстановление секрета по частям")
        print("4. Выход")
        
        choice = input("\nВаш выбор (1-4): ")
        
        if choice == "1":
            try:
                n = int(input("Количество частей: "))
                secret_length = int(input("Длина секрета (количество цифр): "))
                k = int(input("Порог восстановления (сколько частей нужно для восстановления): "))
                
                secret, shares = sss.generate_and_split(n, secret_length, k)
                print(f"\nСгенерированный секрет: {secret}")
                print(f"\nДоли секрета (всего {n}, нужно {k} для восстановления):")
                for i, (x, y) in enumerate(shares, 1):
                    print(f"Доля {i}: x={x}, y={y}")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "2":
            try:
                secret = int(input("Введите секрет (число): "))
                n = int(input("Количество частей: "))
                k = int(input("Порог восстановления (сколько частей нужно для восстановления): "))
                
                shares = sss.split_existing_secret(secret, n, k)
                print(f"\nДоли секрета (всего {n}, нужно {k} для восстановления):")
                for i, (x, y) in enumerate(shares, 1):
                    print(f"Доля {i}: x={x}, y={y}")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "3":
            try:
                shares = []
                n = int(input("Сколько долей будете вводить: "))
                
                for i in range(n):
                    print(f"\nДоля {i+1}:")
                    x = int(input("x: "))
                    y = int(input("y: "))
                    shares.append((x, y))
                
                recovered_secret = sss.recover_secret_from_shares(shares)
                print(f"\nВосстановленный секрет: {recovered_secret}")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "4":
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
main()
