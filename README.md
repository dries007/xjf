# xjf 

Example project for experimenting with FastAPI, HTMX, jinja2 fragments and other old-is-new Web technology.

The goal is to create an example project where most resources can be accessed in one of 3 ways:

1. As JSON, when using the `Accepth application/json` header for API usage.
2. [HTMX](https://htmx.org/) (HTML fragment) if `HX-Request: true` is set, using either:
    - jinja2-fragments to render only relevant blocks (based on `HX-Target` header?)
    - A TBD header to select a different template file
3. A full page render otherwise.

To make life easier wrt validation & Pydantic integration, json-enc should be used for sending data back from HTML to the API instead of using Form encoded data.

To try this out, install the custom fork from fasthx <https://github.com/qteal/fasthx> (branch with last changes) and change `jinja2_fragments/fastapi.py` around line ~60:

```python
    def TemplateResponse(
        self,
        name: str,
        context: dict[str, typing.Any],
        status_code: int = 200,
        headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
        **kwargs: typing.Any,
    ) -> Response:
        request: Request = kwargs.get("request", context.get("request"))
        context.setdefault("request", request)

        hx_target = request.headers.get("HX-Target")

        template = self.get_template(name)

        block_name = kwargs.get("block_name", hx_target)
        block_names = kwargs.get("block_names", [])
        
        ...
```

