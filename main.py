from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models import Token, User, UserLogin, Role
from auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from dependencies import get_current_active_user, RoleChecker

app = FastAPI(title="FastAPI JWT RBAC Example")


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint to get JWT token.

    Default users:
    - username: admin, password: secret, role: admin
    - username: user, password: secret, role: user
    - username: moderator, password: secret, role: moderator
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def root():
    """Public endpoint - no authentication required"""
    return {"message": "Welcome to FastAPI JWT RBAC example"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info - requires authentication"""
    return current_user


@app.get("/users/all")
async def read_all_users(
    current_user: User = Depends(RoleChecker([Role.ADMIN]))
):
    """
    Get all users - requires ADMIN role
    """
    return {
        "message": "List of all users",
        "current_user": current_user.username,
        "role": current_user.role
    }


@app.get("/moderate")
async def moderate_content(
    current_user: User = Depends(RoleChecker([Role.ADMIN, Role.MODERATOR]))
):
    """
    Moderate content - requires ADMIN or MODERATOR role
    """
    return {
        "message": "Moderating content",
        "current_user": current_user.username,
        "role": current_user.role
    }


@app.get("/user-only")
async def user_endpoint(
    current_user: User = Depends(RoleChecker([Role.USER, Role.ADMIN, Role.MODERATOR]))
):
    """
    User endpoint - accessible by all authenticated users
    """
    return {
        "message": "User content",
        "current_user": current_user.username,
        "role": current_user.role
    }


@app.get("/admin-only")
async def admin_only_endpoint(
    current_user: User = Depends(RoleChecker([Role.ADMIN]))
):
    """
    Admin only endpoint - requires ADMIN role
    """
    return {
        "message": "Admin-only content",
        "current_user": current_user.username,
        "role": current_user.role
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
