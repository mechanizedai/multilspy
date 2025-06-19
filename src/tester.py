from multilspy.language_servers.superbol_language_server.superbol_server import Superbol
from multilspy.language_server import SyncLanguageServer
from multilspy.multilspy_logger import MultilspyLogger
from multilspy.multilspy_config import MultilspyConfig, Language
import time
import json
import asyncio
from pathlib import Path

# child_proc_env = {"SHELL": "/bin/bash", "CAML_LD_LIBRARY_PATH": "/home/rob/.opam/superbol-studio/lib/stublibs:/home/rob/.opam/superbol-studio/lib/ocaml/stublibs:/home/rob/.opam/superbol-studio/lib/ocaml", "OCAML_TOPLEVEL_PATH": "/home/rob/.opam/superbol-studio/lib/toplevel", "NVM_INC": "/home/rob/.nvm/versions/node/v20.8.1/include/node", "WSL2_GUI_APPS_ENABLED": "1", "WSL_DISTRO_NAME": "Ubuntu", "WT_SESSION": "5954269b-3556-495f-b613-20443b9d4fbe", "RBENV_SHELL": "bash", "AWS_REGION": "us-east-1", "NAME": "DESKTOP-2T5OF5H", "ORCHESTRAL_GIT_SSH_COMMAND": "ssh -i ~/.ssh/robertorch_github_ed25519", "PWD": "/home/rob/playing/opensource/multilspy/src", "LOGNAME": "rob", "MANPATH": ":/home/rob/.opam/superbol-studio/man", "PNPM_HOME": "/home/rob/.local/share/pnpm", "OPAM_SWITCH_PREFIX": "/home/rob/.opam/superbol-studio", "HOME": "/home/rob", "LANG": "C.UTF-8", "WSL_INTEROP": "/run/WSL/9988_interop", "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:", "VIRTUAL_ENV": "/home/rob/playing/opensource/multilspy/venv", "WAYLAND_DISPLAY": "wayland-0", "NVM_DIR": "/home/rob/.nvm", "LESSCLOSE": "/usr/bin/lesspipe %s %s", "TERM": "xterm-256color", "SCALA_HOME": "/home/rob/pyspark-setup/scala-2.13.3", "LESSOPEN": "| /usr/bin/lesspipe %s", "USER": "rob", "DISPLAY": ":0", "SHLVL": "1", "NVM_CD_FLAGS": "", "SPARK_HOME": "/home/rob/pyspark-setup/spark-3.3.0-bin-hadoop3", "VIRTUAL_ENV_PROMPT": "(venv) ", "MECHANIZED_GIT_SSH_COMMAND": "ssh -i ~/.ssh/mechanized_rsa", "XDG_RUNTIME_DIR": "/mnt/wslg/runtime-dir", "PS1": "((venv) ) \\[\\e]0;\\u@\\h: \\w\\a\\]${debian_chroot:+($debian_chroot)}\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ ", "WSLENV": "WT_SESSION:WT_PROFILE_ID:", "XDG_DATA_DIRS": "/usr/local/share:/usr/share:/var/lib/snapd/desktop", "PERSONAL_GIT_SSH_COMMAND": "ssh -i ~/.ssh/rebrowning_github_ed25519", "VAGRANT_WSL_ENABLE_WINDOWS_ACCESS": "1", "BROWSER": "/usr/bin/wslview", "PATH": "/home/rob/.opam/superbol-studio/bin:/home/rob/playing/opensource/multilspy/venv/bin:/home/rob/.local/bin:/home/rob/.rbenv/shims:/home/rob/.rbenv/bin:/home/rob/.local/share/pnpm:/home/rob/.nvm/versions/node/v20.8.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Python313/Scripts/:/mnt/c/Python313/:/mnt/c/Program Files/Oculus/Support/oculus-runtime:/mnt/c/Program Files/Common Files/Oracle/Java/javapath:/mnt/c/Windows/system32:/mnt/c/Windows:/mnt/c/Windows/System32/Wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0/:/mnt/c/Windows/System32/OpenSSH/:/mnt/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/mnt/c/WINDOWS/system32:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/:/mnt/c/WINDOWS/System32/OpenSSH/:/mnt/c/Program Files/Git/cmd:/mnt/c/Program Files/Go/bin:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/c/WINDOWS/system32:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/:/mnt/c/WINDOWS/System32/OpenSSH/:/mnt/c/Program Files/dotnet/:/mnt/c/Program Files/nodejs/:/mnt/c/ProgramData/chocolatey/bin:/mnt/c/Program Files/NVIDIA Corporation/NVIDIA App/NvDLISR:/mnt/c/Users/Alucard/.local/bin:/mnt/c/Users/Alucard/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/Alucard/AppData/Local/Programs/Microsoft VS Code/bin:/mnt/c/Program Files (x86)/GitHub CLI/:/mnt/c/Users/Alucard/go/bin:/mnt/c/Users/Alucard/AppData/Roaming/npm:/mnt/c/Users/Alucard/AppData/Local/Programs/Windsurf/bin:/snap/bin:/home/rob/pyspark-setup/scala-2.13.3/bin:/home/rob/pyspark-setup/spark-3.3.0-bin-hadoop3/bin:/home/rob/.pulumi/bin:/usr/local/go/bin:/home/rob/go/bin", "OPAMNOENVNOTICE": "true", "NVM_BIN": "/home/rob/.nvm/versions/node/v20.8.1/bin", "HOSTTYPE": "x86_64", "PULSE_SERVER": "unix:/mnt/wslg/PulseServer", "WT_PROFILE_ID": "{2c4de342-38b7-51cf-b940-2309a097f518}", "OLDPWD": "/home/rob/playing/opensource/multilspy", "OPAM_LAST_ENV": "/home/rob/.opam/.last-env/env-aea116cf00631fcbddcc6e6e16897e25-0", "_": "/home/rob/playing/opensource/multilspy/venv/bin/python3"}
cwd = "/home/rob/playing/opensource/CobolCraft"
# start_independent_lsp_process = True

