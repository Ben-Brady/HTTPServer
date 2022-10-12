from dataclasses import dataclass, field
from pathlib import Path
from mimetypes import guess_type


@dataclass
class Request:
    path: str
    headers: dict[str, str] = field(default_factory=dict)


@dataclass
class Response:
    status_code: int
    data: bytes = b""
    headers: dict[str, str] = field(default_factory=dict)


def parse_request(data: bytes) -> Request:
    lines = data.split(b"\r\n")
    first_line = lines[0]
    _, path, _ = first_line.split(b" ")
    path = path.decode()
    if path == "/":
        path = "/index.html"
    
    return Request(path=path)


def generate_response(req: Request) -> Response:
    headers = {}
    
    path = _generate_path(req.path)

    if not path.exists():
        return Response(status_code=404)
    else:
        mime, _ = guess_type(req.path)
        if mime:
            headers["Content-Type"] = mime
        
        return Response(
            status_code=200,
            data=path.read_bytes(),
            headers=headers
        )


def _generate_path(path:str) -> Path:
    STORE_PATH = Path("./src")
    file_path = Path(path)
    complete_path = STORE_PATH.joinpath(file_path.name)
    return complete_path


def encode_response(res: Response) -> bytes:
    lines = [b"HTTP/1.1 200 OK"]
    for name, value in res.headers.items():
        lines.append(name.encode() + b": " + value.encode())
    lines.extend([
        b"",
        res.data,
        b"",
    ])
    data = b"\r\n".join(lines)
    return data
