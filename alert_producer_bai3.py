import pika


DIRECT_EXCHANGE = "iot_alert_exchange"
TOPIC_EXCHANGE = "iot_alert_topic_exchange"


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

        # Exchange của bài gốc
        channel.exchange_declare(
            exchange=DIRECT_EXCHANGE,
            exchange_type="direct",
            durable=True,
        )

        # Exchange của phần mở rộng
        channel.exchange_declare(
            exchange=TOPIC_EXCHANGE,
            exchange_type="topic",
            durable=True,
        )

        alerts = [
            ("info", "Hệ thống cảm biến hoạt động bình thường"),
            ("warning", "Nhiệt độ phòng máy vượt ngưỡng cảnh báo"),
            ("critical", "Cảm biến kho lạnh mất kết nối nghiêm trọng"),
        ]

        print("Đã kết nối RabbitMQ.")
        print("Bắt đầu gửi cảnh báo.\n")

        for level, message in alerts:
            # Gửi đến cả hai exchange
            for exchange in (DIRECT_EXCHANGE, TOPIC_EXCHANGE):
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=level,
                    body=message.encode("utf-8"),
                    properties=pika.BasicProperties(
                        content_type="text/plain",
                        content_encoding="utf-8",
                        delivery_mode=2,
                    ),
                )

            print(f"[{level}] Đã gửi tới hai exchange: {message}")

        print("\nĐã gửi xong 3 cảnh báo.")

    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()