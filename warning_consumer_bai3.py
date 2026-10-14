import pika


EXCHANGE_NAME = "iot_alert_exchange"
QUEUE_NAME = "warning_queue"


def handle_message(channel, method, properties, body):
    # Giải mã nội dung tiếng Việt
    message = body.decode("utf-8")

    print(f"[{QUEUE_NAME}] Đã nhận: {message}", flush=True)

    # Xác nhận đã xử lý thông điệp
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
            exchange_type="direct",
            durable=True,
        )

        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True,
        )

        # Chỉ nhận thông điệp có routing key là warning
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=QUEUE_NAME,
            routing_key="warning",
        )

        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=handle_message,
            auto_ack=False,
        )

        print("Đã kết nối RabbitMQ.")
        print(f"[{QUEUE_NAME}] Đang chờ cảnh báo mức warning.")
        print("Nhấn Ctrl+C để dừng.\n")

        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình nhận cảnh báo warning.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()