# Constraint Protocol Wire Format

**Binary protocol for serial/I2C/SPI transport of constraint-theory music events.**

Used by `constraint-mux` and any hardware implementing the lattice oscillator
ecosystem. Designed for minimal latency on low-bandwidth links.

---

## Frame Format

```
┌──────┬──────┬──────┬──────────────┬──────┐
│ SYNC │ LEN  │ CMD  │ DATA[0..N-1] │ CRC8 │
│ 0xAA │ u8   │ u8   │ bytes        │ u8   │
└──────┴──────┴──────┴──────────────┴──────┘
```

| Field | Size | Description |
|-------|------|-------------|
| SYNC  | 1 byte | Always `0xAA` — used for frame synchronization and byte-level alignment |
| LEN   | 1 byte | Length of DATA field (0–255). Does NOT include SYNC, LEN, CMD, or CRC. |
| CMD   | 1 byte | Command identifier (see below) |
| DATA  | LEN bytes | Command-specific payload |
| CRC8  | 1 byte | CRC-8 over SYNC + LEN + CMD + DATA. Polynomial: `0x07` (CRC-8-CCITT). |

**Total frame size:** 4 + LEN bytes (minimum 4 bytes for LEN=0).

---

## CRC-8 Computation

Polynomial: `0x07` (x⁸ + x² + x + 1), init = `0x00`, no final XOR.

```c
uint8_t crc8(const uint8_t *data, size_t len) {
    uint8_t crc = 0x00;
    for (size_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 0x80)
                crc = (crc << 1) ^ 0x07;
            else
                crc = crc << 1;
        }
    }
    return crc;
}
// Call: crc8(frame, 3 + LEN)  -- covers SYNC + LEN + CMD + DATA
```

---

## Commands

| CMD  | Name              | LEN  | Description |
|------|-------------------|------|-------------|
| 0x01 | NOTE_ON           | 16   | Start a note |
| 0x02 | NOTE_OFF          | 16   | Stop a note |
| 0x03 | SET_SCALE         | 8    | Change the active tuning/scale |
| 0x04 | SET_DIAL          | 5    | Update a constraint dial |
| 0x05 | QUERY_CONSONANCE  | 4    | Request consonance score for a chord |
| 0x06 | CONSONANCE_RESP   | 8    | Response to QUERY_CONSONANCE |
| 0x07 | SET_VOICE_PARAMS  | 12   | Configure voice parameters |
| 0x08 | PING              | 0    | Link alive check |
| 0x09 | PONG              | 0    | Response to PING |
| 0x0A | RESET             | 0    | Reset all voices |
| 0xFF | ERROR             | 1+   | Error response (DATA[0] = error code) |

---

## Command Details

### NOTE_ON (0x01) / NOTE_OFF (0x02) — 16 bytes

```
┌──────────┬──────────┬────────────────────┐
│ Offset   │ Size     │ Field              │
├──────────┼──────────┼────────────────────┤
│ 0        │ 4 (f32)  │ frequency          │  Hz (IEEE 754 LE)
│ 4        │ 3 (i8×3) │ lattice_coords     │  (i, j, k) signed lattice position
│ 7        │ 1 (u8)   │ voice_id           │  0-255 (255 = auto-assign)
│ 8        │ 4 (f32)  │ consonance         │  Precomputed consonance (0.0-1.0)
│ 12       │ 1 (u8)   │ velocity           │  0-255 (for NOTE_ON, ignored for NOTE_OFF)
│ 13       │ 1 (u8)   │ channel            │  0-15 (MIDI-compatible)
│ 14       │ 2 (u8×2) │ reserved           │  Must be 0
└──────────┴──────────┴────────────────────┘
```

**Lattice coordinates** `(i, j, k)` encode the note's position in the
3D integer lattice:
- `i` = octave axis (2^i dimension)
- `j` = fifth axis (3^j dimension)
- `k` = third axis (5^k dimension)

**Frequency computation from lattice coords:**
```
freq = base_freq × 2^i × 3^j × 5^k
```

**Consonance** is precomputed by the sender using:
```
consonance = 1 / (1 + log₂(2^|i| × 3^|j| × 5^|k|))
```

### SET_SCALE (0x03) — 8 bytes

```
┌──────────┬──────────┬────────────────────┐
│ Offset   │ Size     │ Field              │
├──────────┼──────────┼────────────────────┤
│ 0        │ 1 (u8)   │ scale_id           │  Scale type (see below)
│ 1        │ 1 (u8)   │ root_note          │  0-11 (C=0, C#=1, ... B=11)
│ 2        │ 2 (u16)  │ num_notes          │  Number of notes in scale
│ 4        │ 4 (u32)  │ flags              │  Scale flags (bitfield)
└──────────┴──────────┴────────────────────┘
```

**Scale IDs:**
| ID  | Name |
|-----|------|
| 0   | Just Intonation (lattice) |
| 1   | 12-TET (standard) |
| 2   | Pythagorean |
| 3   | Meantone (¼ comma) |
| 4   | Custom (defined by flag bits) |

### SET_DIAL (0x04) — 5 bytes

```
┌──────────┬──────────┬────────────────────┐
│ Offset   │ Size     │ Field              │
├──────────┼──────────┼────────────────────┤
│ 0        │ 1 (u8)   │ dial_id            │  0=vertical, 1=horizontal, 2=spectral |
│ 1        │ 4 (f32)  │ value              │  0.0 to 1.0 (IEEE 754 LE)             │
└──────────┴──────────┴────────────────────┘
```

