## Họ tên thành viên nhóm:
- Hoàng Khải Hưng B23DCCN365
- Thào A Bảy B22DCCN072
- Trịnh Quang Anh B23DCCN055

# Buổi thực hành: Lập trình Python với giao thức AMQP
- Bộ bài gồm ba mô hình: 
+ producer/consumer qua queue.
+ Telemetry cảm biến IoT dạng JSON.
+ Định tuyến cảnh báo qua direct exchange.

## 1. Chuẩn bị
- Python 3.x
- Hệ thống sử dụng `RabbitMQ Server 4.3.6`, chạy trên `Erlang/OTP 28.5.0.7.`
- Thư viện `pika`
- Tạo môi trường ảo: `python -m venv .venv`
- Kích hoạt môi trường ảo: `.\.venv\Scripts\Activate.ps1`
- Cài thư viện: `python -m pip install pika`
- Mặc định các chương trình kết nối `localhost:5672`, virtual host `/`, tài khoản `guest` và mật khẩu `guest`. Tài khoản `guest` của RabbitMQ thường chỉ cho kết nối từ máy cài broker. Với broker khác, đặt biến môi trường trước khi chạy:
```powershell
$env:RABBITMQ_HOST = "127.0.0.1"
$env:RABBITMQ_PORT = "5672"
$env:RABBITMQ_USER = "guest"
$env:RABBITMQ_PASSWORD = "guest"
$env:RABBITMQ_VHOST = "/"
```

## 2. Thực hiện
## Bài 1 — Gửi và nhận message
- Chạy: 
    + Terminal 1: `python consumer_bai1.py` trước
    + Terminal 2: `python producer_bai1.py` sau
- `Kết quả dặt được:`
    + Terminal 2:
        Đã kết nối RabbitMQ.
        Nhấn Enter ở dòng nội dung để kết thúc.
        Nhập nội dung chào mừng: Xin chao tu ung dung Python AMQP
        Đã gửi: Xin chao tu ung dung Python AMQP - B22DCCN072 - Thào A Bảy
        Nhập nội dung chào mừng: 
    + Terminal 1:
        Đang lắng nghe queue: iot_lab_queue
        Nhấn Ctrl+C để dừng.
        Đã nhận message: Xin chao tu ung dung Python AMQP - B22DCCN072 - Thào A Bảy
        Thời gian nhận: 15:45:45

## 3. Bài 2 — Dữ liệu cảm biến IoT
- Chạy: 
    + Terminal 1: `python monitor_consumer_bai2.py` trước
    + Terminal 2: `python sensor_producer_bai2.py` sau
- `Kết quả dặt được:`
    + Terminal 2:
        Đã kết nối RabbitMQ.
        Đang mô phỏng các thiết bị cảm biến.
        Queue: sensor_data_queue
        Gửi dữ liệu mỗi 3 giây. Nhấn Ctrl+C để dừng.
    
        Đã gửi dữ liệu:
        Thiết bị: sensor01
        Nhiệt độ: 23.0 °C
        Độ ẩm: 62.5 %
        JSON: {"device_id": "sensor01", "temperature": 23.0, "humidity": 62.5}
        --------------------------------------------------
        Đã gửi dữ liệu:
        Thiết bị: sensor02
        Nhiệt độ: 21.5 °C
        Độ ẩm: 43.5 %
        JSON: {"device_id": "sensor02", "temperature": 21.5, "humidity": 43.5}
        --------------------------------------------------
        Đã gửi dữ liệu:
        Thiết bị: sensor03
        Nhiệt độ: 37.1 °C
        Độ ẩm: 75.3 %
        JSON: {"device_id": "sensor03", "temperature": 37.1, "humidity": 75.3}
        --------------------------------------------------
        Đã dừng cảm biến.
    
    + Terminal 1:
        Đã kết nối RabbitMQ.
        Đang chờ dữ liệu cảm biến. Nhấn Ctrl+C để dừng.
    
        Device: sensor01
        Temperature: 23.0
        Humidity: 62.5
        -----------------------------------
        Device: sensor02
        Temperature: 21.5
        Humidity: 43.5
        -----------------------------------
        Device: sensor03
        Temperature: 37.1
        Humidity: 75.3
        CANH BAO: Nhiet do cao
        -----------------------------------
        Đã dừng giám sát.

