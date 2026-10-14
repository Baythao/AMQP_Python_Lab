import json

import pika


QUEUE_NAME = "sensor_data_queue"


def handle_message(channel, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))

        device_id = data["device_id"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])

        print(f"Device: {device_id}")
        print(f"Temperature: {temperature:.1f}")
        print(f"Humidity: {humidity:.1f}")

        if temperature > 35:
            print("CANH BAO: Nhiet do cao")

        if humidity < 40:
            print("CANH BAO: Do am thap")

        print("-" * 35, flush=True)

    except (ValueError, KeyError, TypeError, UnicodeDecodeError) as error:
        print(f"Dữ liệu không hợp lệ: {error}", flush=True)
        channel.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False,
        )
        return

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

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=handle_message,
        auto_ack=False,
    )

    print("Đã kết nối RabbitMQ.")
    print("Đang chờ dữ liệu cảm biến. Nhấn Ctrl+C để dừng.\n")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nĐã dừng giám sát.")
        channel.stop_consuming()
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()