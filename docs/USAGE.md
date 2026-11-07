# Usage

From an installed checkout, launch the visible synthetic demo:

```bash
./launch --provider mock
```

For automatic local Ollama selection use `./launch`; read the provider banner before interpreting answers. Mock output is fixed synthetic text, not an answer to your question. [Setup](SETUP.md) explains local inference.

## Controls

| Input | Result |
| --- | --- |
| Terminal `/ask PROMPT` | Clear prior response, activate a new generation, stream answer |
| Terminal `/dismiss` | Clear HUD and cancel current request |
| Focused window Space | Inject device single-button event, clear locally, notify host to cancel |
| Lua single or long button callback | Same dismissal behavior; real gesture hardware not tested |
| Terminal `/save /tmp/quiet-glasses.png` | Explicitly persist current framebuffer (256×256) |
| Terminal `/quit` or stdin EOF | Clear, stop emulator and exit |
| Window close button | Clear and stop viewer; terminal remains running |

Other text is ignored. There is no voice input, hotkey activation outside the window, double-button action, mouse interaction or document reader. Use nonempty questions; whitespace-only prompts and save errors are not handled gracefully by the console.

## Example session

```text
/ask In two short sentences, why does the sky look blue?
```

Watch the window and wait for the first-visible timing line. Then optionally save it:

```text
/save /tmp/quiet-glasses.png
/dismiss
/quit
```

The parent directory for saved images must exist. Avoid private content in screenshots. Dismissal also works while inference is waiting; a new `/ask` replaces previous work. Requests that fail clear the display and print a generic failure message.

## Text navigation and reader status

There is no manual scrolling, pagination, document loading or reader mode. The display follows the most recent six wrapped lines automatically; older content falls out of view. Only the most recent 4096 source characters are retained for layout. Text is ASCII-normalized, so non-Latin text and many symbols disappear. Translation and diagram rendering are future work.

The terminal prints per-request metrics; window presentation metrics require a viewer. A black screenshot proves cleared emulator pixels, not optical transparency. See [testing](TESTING.md) for timing definitions and [experiments](EXPERIMENTS.md) for the explicit screenshot reproduction script.