# async def run_superbol_lsp():
#     cmd = 'opam exec --switch superbol-studio -- superbol-free lsp'
#     print(f"Running: {cmd}")
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE,
#         stdin=asyncio.subprocess.PIPE,
#         env=child_proc_env,
#         cwd=cwd,
#         start_new_session=start_independent_lsp_process,
#     )
#     loop = asyncio.get_event_loop()
#     async def _monitor_process_exit():
#         if proc:
#             returncode = await proc.wait()
#             print(f"[LSP DEBUG] Process exited early with return code {returncode}")
#             if proc.stderr:
#                 try:
#                     stderr_output = await proc.stderr.read()
#                     print("[LSP DEBUG] Early stderr output:\n", stderr_output.decode("utf-8", errors="replace"))
#                 except Exception as e:
#                     print("[LSP DEBUG] Failed to read early server stderr:", e)
#             if proc.stdout:
#                 try:
#                     stdout_output = await proc.stdout.read()
#                     print("[LSP DEBUG] Early stdout output:\n", stdout_output.decode("utf-8", errors="replace"))
#                 except Exception as e:
#                     print("[LSP DEBUG] Failed to read early server stdout:", e)
    
#     loop.create_task(_monitor_process_exit())

#     # Example: Send an LSP initialize request (replace with actual LSP JSON)
#     # time.sleep(5)
#     body = {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"rootUri":"file:///home/rob/playing/opensource/CobolCraft","capabilities":{}}}
#     payload = json.dumps(body, check_circular=False, ensure_ascii=False, separators=(",", ":"))
#     initialize_msg = (
#         f'Content-Length: {len(payload)}\r\n\r\n'
#         f'{payload}'
#     )
#     proc.stdin.write(initialize_msg.encode('utf-8'))
#     await proc.stdin.drain()

#     # Read response (you'll need to parse headers and body per LSP spec)
#     response = await proc.stdout.read(4096)
#     print("LSP Response:", response.decode())

#     async def read_lsp_messages(proc):
#         buffer = b""
#         while True:
#             # Read header lines until we get Content-Length
#             headers = b""
#             while True:
#                 line = await proc.stdout.readline()
#                 if not line:
#                     return  # Process exited or pipe closed
#                 headers += line
#                 if line == b"\r\n":
#                     break  # End of headers

#             # Parse Content-Length
#             header_lines = headers.decode("utf-8", errors="replace").split("\r\n")
#             content_length = None
#             for h in header_lines:
#                 if h.lower().startswith("content-length:"):
#                     content_length = int(h.split(":")[1].strip())
#             if content_length is None:
#                 print("No Content-Length found in headers:", header_lines)
#                 continue

#             # Read the message body
#             body = await proc.stdout.readexactly(content_length)
#             print("LSP MESSAGE:", body.decode("utf-8", errors="replace"))

#     # In your main function, after sending the initialize message:
#     await read_lsp_messages(proc)
#     # while True:
#     #     line = await proc.stdout.readline()
#     #     if not line:
#     #         break  # EOF reached, process likely exited
#     #     print("LSP STDOUT:", line.decode(errors="replace").rstrip())
#     # # Keep the process and pipes open as long as you need to communicate
#     # # When done, close stdin to signal shutdown
#     # await proc.wait()
#     # stdout, stderr = await proc.communicate(initialize_msg.encode('utf-8'))
#     # print("STDOUT:")
#     # print(stdout.decode())
#     # print("STDERR:")
#     # print(stderr.decode())
#     # print("Return code:", proc.returncode)

# if __name__ == "__main__":
#     asyncio.run(run_superbol_lsp())
from typing import List
PROJECT_ROOT = Path(cwd) 

extensions = [".cbl", ".cpy", ".jcl", '.cob' ]
cobol_files: List[Path] = []
for ext in extensions:
    cobol_files.extend(PROJECT_ROOT.rglob(f"*{ext}"))
    cobol_files.extend(PROJECT_ROOT.rglob(f"*{ext.upper()}"))

server = Superbol(
    config=MultilspyConfig(code_language=Language.COBOL, ignore_content_type_header=True),  # Replace with actual MultilspyConfig instance
    logger=MultilspyLogger(),  # Replace with actual MultilspyLogger instance
    repository_root_path=PROJECT_ROOT.as_posix()
)

ss = SyncLanguageServer(server)

print("Starting Superbol Language Server...")
with ss.start_server() as server:
    print("Superbol Language Server started successfully.")
    for file_path in cobol_files:
        print(f"opening {file_path.as_posix()}")
        server.open_file(file_path.as_posix())
    
    for file_path in cobol_files:
        path = file_path.as_posix()
        print(f"getting symbols for {path}")
        try:
            res = server.request_document_symbols(path)
        except:
            continue
        symbols = res[0]
        for symbol in symbols:
            print(symbol)
            
            try:
                references = server.request_references(
                    path,
                    line=symbol['range']['start']['line'],
                    column=symbol['range']['start']['character']
                )
            except:
                continue

            for reference in references:
                print(reference)
                input()