import subprocess
from typing import Any, Dict, List, Optional
import json
from loguru import logger


class KubectlExecutor:
    """Utility to safely execute kubectl commands using Python subprocess."""

    @staticmethod
    def run(args: List[str], timeout: int = 15) -> Dict[str, Any]:
        """Execute a kubectl command and return structured output with stdout, stderr, and success status."""
        cmd = ["kubectl"] + args
        cmd_str = " ".join(cmd)
        logger.debug("Executing kubectl command: {}", cmd_str)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            success = result.returncode == 0
            if not success:
                logger.warning(
                    "kubectl command failed (code {}): {} | stderr: {}",
                    result.returncode,
                    cmd_str,
                    result.stderr.strip(),
                )
            else:
                logger.debug("kubectl command succeeded: {}", cmd_str)

            return {
                "success": success,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            logger.error("kubectl command timed out after {}s: {}", timeout, cmd_str)
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
            }
        except FileNotFoundError:
            logger.error("kubectl binary not found in system PATH")
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "kubectl binary not found in system PATH",
            }
        except Exception as e:
            logger.exception("Unexpected error executing kubectl: {}", e)
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
            }

    @classmethod
    def run_json(cls, args: List[str], timeout: int = 15) -> Optional[Dict[str, Any]]:
        """Execute a kubectl command requesting JSON output and parse it."""
        if "-o" not in args and "--output" not in args:
            args = args + ["-o", "json"]

        res = cls.run(args, timeout=timeout)
        if not res["success"] or not res["stdout"].strip():
            return None

        try:
            return json.loads(res["stdout"])
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse kubectl JSON output: {} | error: {}", res["stdout"][:200], e)
            return None
