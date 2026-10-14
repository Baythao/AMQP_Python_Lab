import json
import random

import pika


QUEUE_NAME = "sensor_data_queue"


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="127.0.0.1",
            port=5672,
            virtual_host="/",
            credentials=pika.PlainCredentials("guest", "guest"),
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print("Đã kết nối RabbitMQ.")
    print("Đang mô phỏng các thiết bị cảm biến.")
    print("Queue:", QUEUE_NAME)
    print("Gửi dữ liệu mỗi 3 giây. Nhấn Ctrl+C để dừng.\n")

    sensor_number = 1

    try:
        while True:
            data = {
                "device_id": f"sensor{sensor_number:02d}",
                "temperature": round(random.uniform(20, 45), 1),
                "humidity": round(random.uniform(25, 85), 1),
            }

            message = json.dumps(data, ensure_ascii=False)

            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=message.encode("utf-8"),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    content_encoding="utf-8",
                    delivery_mode=2,
                ),
            )

            print("Đã gửi dữ liệu:")
            print("Thiết bị:", data["device_id"])
            print("Nhiệt độ:", data["temperature"], "°C")
            print("Độ ẩm:", data["humidity"], "%")
            print("JSON:", message)
            print("-" * 50, flush=True)

            sensor_number += 1
            connection.sleep(3)

    except KeyboardInterrupt:
        print("\nĐã dừng cảm biến.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()