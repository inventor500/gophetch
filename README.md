# Features

1. Send request for directory listing to server, and then display the returned values.
2. Navigate to other remote directories from the current directory.
3. Download files from a directory.

# Brief Explanation of Gopher

Gopher is best thought of as a directory listing. Each page is an annotated directory listing, with links to files and other directories (which can be on other servers).

# Client Commands

To run the program, run the `gophetch` file. It is executable with `./gophetch` if you have a Python interpreter at `/usr/bin/python3`, otherwise it can be invoked with `python gophetch`.

| Command  | Description               |
|----------|---------------------------|
| `r`      | Reload                    |
| `g`      | Goto URL or linked buffer |
| `d`      | Download                  |
| `p`      | Print Buffer              |
| ``     | Exit (Sends EOF)          |
| ` RET` | Clear screen              |


`p` prints link numbers in front of directory links and downloadable files. `☰` represents a directory link.

`g` accepts either a URL or a link number.

`d` only accepts link numbers.

# Example Session

`g gopher.floodgap.com`
`p`
`d 0`
`g 13`
`p`
`g 15`
`p`
`g 7`
`p`
`d 0`
``

# Useful Sites

| Site                       | Description                         |
|----------------------------|-------------------------------------|
| <gopher.floodgap.com>      | The traditional gopher introduction |
| <gopher.bitreich.org/lawn> | Organized list of other sites       |
| <gopher.fnord.one/Mirrors> | RFCs, PEPs, and more                |

# Notes

1. Not all gopher types are implemented. Any type that requires (or often requires) supporting an additional protocol is disabled, and will be displayed the same as informational text. This includes HTML, as that often is a link to the regular internet (requiring an HTTP request). Searching is also not implemented.
2. Links are displayed in blue.
3. Informational text is displayed in green.
4. Error text is displayed in red.
5. Downloaded files are named by their network path. For example, `gopher.example.com/myfile.txt` will be saved as `myfile.txt`.
6. The commands for this client are loosely inspired by ed.
7. This program cannot parse malformed buffers.
8. If the prompt (`ゴーフアー`) does not display correctly, install a Japanese font.
