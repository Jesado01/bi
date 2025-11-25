import pika
import json
import time
import threading
import os

from dotenv import load_dotenv
load_dotenv(override=True)

from agents.refiner_core import CoreRefinerState
from agents.agent_setup import setup_refiner_framework


# --- Connection Details ---
RABBIT_HOST = 'localhost'
RABBIT_USER = 'guest'
RABBIT_PASS = 'guest'
CREDENTIALS = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)

# --- Queue Names ---
INPUT_QUEUE_NAME = 'bian_queue'
OUTPUT_QUEUE_NAME = 'generator_queue'

def save_requirements(requirements: str, output_dir: str = "output", file_name: str = "api_requirements.md"):
    """Save the generated requirements to a markdown file."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = Path(output_dir) / file_name
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print(f"\n✅ Requirements saved to: {output_path.absolute()}")

def do_work(channel, delivery_tag, body):
    """
    This function runs in a separate thread and performs the slow task.
    """
    message = json.loads(body.decode())
    print(f"    [Thread] Starting long-running task for message: {message}")

    initial_state = CoreBianState(
        errors=[],
        module_results={},
        target_architecture="multimodule_dinners",
        bian_dir=message['bianContract']+'/output', 
        endpoints_dir=message['output']+'/reqs'
    )

    # Setup and run the framework
    print("🚀 Starting analysis...")
    framework = setup_agent_framework(initial_state, api_key=os.getenv('ANTHROPIC_API_KEY'))
    final_state = framework.start_analysis(initial_state)

    # Print summary
    print("\n📊 Analysis Complete!")
    print(f"🔍 Detected Language: {final_state.get('target_language', 'Unknown')}")
    print(f"🛠️  Detected Framework: {final_state.get('target_framework', 'Unknown')}")
    
    # Save requirements if they were generated
    if 'updated_requirements' in final_state:
        save_requirements(final_state['updated_requirements'], file_name="updated_requirements.md")
        save_requirements(final_state['generated_requirements'], file_name="api_requirements.md")
    
    # Print any errors that occurred
    if final_state.get('errors'):
        print("\n❌ Errors encountered:")
        for error in final_state['errors']:
            print(f"- {error}")

    print(f"    [Thread] Task finished. Scheduling {len(messages_to_publish)} result(s) to be published.")

    def publish_result():
        channel.basic_publish(
            exchange='',
            routing_key=OUTPUT_QUEUE_NAME,
            body=json.dumps(message)
        )
        print(f"[*] Sent result message to queue '{OUTPUT_QUEUE_NAME}'.\n")
        # Acknowledge the message only after the work is done and published
        channel.basic_ack(delivery_tag=delivery_tag)

    # Ask the main I/O loop to run the publish_result function
    channel.connection.add_callback_threadsafe(publish_result)


def process_message(channel, method, properties, body):
    """
    This callback is now very fast. It just starts a new thread.
    """
    print(f"[*] Received message. Offloading to a worker thread.")

    # Create and start a new thread to do the actual work
    worker_thread = threading.Thread(
        target=do_work,
        args=(channel, method.delivery_tag, body)
    )
    worker_thread.start()


def main():
    """Main function to set up the connection and start consuming."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBIT_HOST,
            credentials=CREDENTIALS
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue=INPUT_QUEUE_NAME, durable=True)
    channel.queue_declare(queue=OUTPUT_QUEUE_NAME, durable=True)

    # Prevents the consumer from grabbing all messages at once if they are busy
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=INPUT_QUEUE_NAME,
        on_message_callback=process_message
    )

    print(f"[*] Waiting for messages on queue '{INPUT_QUEUE_NAME}'. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("[-] Stopping consumer.")
        connection.close()


if __name__ == '__main__':
    main()