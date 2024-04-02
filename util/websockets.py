import hashlib
import base64

def compute_accept(ws_key):
    # GUID from slide 7?
    return base64.b64encode(hashlib.sha1((ws_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()


def parse_ws_frame(ws_frame_bytes):
    class WebSocketFrame:
        def __init__(self, fin_bit, opcode, payload_length, payload):
            self.fin_bit = fin_bit
            self.opcode = opcode
            self.payload_length = payload_length
            self.payload = payload

    first_byte = ws_frame_bytes[0]
    second_byte = ws_frame_bytes[1]

    fin_bit = (first_byte >> 7) & 0x01
    opcode = first_byte & 0x0F
    mask_bit = (second_byte >> 7) & 0x01
    payload_length = second_byte & 0x7F

    payload, payload_start = bytearray(), 0

    if payload_length < 126:
        payload_start = 2
    elif payload_length == 126:
        payload_start = 4
        payload_length = int.from_bytes(ws_frame_bytes[2:4], byteorder='big')
    elif payload_length == 127:
        payload_start = 10
        payload_length = int.from_bytes(ws_frame_bytes[2:10], byteorder='big')

    if mask_bit == 0x01:
        mask = ws_frame_bytes[payload_start:payload_start + 4]
        payload_start += 4
        for i in range(payload_start, payload_start + payload_length):
            mask_index = (i - payload_start) % 4
            xor_byte = ws_frame_bytes[i] ^ mask[mask_index] #xor
            payload.append(xor_byte)
    else:
        payload = ws_frame_bytes[payload_start:payload_start + payload_length]

    return WebSocketFrame(fin_bit, opcode, payload_length, payload)


def generate_ws_frame(payload_bytes):
    fin_bit, opcode = 0x80, 0x0001 
    fin_opcode = fin_bit | opcode
    frame = bytearray([fin_opcode])
    
    if len(payload_bytes) < 126:
        frame.append(len(payload_bytes))
    elif len(payload_bytes) < 65536:
        frame.append(126)
        frame.extend(len(payload_bytes).to_bytes(2))
    else:
        frame.append(127)
        frame.extend(len(payload_bytes).to_bytes(8))

    frame.extend(payload_bytes)
    return bytes(frame)