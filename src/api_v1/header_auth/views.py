from fastapi import APIRouter, Depends, Header, HTTPException, status


router = APIRouter(
    prefix="/header_auth",
    tags=["header_auth"],
)

static_auth_token_to_username = {
    "83948787086fd61b3728efaef31cbc": "admin",
    "6580ddaefaa62f1197bf4fc0b87d011488": "password",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if token := static_auth_token_to_username.get(static_token):
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token invalid"
    )


@router.get("/some-http-header-auth-username/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    pass
