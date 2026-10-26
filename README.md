# ascii-player

Play a video inside your terminal as animated ASCII art.

`higuruma.py` reads a video file with OpenCV, converts each frame to grayscale,
maps the pixels onto an ASCII brightness ramp, and prints the result in green
using ANSI escape codes to redraw the terminal in place.

## Features

- Real-time video playback in the terminal
- Contrast enhancement with CLAHE and a sharpening kernel for crisper output
- Automatic aspect-ratio correction for terminal characters (which are roughly
  twice as tall as they are wide)
- Honors the source video's frame rate, with a fallback when it is not reported
- Cross-platform terminal clearing (Windows and Unix-like systems)

## Requirements

- Python 3.8+
- A terminal that supports ANSI escape sequences (Windows Terminal, PowerShell,
  or any modern Linux/macOS terminal)
- The following Python packages:

  ```text
  opencv-python
  numpy
  colorama
  ```

## Installation

```bash
git clone https://github.com/miggy158/ascii-player.git
cd ascii-player
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install opencv-python numpy colorama
```

## Usage

1. Put the video you want to play in the project root and name it `video.mp4`
   (or change `VIDEO_PATH` in `higuruma.py`).
2. Run the script:

   ```bash
   python higuruma.py
   ```

The terminal is cleared and the video plays until it ends or you interrupt it
with `Ctrl+C`.

## Configuration

Tune the playback by editing the constants at the top of `higuruma.py`:

| Constant         | Default          | Description                                                                 |
| ---------------- | ---------------- | --------------------------------------------------------------------------- |
| `ASCII_CHARS`    | `" .,:;i1tfLCG08@"` | Brightness ramp, ordered from darkest (space) to brightest (`@`).        |
| `VIDEO_PATH`     | `"video.mp4"`    | Path to the video file to play.                                             |
| `FRAME_WIDTH`    | `100`            | Output width in characters. Lower it for small terminals, raise it for more detail. |
| `FPS_FALLBACK`   | `30`             | Frame rate used when the video does not report a valid FPS.                 |
| `SHARPEN_KERNEL` | 3x3 sharpen      | Convolution kernel applied before the ASCII conversion.                     |

Smaller `FRAME_WIDTH` values render faster; larger values look more detailed but
use more CPU and need a wider terminal.

## How it works

1. **Open the video** — `cv2.VideoCapture` loads `VIDEO_PATH` and reads its FPS.
2. **Resize** — each frame is scaled to `FRAME_WIDTH` characters wide. The height
   is multiplied by `0.5` to compensate for the tall shape of terminal
   characters.
3. **Grayscale + enhance** — the frame is converted to grayscale, sharpened with
   a 3x3 kernel, and passed through CLAHE (contrast limited adaptive histogram
   equalization) to bring out detail in dark and bright regions.
4. **Map to ASCII** — every pixel value (0–255) is scaled to an index in
   `ASCII_CHARS`, producing one character per pixel.
5. **Draw** — the cursor is moved to the top-left with `\033[H` and the frame is
   printed in green, giving the appearance of animation.

## Troubleshooting

- **`Cannot open video.`** — Check that `video.mp4` exists in the working
  directory, or update `VIDEO_PATH` with an absolute path. Confirm OpenCV can
  decode the file's codec.
- **Output scrolls instead of animating** — Your terminal may be adding new
  content faster than it can redraw, or the window is shorter than the rendered
  frame. Reduce `FRAME_WIDTH`, or resize the terminal.
- **Playback is choppy** — Rendering is CPU-bound. Reduce `FRAME_WIDTH` or use a
  lower-resolution source video.
- **Garbled colors or escape characters** — Use a terminal with ANSI support
  (Windows Terminal is recommended over the legacy console).
- **`ModuleNotFoundError`** — Activate the virtual environment and reinstall the
  dependencies listed above.

## License

No license has been specified for this project.