Producer gửi JSON mỗi 3 giây vào `sensor_data_queue`. Nhiệt độ được sinh ngẫu nhiên trong khoảng 20–40°C, độ ẩm trong khoảng 30–80%. Message có thêm thời điểm gửi UTC. Consumer cảnh báo khi nhiệt độ lớn hơn 35°C hoặc độ ẩm nhỏ hơn 40%. Tự động mã cảm biến khi chạy


## 4. Bài 3 — Exchange và routing key
- Mở ba terminal riêng và chạy hai consumer trước và theo thứ tự Terminal: 
    + Terminal 1: `python warning_consumer_bai3.py` 
    + Terminal 2: `python critical_consumer_bai3.py`
    + Terminal 3: `python all_alert_producer_bai3.py` Mở rông nhận tất cả cảnh báo bằng topic exchange.
    + Terminal 4: `python alert_producer_bai3.py` 
- `Kết quả dặt được:`
    + Terminal 4:
        Đã kết nối RabbitMQ.
        Bắt đầu gửi cảnh báo.
    
        - [info] Đã gửi tới hai exchange: Hệ thống cảm biến hoạt động bình thường.
        - [warning] Đã gửi tới hai exchange: Nhiệt độ phòng máy vượt ngưỡng cảnh báo.
        - [critical] Đã gửi tới hai exchange: Cảm biến kho lạnh mất kết nối nghiêm trọng.
    
    + Terminal 3:
        Đã kết nối RabbitMQ.
        Đang nhận tất cả cảnh báo: info, warning, critical.File log: D:\BTL_HK1_2026-2027\IOT\amqp_python_lab\iot_alerts.log
        Nhấn Ctrl+C để dừng.
    
        - [all_alert_queue] [info] Đã nhận: Hệ thống cảm biến hoạt động bình thường.
        - [all_alert_queue] [warning] Đã nhận: Nhiệt độ phòng máy vượt ngưỡng cảnh báo.
        - [all_alert_queue] [critical] Đã nhận: Cảm biến kho lạnh mất kết nối nghiêm trọng.
    
    + Terminal 2:
        Đã kết nối RabbitMQ.
        [critical_queue] Đang chờ cảnh báo mức critical.
        Nhấn Ctrl+C để dừng.
    
        - [critical_queue] Đã nhận: Cảm biến kho lạnh mất kết nối nghiêm trọng.
      
    + Terminal 1:
        Đã kết nối RabbitMQ.
        [warning_queue] Đang chờ cảnh báo mức warning.
        Nhấn Ctrl+C để dừng.
    
        - [warning_queue] Đã nhận: Nhiệt độ phòng máy vượt ngưỡng cảnh báo.
    
    - Consumer mới ghi toàn bộ cảnh báo vào iot_alerts.log.
    + File log `iot_alerts.log:`
        - 2026-10-14T16:41:19+07:00 | info | Hệ thống cảm biến hoạt động bình thường.
        - 2026-10-14T16:41:19+07:00 | warning | Nhiệt độ phòng máy vượt ngưỡng cảnh báo.
        - 2026-10-14T16:41:19+07:00 | critical | Cảm biến kho lạnh mất kết nối nghiêm trọng.

## 5. File nộp
- `producer_bai1.py`
- `consumer_bai1.py`
- `sensor_producer_bai2.py`
- `monitor_consumer_bai2.py`
- `alert_producer_bai3.py`
- `warning_consumer_bai3.py`
- `critical_consumer_bai3.py`
- `all_alert_consumer_bai3.py` Mở rộng
- `iot_alerts.log` Các cảnh báo
- `README.md`

