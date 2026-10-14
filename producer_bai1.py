import pika

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "iot_lab_queue"

STUDENT_ID = "B22DCCN072"
STUDENT_NAME = "Thào A Bảy"


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print("Đã kết nối RabbitMQ.")
    print("Nhấn Enter ở dòng nội dung để kết thúc.")

    try:
        while True:
            greeting = input("Nhập nội dung chào mừng: ").strip()
            if not greeting:
                break

            message = (
                f"{greeting} - {STUDENT_ID} - {STUDENT_NAME}"
            )

            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=message.encode("utf-8"),
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                ),
            )
            print(f"Đã gửi: {message}")

    finally:
        connection.close()
        print("Đã ngắt kết nối.")


if __name__ == "__main__":
    main()