The three constraint dials control:
- **0 (vertical):** Harmonic range — how many partials/octaves to use
- **1 (horizontal):** Ratio complexity — which lattice ratios to include
- **2 (spectral):** Brightness — amplitude rolloff across partials

### QUERY_CONSONANCE (0x05) — 4 bytes

```
┌──────────┬──────────┬────────────────────┐
│ Offset   │ Size     │ Field              │
├──────────┼──────────┼────────────────────┤
│ 0        │ 1 (u8)   │ query_id           │  Matches response            │
│ 1        │ 1 (u8)   │ num_notes          │  Number of notes in chord   │
│ 2        │ 2 (u8×2) │ voice_ids          │  Voice IDs to evaluate      │
└──────────┴──────────┴────────────────────┘
```

### CONSONANCE_RESP (0x06) — 8 bytes

```
┌──────────┬──────────┬────────────────────┐
│ Offset   │ Size     │ Field              │
├──────────┼──────────┼────────────────────┤
│ 0        │ 1 (u8)   │ query_id           │  Matches QUERY_CONSONANCE   │
│ 1        │ 1 (u8)   │ num_notes          │  Notes evaluated            │
│ 2        │ 2        │ reserved           │                             │
│ 4        │ 4 (f32)  │ consonance         │  0.0 (dissonant) to 1.0 (consonant) │
└──────────┴──────────┴────────────────────┘
```

---

## Byte Order

All multi-byte fields are **little-endian** (matching ARM/RISC-V native order).

---

## Throughput Analysis

### Note Event Bandwidth (NOTE_ON = 16 bytes DATA + 4 overhead = 20 bytes total)

| Transport    | Speed     | Events/sec | Notes |
|-------------|-----------|------------|-------|
| UART Serial | 115200    | ~720       | Standard MIDI speed × 5 |
| UART Serial | 921600    | ~5,760     | Fast UART |
| I2C         | 100 kHz   | ~625       | Standard mode |
| I2C         | 400 kHz   | ~2,500     | Fast mode |
| I2C         | 1 MHz     | ~6,250     | Fast mode plus |
| SPI         | 1 MHz     | ~6,250     | Low-speed SPI |
| SPI         | 10 MHz    | ~62,500    | Standard SPI |
| SPI         | 50 MHz    | ~312,500   | High-speed SPI |
| USB 2.0     | 12 Mbps   | ~75,000    | Full-speed bulk |
| USB 2.0     | 480 Mbps  | ~3,000,000 | High-speed bulk |

### Calculation (for note events):
```
bytes_per_event = 4 (frame overhead) + 16 (NOTE_ON data) = 20 bytes
events_per_sec  = bitrate / 8 / bytes_per_event
```

**Example:** At 115200 baud serial with 8N1 (10 bits/byte):
```
115200 / 10 / 20 = 576 events/sec
```
Including protocol overhead (~10%), realistic throughput is **~520 events/sec**.
This is 4× MIDI's ~128 events/sec — more than sufficient for real-time polyphonic control.

---

## Synchronization

### Frame Detection

Receiver syncs by scanning for `0xAA`:
1. Read byte. If `0xAA`, potential frame start.
2. Read LEN. If LEN + 4 > buffer, skip (invalid).
3. Read CMD. Validate against known commands.
4. Read DATA[LEN].
5. Read CRC8. Compute CRC over received bytes. If match, process frame.
6. If mismatch, discard and resume scanning for `0xAA`.

### Multi-byte SYNC (optional for noisy links)

For environments with high bit-error rates, use double SYNC:
```
[0xAA] [0x55] [LEN] [CMD] [DATA...] [CRC8]
```
The `0xAA 0x55` pattern has low probability of appearing in random data
(1 in 65536), providing robust frame detection.

---

## Error Handling

| Error Code | Description |
|-----------|-------------|
| 0x01      | Invalid command |
| 0x02      | Invalid length |
| 0x03      | CRC mismatch |
| 0x04      | No free voices (NOTE_ON) |
| 0x05      | Voice not found (NOTE_OFF) |
| 0x06      | Invalid dial ID |
| 0x07      | Invalid frequency (≤ 0 or > Nyquist) |
| 0x08      | Buffer overflow |
| 0xFF      | Unknown error |

Error responses use CMD = 0xFF:
```
[0xAA] [LEN] [0xFF] [error_code] [details...] [CRC8]
```

---

## Example Sessions

### Simple note on/off (A440)

```
TX: AA 10 01 00 00 DC 00 00 00 00 00 00 00 00 00 FF 00 3F 00 00 00 FF 00 [CRC]
    │  │  │  ├───────────── frequency=440.0 ─────────────┤ │ i j k │vid│  cons │ vel│ch│00 00│
    │  │  │
    │  │  CMD=NOTE_ON
    │  LEN=16
    SYNC

TX: AA 10 02 00 00 DC 00 00 00 00 00 00 00 00 00 FF 00 3F 00 00 00 00 00 [CRC]
    CMD=NOTE_OFF (same structure, velocity ignored)
```

### Dial change

```
TX: AA 05 04 00 3F 00 00 00 [CRC]
    │  │  │  ├─ value=0.5 ─┤
    │  │  dial_id=0 (vertical)
    │  LEN=5
    SYNC
```

---

## Relationship to constraint-mux

The `constraint-mux` component uses this protocol to:
1. Receive dial positions from hardware controllers (SET_DIAL)
2. Send note events to synthesizer hardware (NOTE_ON/OFF)
3. Query consonance for real-time visual feedback (QUERY_CONSONANCE)
4. Change scales based on compositional context (SET_SCALE)

Any hardware implementing this protocol can participate in the
constraint-theory music ecosystem.
