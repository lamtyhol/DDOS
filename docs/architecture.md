# Kiến trúc dự án

## Tổng quan

Dự án này được tổ chức theo mô hình đơn giản:

- `ddos/config.py`: cấu hình ứng dụng
- `ddos/analyzer.py`: phân tích lưu lượng và cảnh báo
- `ddos/monitor.py`: theo dõi lịch sử sự kiện
- `main.py`: entry point
- `tests/`: kiểm thử cơ bản

## Mở rộng trong tương lai

Bạn có thể thêm:
- xử lý log thời gian thực
- lưu trữ dữ liệu vào cơ sở dữ liệu
- giao diện dashboard
- phân tích biểu đồ
- API HTTP cho hệ thống giám sát
