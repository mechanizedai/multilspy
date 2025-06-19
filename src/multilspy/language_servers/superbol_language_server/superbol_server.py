from multilspy.multilspy_logger import MultilspyLogger
from multilspy.language_server import LanguageServer
from multilspy.multilspy_config import MultilspyConfig
from multilspy.lsp_protocol_handler.server import ProcessLaunchInfo
import subprocess
import shutil
import os
import asyncio
import logging
import json
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional, AsyncIterator

class Superbol(LanguageServer):
    """
    Provides Superbol specific instantiation of the LanguageServer class.
    Contains various configurations and settings specific to Superbol.
    """

    def __init__(self, config: MultilspyConfig, logger: MultilspyLogger, repository_root_path: str):
        self.setup_runtime_dependencies(logger, config)
        super().__init__(
            config,
            logger,
            repository_root_path,
            ProcessLaunchInfo(cmd=f"opam exec --switch superbol-studio -- superbol-free lsp", cwd=repository_root_path),
            "cobol",
        )
        self.server_ready = asyncio.Event()
        
    def _run_command(self, command: list[str], env: Optional[dict] = None) -> tuple[bool, str]:
        """Run a command and return whether it succeeded and its output."""
        try:
            result = subprocess.run(
                command,
                env=env,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)

    def setup_runtime_dependencies(self, logger: MultilspyLogger, config: MultilspyConfig) -> str:
        # check to see if opam is installed
        opam_path = shutil.which('opam')
        if not opam_path:
            raise RuntimeError("opam is not installed. Please install it using: sh <(curl -fsSL https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh)")

        # check if opam is initialized
        success, _ = self._run_command(['opam', 'var', 'root'])
        if not success:
            raise RuntimeError("opam is not initialized. Please run: opam init")

        # check to see if drom is installed
        env = dict(os.environ)
        success, _ = self._run_command(['opam', 'exec', '--', 'which', 'drom'], env)
        if not success:
            raise RuntimeError("drom is not installed. Please run: opam install drom -y")

        # check to see if superbol is installed and get its version
        success, output = self._run_command(
            ['opam', 'exec', '--', 'superbol-free', 'lsp', '--version'],
            env
        )
        if not success:
            raise RuntimeError("superbol is not installed or not properly configured. Please ensure it's installed using drom install --switch superbol-studio -y")

        logger.log(f"Superbol LSP server version: {output.strip()}", logging.INFO)
        print(f"Superbol LSP server version: {output.strip()}")
        return ""
    
    def _get_initialize_params(self, repository_root_path: str) -> dict:
        with open(os.path.join(os.path.dirname(__file__), "initialize_params.json"), "r") as f:
            d = json.load(f)
        assert d["rootPath"] == "$rootPath"
        d["rootPath"] = repository_root_path

        assert d["rootUri"] == "$rootUri"
        d["rootUri"] = Path(repository_root_path).resolve().as_uri()

        return d
    
    @asynccontextmanager
    async def start_server(self) -> AsyncIterator["Superbol"]:
        print("attempting to start the Superbol server")
        async with super().start_server():
            self.logger.log("Starting Superbol server process", logging.INFO)
            print("Starting Superbol server process")
            await self.server.start()
            initialize_params = self._get_initialize_params(self.repository_root_path)

            self.logger.log(
                "Sending initialize request from LSP client to LSP server and awaiting response",
                logging.INFO,
            )
            print("Sending initialize request from LSP client to LSP server and awaiting response")
            self.logger.log(f"Sending init params: {json.dumps(initialize_params, indent=4)}", logging.INFO)
            print(f"Sending init params: {json.dumps(initialize_params, indent=4)}")
            init_response = await self.server.send.initialize(initialize_params)
            self.logger.log(f"Received init response: {init_response}", logging.INFO)
            print(f"Received init response: {json.dumps(init_response,indent=2)}")
            assert init_response["capabilities"]["textDocumentSync"]["change"] == 2
            self.server.notify.initialized({})
            self.completions_available.set()

            self.server_ready.set()
            await self.server_ready.wait()

            yield self

            await self.server.shutdown()
            await self.server.stop()