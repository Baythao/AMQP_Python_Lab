from datetime import datetime
from pathlib import Path

import pika


EXCHANGE_NAME = "iot_alert_topic_exchange"
QUEUE_NAME = "all_alert_queue"

# File log nằm cùng thư mục với chương trình
LOG_FILE = Path(__file__).resolve().parent / "iot_alerts.log"


def handle_message(channel, method, properties, body):
    message = body.decode("utf-8")
    level = method.routing_key
    received_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    log_line = (
        f"[{received_time}] "
        f"[{QUEUE_NAME}] "
        f"[{level}] Đã nhận: {message}"
    )

    # Chế độ "a": ghi nối tiếp, không xóa log cũ
    # UTF-8: lưu đúng tiếng Việt có dấu
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(log_line + "\n")

    print(log_line, flush=True)

    # Chỉ xác nhận sau khi ghi log thành công
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="127.0.0.1",
            port=5672,
            virtual_host="/",
            credentials=pika.PlainCredentials("guest", "guest"),
        )
    )

    try:
        channel = connection.channel()

        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type="topic",
            durable=True,
        )

        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True,
        )

        # Nhận tất cả các mức cảnh báo
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=QUEUE_NAME,
            routing_key="#",
        )

        # Mỗi lần xử lý một thông điệp chưa xác nhận
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=handle_message,
            auto_ack=False,
        )

        print("Đã kết nối RabbitMQ.")
        print("Đang nhận tất cả cảnh báo: info, warning, critical.")
        print("File log:", LOG_FILE)
        print("Nhấn Ctrl+C để dừng.\n")

        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình nhận cảnh báo.")

    except OSError as error:
        print(f"\nKhông ghi được file log: {error}")
        print("Thông điệp chưa được xác nhận với RabbitMQ.")

    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()