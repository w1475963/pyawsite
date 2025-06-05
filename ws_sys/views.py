import os
import subprocess
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def sys_run(str_list: list[str]):
    try:
        result = subprocess.run(
            str_list,
            capture_output=True,  # 已包含stdout和stderr的PIPE设置
            cwd=os.getenv("PROJECT_ROOT", "."),
            text=True,
            timeout=180,
        )

    except subprocess.TimeoutExpired as e:
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": "",
            "error": f"Timeout(180)\n{e}",
        }
    except Exception as e:
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": "",
            "error": f"Exception\n{e}",
        }
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


@api_view(["POST"])
def ws_update(request):
    res = sys_run(["bash", "update.sh"])
    if "error" in res:
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    if res["returncode"] != 0:
        return Response(
            {
                **res,
                "error": "Run Failed",
            }
        )
    return Response(
        {
            "success": "Success",
            **res,
        }
    )
