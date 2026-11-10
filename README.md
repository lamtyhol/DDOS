# DDoS Learning Project

Một khung dự án mẫu dành cho việc học và nghiên cứu về phát hiện, phân tích và giám sát lưu lượng mạng có dấu hiệu tấn công DDoS.

## Mục tiêu
- Cung cấp một cấu trúc dự án rõ ràng.
- Tách rõ lớp cấu hình, phân tích và giám sát.
- Dễ mở rộng cho các bài thực hành hoặc prototype tiếp theo.

## Cấu trúc

```text
DDOS/
├── README.md
├── .gitignore
├── requirements.txt
├── main.py
├── ddos/
│   ├── __init__.py
│   ├── config.py
│   ├── analyzer.py
│   └── monitor.py
├── tests/
│   └── test_analyzer.py
└── docs/
    └── architecture.md
```

## Bắt đầu

```bash
python -m venv .venv
source .venv/bin/activate  # trên Linux/macOS
# hoặc .venv\Scripts\activate trên Windows
pip install -r requirements.txt
python main.py
```

## Ghi chú

Dự án này chỉ nhằm mục đích học tập và nghiên cứu an ninh mạng, không dùng cho các hành vi gây hại hoặc tấn công mạng.
