import select
import sys

from ethernet import Ethernet          # your Ethernet class

ETH_P_CHAT = 0x88B5
BROADCAST  = "FF:FF:FF:FF:FF:FF"

# ---- edit these three ----
INTERFACE = "lan"                       # Your interface
MY_MAC    = "02:00:00:00:00:01"         # Your assigned MAC
NICKNAME  = "changeme"                  # Your pick a nickname
# --------------------------


class ChatClient:
    def __init__(self):
        pass # Create a socket and bind to the interface, call it self.sock

    # ===== YOU IMPLEMENT =====

    def send(self, text: str) -> None:
        """Build a chat frame for `text` (per the protocol) and transmit it.
        1. payload = nick_len + nickname + msg_len + message
        2. frame   = [broadcast dst][MY_MAC src][ETH_P_CHAT] + payload
        3. self.sock.send(frame)
        """
        raise NotImplementedError

    def parse(self, raw: bytes):
        """Parse a received raw frame -> (nickname, message), or None to ignore.
        1. frame = Ethernet(raw)
        2. ignore our own echo:  if frame.src_mac == mac_to_bytes(MY_MAC): return None
        3. from frame.payload, read nick_len, nickname, msg_len, message
        4. return (nickname, message)
        """
        raise NotImplementedError

    # ==========================

    def run(self) -> None:
        print(f"[public chat] you are '{NICKNAME}'. Type a message, press Enter.")
        print("> ", end="", flush=True)
        while True:
            readable, _, _ = select.select([sys.stdin, self.sock], [], [])
            for source in readable:
                if source is self.sock:
                    parsed = self.parse(self.sock.recv(65535))
                    if parsed is not None:
                        nickname, message = parsed
                        print(f"\r{nickname}: {message}\n> ", end="", flush=True)
                else:
                    self.send(sys.stdin.readline().strip())
                    print("> ", end="", flush=True)


if __name__ == "__main__":
    ChatClient().run()