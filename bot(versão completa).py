from minecraft.networking.connection import Connection
from minecraft.networking.packets import (
    PositionAndLookPacket,
    ChatPacket
)
from minecraft.networking.packets.clientbound.play import PlayerPositionAndLookPacket
import time
import random
import threading

# Configurações do servidor e do bot
server_address = "ByteHackers.aternos.me"
server_port = 42029
username = "BOT"

# Conectar ao servidor
connection = Connection(server_address, server_port, username=username)

# Variáveis de posição
bot_position = {"x": 0, "y": 64, "z": 0}
position_received = threading.Event()

# Função chamada quando o servidor envia a posição inicial
def on_position_and_look(packet):
    bot_position["x"] = packet.x
    bot_position["y"] = packet.y
    bot_position["z"] = packet.z
    print(f"Posição inicial recebida: ({packet.x}, {packet.y}, {packet.z})")
    position_received.set()

# Função para movimentação do bot
def move_bot():
    position_received.wait()  # Espera a posição inicial antes de começar

    while True:
        bot_position["x"] += random.uniform(-0.5, 0.5)
        bot_position["z"] += random.uniform(-0.5, 0.5)

        packet = PositionAndLookPacket()
        packet.x = bot_position["x"]
        packet.feet_y = bot_position["y"]
        packet.z = bot_position["z"]
        packet.yaw = random.uniform(0, 360)
        packet.pitch = 0
        packet.on_ground = True

        connection.write_packet(packet)
        print(f"Movendo para ({bot_position['x']:.2f}, {bot_position['y']:.2f}, {bot_position['z']:.2f})")

        time.sleep(10)

# Função para enviar mensagem no chat
def send_chat_message(message):
    packet = ChatPacket()
    packet.message = message
    connection.write_packet(packet)
    print(f"Mensagem enviada: {message}")

messages = [
    "O ChefinhoBot tá online! 🤖",
    "Ainda por aqui hein 👀",
    "Servidor não vai cair hoje não!",
    "De pé firme no ByteHackers!"
]
# Função para o bot mandar mensagem a cada X segundos
def send_periodic_messages():
    while True:
        message = random.choice(messages)
        send_chat_message(message)
        time.sleep(420)

# Conectar e iniciar o bot
def start_bot():
    connection.register_packet_listener(on_position_and_look, PlayerPositionAndLookPacket)
    connection.connect()
    print(f"{username} conectado ao servidor {server_address}:{server_port} com sucesso!")

    # Inicia as threads de movimentação e mensagens periódicas
    threading.Thread(target=move_bot, daemon=True).start()
    threading.Thread(target=send_periodic_messages, daemon=True).start()

    # Mantém a thread principal viva
    while True:
        time.sleep(1)

# Iniciar
if __name__ == "__main__":
    start_bot()
