import pika
from datetime import datetime

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "iot_lab_queue"


def on_message(channel, method, properties, body):
    message = body.decode("utf-8")
    receive_time = datetime.now().strftime("%H:%M:%S")

    print(f"Đã nhận message: {message}")
    print(f"Thời gian nhận: {receive_time}")
    print()

    # Xác nhận đã xử lý message
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=on_message,
        auto_ack=False,
    )

    print(f"Đang lắng nghe queue: {QUEUE_NAME}")
    print("Nhấn Ctrl+C để dừng.")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()